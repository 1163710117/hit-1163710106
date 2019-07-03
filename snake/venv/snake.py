from random import randint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

'''
    贪吃蛇
'''

# 窗口大小
width, height = 500, 500
# 宽度高度的格子数
widthPixel, heightPixel = 50, 50
''' 
    Snake速度的计时器。
    随着Snake吃的食物，这个计时器会减少
    蛇的速度更快
'''
t = 200

''' 
    Snake有两个变量定义
    1 snake_direction- 移动方向;
    - （0,1）：向上;
    - （0，-1）：向下;
    - （-1,1）：向左;
    - （1,0）：向右。
    2 snake_locate- 蛇身体位置列表：当吃到食物时，位置被添加到此列表中。
    - 蛇头最初位于（25.1）位置。
'''
snake_locate = [(25, 1)]  # 它开始只有一个位置（它的头部）
snake_direction = (1, 0)  # 正在进行的方向（开始向右）

'''
    屏幕的高度和宽度位置从0到49
    [0, 49]
    开始食物位置随机
'''
food = randint(1, 48), randint(1, 48)

'''
    用于控制游戏运行的标志
'''
gameRun = False  # 游戏进行
gameOver = False  # 游戏暂停

# 评分，初始为0
grade = 0

'''
	输入控制游戏的按键，
'''


def input_keyMenu(input_key, x, y):
    global gameRun
    '''
        确定游戏是否暂停。
        如果是，在进行暂停游戏时你应该回到循环中绘制Snake
    '''
    flagStop = gameRun

    # 通过在游戏中按“P”键暂停/开始
    if input_key == b'p':
        gameRun = not gameRun
    # 按'S'键开始游戏：
    if input_key == b's':
        gameRun = True
    # 按“R”重新开始游戏
    if input_key == b'r':
        restartgame()

    # 如果游戏在进行中，调用函数move
    if (not flagStop) and gameRun:
        move(1)


'''
	蛇的移动指令读入
'''


def input_keyMove(input_key, x, y):
    global snake_direction
    # 蛇是不可以反方向走的,但很有趣的一点是你可以在向左走的时候快速点击上和右，然后转头碰到自己的身体
    if input_key == GLUT_KEY_UP and snake_direction != (0, -1):
        snake_direction = (0, 1)
        # 上转向
    if input_key == GLUT_KEY_DOWN and snake_direction != (0, 1):
        snake_direction = (0, -1)
        # 下转向
    if input_key == GLUT_KEY_LEFT and snake_direction != (1, 0):
        snake_direction = (-1, 0)
        # 左转向
    if input_key == GLUT_KEY_RIGHT and snake_direction != (-1, 0):
        snake_direction = (1, 0)
        # 右转向


'''
	重启游戏
'''


def restartgame():
    global grade, food, snake_locate, snake_direction, gameRun, gameOver, t
    grade = 0
    # 成绩归零
    food = randint(1, 48), randint(1, 48)
    # 随机创建食物
    snake_locate = [(25, 1)]
    # 初始化蛇位置
    snake_direction = (1, 0)
    # 初始化蛇方向
    gameRun = True  # 游戏进行
    gameOver = False  # 游戏未结束
    # 重置速度计时器
    t = 200


'''
    根据键盘的交互移动Snake的功能。
    根据变量“snake_direction”的当前位置移动Snake。
    运动如下：将新像素插入第一个位置（在Snake头部前面）并从身体中移除最后一个像素。
    因此，根据设定的方向，它给人以运动的印象。
'''


def move(x):
    global food
    global t
    global grade
    global gameOver, gameRun

    # 将Snake移动到当前方向
    newLocation = moveSnake(snake_locate[0], snake_direction)
    snake_locate.insert(0, newLocation)  # 插入开头
    snake_locate.pop()  # 删除最后

    # 确定头部位置：
    (headX, headY) = snake_locate[0]

    # 确定Snake的头是否碰到身体的任何部位（游戏关闭）
    # 条件是头部与其他部分处于相同位置
    for i in range(1, len(snake_locate)):
        temp = snake_locate[i]
        if headX == temp[0] and headY == temp[1]:
            gameOver = True
            gameRun = False

    # 确定Snake是否吃了食物：
    if headX == food[0] and headY == food[1]:
        # 增加Snake的体型：
        snake_locate.append(food)
        # 为食物创造新的位置：
        food = randint(1, 48), randint(1, 48)
        # 通过减慢计时器和Snake更快来增加游戏难度
        t -= 5
        # 提高分数
        grade += 10

    if gameRun:
        glutTimerFunc(t, move, 1)  # 定时器启动
    elif gameOver:
        print("Game Over")


'''
   蛇身体进行移动：增加位置加上当前的方向
'''


def moveSnake(point1, point2):
    global gameRun, gameOver
    x = point1[0] + point2[0]
    y = point1[1] + point2[1]

    # 撞墙了
    if x >= 49 or y >= 49 or x <= 0 or y <= 0:
        gameRun = False
        gameOver = True

    return (x, y)


def drawfoods():
    glColor3f(1.0, 0.0, 1.0)
    # 发送坐标以在屏幕上绘制食物：
    drawLocate(food[0], food[1], 1, 1)


def drawSnake():
    glColor3f(1.0, 1.0, 1.0)  # 蛇的颜色：白色
    for x, y in snake_locate:  # 对于蛇身体的每一点
        drawLocate(x, y, 1, 1)  # 绘制高度和宽度为1的位置（x，y）


'''
    把500*500的窗口分成50*50的格子
	将窗口大小按照格子数分割
'''


def restartMap(width, height, widthLocationMap, heightLocationMap):
    glViewport(0, 0, width, height)  # 指定视口的尺寸
    glMatrixMode(GL_PROJECTION)  # 指定坐标系
    glLoadIdentity()  # 用于标识的数组数组
    glOrtho(0.0, widthLocationMap, 0.0, heightLocationMap, 0.0, 1.0) #分出2D的格子
    glMatrixMode(GL_MODELVIEW) # 指定当前矩阵
    glLoadIdentity() # 重置当前指定的矩阵为单位矩阵


'''
    负责从Snake身体绘制像素的功能。.
'''


def drawLocate(x, y, width, height):
    glBegin(GL_QUADS) # 绘制由四个顶点组成的一组单独的四边形
    glVertex2f(x, y) # 画点
    glVertex2f(x + width, y)
    glVertex2f(x + height, y + height)
    glVertex2f(x, y + height)
    glEnd() # 与begin一起用，结束绘制


'''
    始终调用绘图功能
'''


def draw():
    global food
    # 清除屏幕
    glClear(GL_COLOR_BUFFER_BIT)
    # 使用单位矩阵初始化当前数组（不累积转换）：
    glLoadIdentity()
    # 设置位置图的内部尺寸：
    restartMap(width, height, widthPixel, heightPixel)
    # 屏幕清除后，在屏幕上绘制所有蛇和食物：
    drawfoods()
    drawSnake()
    # 如果游戏终止：
    if gameOver:
        food = (50, 50)
		# 输出结果
        drawTexto("Game Over!  ", 17, 30)
        drawTexto("Grades: " + str(grade), 17, 22)

    glutSwapBuffers() # 避免闪烁


def drawTexto(string, x, y):
    glPushMatrix() # 把当前状态压入
    glColor3f(1.0, 0.0, 0.0)
    # 在将要放置文本的Universe中的位置
    glRasterPos2f(x, y)
    # 逐个字符显示
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glPopMatrix() # 将当前状态弹出


# 主要功能：初始化和交互功能
def main():
    glutInit(sys.argv)  # 初始化
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # 注意使用什么样的视图
    glutInitWindowSize(width, height)  # 将窗口大小设置为特定大小
    glutInitWindowPosition(200, 200)  # 设置窗口在屏幕上的位置
    glutCreateWindow(b"Snake")  # 创建一个具有已定义标题的窗口
    glutDisplayFunc(draw)  # 设置要显示的回调函数
    glutIdleFunc(draw)  # 在后台执行操作（调用函数draw（））
    glutKeyboardFunc(input_keyMenu)  # 接收键盘交互
    glutSpecialFunc(input_keyMove)  # 接收键盘交互
    glutMainLoop()# 进入GLUT事件处理循环


# 调用主要功能
main()