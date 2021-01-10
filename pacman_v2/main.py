import random
import threading
import time
from tkinter import *

# 先執行 pip install pathfinding
# https://pypi.org/project/pathfinding/
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
       [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
       [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# 前進方向向右
def rightKey(event):
    global pacd;
    pacd = 0


# 前進方向向下
def downKey(event):
    global pacd;
    pacd = 1


# 前進方向向左
def leftKey(event):
    global pacd;
    pacd = 2


# 前進方向向上
def upKey(event):
    global pacd;
    pacd = 3


def drawmap(w, img):
    # 隨機產生四顆大力丸
    for i in range(4):
        corner = 0

        while True:
            x = random.randint(0, 11)
            y = random.randint(0, 19)

            if x == 1 and y == 1:
                corner = 1
            # 把原本的黃點 0，取代成大力丸 3
            if map[x][y] == 0 and corner == 0:
                map[x][y] = 3
                break
            else:
                continue

    # 根據地圖上的各個位置，擺入正確的圖片
    # map0 黃點
    # map1 牆壁
    # map2 全黑(被吃掉)
    # map3 黃點(大力丸)
    for my in range(0, 12):
        global beans
        count = map[my].count(0) + map[my].count(3)
        beans += count
        # 計算場上產生的黃點+大力丸總數
        for mx in range(0, 20):
            w.create_image(mx * 30, my * 30, anchor=NW, image=img[map[my][mx]])


def pacman(w, xy, di, color):
    global sw;
    r = 30  # 小精靈嘴巴開口角度
    global pacd  # 小精靈的前進方向
    global powerstate  # 小精靈的狀態(是否吃的大力丸)
    global starttime  # 存下當時吃到大力丸的時間
    global beans  # 吃到的點數數量
    global scores  # 計算分數

    w.create_image(xy[0] * r, xy[1] * r, anchor=NW, image=img[map[xy[1]][xy[0]]])

    if pacd == 0 and (map[xy[1]][xy[0] + 1] % 2 == 0 or map[xy[1]][xy[0] + 1] % 3 == 0):  # Pacman往右
        xy[0] = xy[0] + 1
        di[0] = 0
    if pacd == 1 and (map[xy[1] + 1][xy[0]] % 2 == 0 or map[xy[1] + 1][xy[0]] % 3 == 0):  # Pacman往下
        xy[1] = xy[1] + 1
        di[0] = 1
    if pacd == 2 and (map[xy[1]][xy[0] - 1] % 2 == 0 or map[xy[1]][xy[0] - 1] % 3 == 0):  # Pacman往左
        xy[0] = xy[0] - 1
        di[0] = 2
    if pacd == 3 and (map[xy[1] - 1][xy[0]] % 2 == 0 or map[xy[1] - 1][xy[0]] % 3 == 0):  # Pacman往上
        xy[1] = xy[1] - 1
        di[0] = 3

    # 吃掉黃點，總點數減1
    if map[xy[1]][xy[0]] == 0:
        map[xy[1]][xy[0]] = 2
        beans -= 1
        scores += 1
    # 吃掉大力丸，總點數減1，狀態變成1
    elif map[xy[1]][xy[0]] == 3:
        map[xy[1]][xy[0]] = 2
        beans -= 1
        scores += 1
        starttime = time.time()  # 吃到大力丸的時間
        powerstate = 1

    x = xy[0] * r;
    y = xy[1] * r;

    # sw判斷小精靈開口方向
    if di[0] == 0:
        if sw == 0:
            w.create_arc(x, y, x + r, y + r, start=30, extent=300, fill=color, width=3)  # 右開嘴
        else:
            w.create_arc(x, y, x + r, y + r, start=0, extent=359, fill=color, width=3)  # 右合嘴
    if di[0] == 1:
        if sw == 0:
            w.create_arc(x, y, x + r, y + r, start=-60, extent=300, fill=color, width=3)  # 下開嘴
        else:
            w.create_arc(x, y, x + r, y + r, start=-90, extent=359, fill=color, width=3)  # 下合嘴
    if di[0] == 2:
        if sw == 0:
            w.create_arc(x, y, x + r, y + r, start=150, extent=-300, fill=color, width=3)  # 左開嘴
        else:
            w.create_arc(x, y, x + r, y + r, start=180, extent=-359, fill=color, width=3)  # 左合嘴
    if di[0] == 3:
        if sw == 0:
            w.create_arc(x, y, x + r, y + r, start=60, extent=-300, fill=color, width=3)  # 上開嘴
        else:
            w.create_arc(x, y, x + r, y + r, start=90, extent=-359, fill=color, width=3)  # 上合嘴

    sw = ~ sw


# 鬼追小精靈，用A* Search演算法
# Ghsot(畫布, 鬼的座標, 鬼要走的方向, 鬼的顏色, PacMan的座標)
def Ghost(w, xy, di1, color, pac):
    global matrix
    # 使用二維網格
    grid = Grid(matrix=matrix)

    ex = 0;
    ey = 0;
    iv = [2, 3, 0, 1];
    dl = [0, 0, 0, 0]
    w.create_image(xy[0] * 30, xy[1] * 30, anchor=NW, image=img[map[xy[1]][xy[0]]])
    od1 = iv[di1[0]];

    print("pacman 位置:" + str(pac))
    print("鬼位置:" + str(xy))
    print(xy[0], xy[1])

    start = grid.node(xy[0], xy[1])
    print(xy[0], xy[1])
    end = grid.node(pac[0], pac[1])
    print(pac[0], pac[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    print(path)
    print(path[1][1])
    print(path[1][0])

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))

    xy[0] = path[1][0];
    xy[1] = path[1][1];
    # draw ghost
    x = (path[1][0]) * 30
    y = (path[1][1]) * 30

    # body
    w.create_arc(x + 3, y, x + 30 - 3, y + 60, start=0, extent=180, fill=color, width=1)
    w.create_oval(x + 6, y + 9, x + 14, y + 17, fill="white", width=1)
    w.create_oval(x + 16, y + 9, x + 24, y + 17, fill="white", width=1)

    # -eye
    if di1[0] == 0: ex = 1;  ey = 0;
    if di1[0] == 1: ex = 0;  ey = 1;
    if di1[0] == 2: ex = -1; ey = 0;
    if di1[0] == 3: ex = 0;  ey = -1;
    w.create_oval(x + 9 + ex, y + 12 + ey, x + 11 + ex, y + 14 + ey, fill="black", width=2)
    w.create_oval(x + 19 + ex, y + 12 + ey, x + 21 + ex, y + 14 + ey, fill="black", width=2)

    # -leg
    w.create_arc(x + 13, y + 26, x + 17, y + 34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x + 6, y + 26, x + 10, y + 34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x + 20, y + 26, x + 24, y + 34, start=0, extent=180, fill="black", width=1)


# 當pacman吃大力丸，鬼隨便走------
# Ghsot1(畫布, 鬼的座標, 鬼要走的方向, 鬼的顏色, PacMan的座標)
def Ghost1(w, xy, di1, color):
    ex = 0;
    ey = 0;
    iv = [2, 3, 0, 1];
    dl = [0, 0, 0, 0];  # 可以走的方向，初始都是0
    w.create_image(xy[0] * 30, xy[1] * 30, anchor=NW, image=img[map[xy[1]][xy[0]]])
    od1 = iv[di1[0]];

    # 哪邊可以走
    if map[xy[1]][xy[0] + 1] % 2 == 0 or map[xy[1]][xy[0] + 1] % 3 == 0: dl[0] = 1;  # 鬼可以向右走，dl[0]存成1
    if map[xy[1] + 1][xy[0]] % 2 == 0 or map[xy[1] + 1][xy[0]] % 3 == 0: dl[1] = 1;  # 鬼可以向下走，dl[1]存成1
    if map[xy[1]][xy[0] - 1] % 2 == 0 or map[xy[1]][xy[0] - 1] % 3 == 0: dl[2] = 1;  # 鬼可以向左走，dl[2]存成1
    if map[xy[1] - 1][xy[0]] % 2 == 0 or map[xy[1] - 1][xy[0]] % 3 == 0: dl[3] = 1;  # 鬼可以向上走，dl[3]存成1

    while True:
        count = dl[0] + dl[1] + dl[2] + dl[3];
        # 如果鬼只有一條可以走
        if count == 1: di1[0] = od1; break;
        # 如果鬼有多條可以走
        ch = random.randint(0, 3)
        if dl[ch] == 1 and ch != od1:
            di1[0] = ch
            break
    # 向右
    if di1[0] == 0:
        xy[0] = xy[0] + 1
    # 向下
    if di1[0] == 1:
        xy[1] = xy[1] + 1
    # 向左
    if di1[0] == 2:
        xy[0] = xy[0] - 1
    # 向上
    if di1[0] == 3:
        xy[1] = xy[1] - 1

    # draw ghost
    x = xy[0] * 30;
    y = xy[1] * 30

    # body
    w.create_arc(x + 3, y, x + 30 - 3, y + 60, start=0, extent=180, fill=color, width=1)
    w.create_oval(x + 6, y + 9, x + 14, y + 17, fill="white", width=1)
    w.create_oval(x + 16, y + 9, x + 24, y + 17, fill="white", width=1)

    # -eye
    if di1[0] == 0: ex = 1;  ey = 0;
    if di1[0] == 1: ex = 0;  ey = 1;
    if di1[0] == 2: ex = -1; ey = 0;
    if di1[0] == 3: ex = 0;  ey = -1;
    w.create_oval(x + 9 + ex, y + 12 + ey, x + 11 + ex, y + 14 + ey, fill="black", width=2)
    w.create_oval(x + 19 + ex, y + 12 + ey, x + 21 + ex, y + 14 + ey, fill="black", width=2)

    # -leg
    w.create_arc(x + 13, y + 26, x + 17, y + 34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x + 6, y + 26, x + 10, y + 34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x + 20, y + 26, x + 24, y + 34, start=0, extent=180, fill="black", width=1)


def draw(w):
    global powerstate
    global starttime
    global scores
    # Pacman的起始位置
    # 出現在地圖的最左上角
    xy = [1, 1];  # xy = pacman的所在座標
    di = [0];  # di = pacman要前進的方向
    # Ghost red (行,列)
    xy1 = [1, 10];  # xy1 = 紅鬼的所在座標
    di1 = [0];  # di1 = 紅鬼要前進的方向
    # Ghost blue (行,列) 
    xy2 = [15, 10];  # xy2 = 藍鬼的所在座標
    di2 = [2];  # di2 = 藍鬼要前進的方向

    drawmap(w=w, img=img)

    while True:
        if powerstate == 0:
            pacman(w=w, xy=xy, di=di, color="yellow")
            print("pacman:xy=[" + str(xy[0]) + "," + str(xy[1]) + "]")
            # Pacman碰到Ghost，黃色Game Over
            # if xy[0] == xy1[0] and xy[1] == xy1[1]:
            #     w.create_text(300, 180, fill="yellow", font="Times 35 italic bold", text="Game Over!")
            #     break
            # elif xy[0] == xy2[0] and xy[1] == xy2[1]:
            #     w.create_text(300, 180, fill="yellow", font="Times 35 italic bold", text="Game Over!")
            #     break

            # 紅鬼和pacman的座標相疊
            if xy[0] == xy1[0] and xy[1] == xy1[1]:
                w.create_text(300, 180, fill="red", font="Times 35 italic bold",
                              text="Game Over!\nYour score : %s" % scores)
                break
            Ghost(w=w, xy=xy1, di1=di1, color="red", pac=xy)
            # Red Ghost碰到Pacman，紅色Game Over
            print("red:xy1=[" + str(xy1[0]) + "," + str(xy1[1]) + "]")

            # 藍鬼和pacman的座標相疊
            if xy[0] == xy2[0] and xy[1] == xy2[1]:
                w.create_text(300, 180, fill="blue", font="Times 35 italic bold",
                              text="Game Over!\nYour score : %s" % scores)
                break
            Ghost(w=w, xy=xy2, di1=di2, color="blue", pac=xy)
            # Blue Ghost碰到Pacman，藍色Game Over
            print("Blue:xy2=[" + str(xy2[0]) + "," + str(xy2[1]) + "]")

            # 速度(越大越慢)
            time.sleep(0.3)

        # Pacman吃了大力丸後，狀態變成1
        elif powerstate == 1:
            pacman(w=w, xy=xy, di=di, color="yellow")

            # 鬼變紫色且撞到不會Game Over
            Ghost1(w=w, xy=xy1, di1=di1, color="purple")
            Ghost1(w=w, xy=xy2, di1=di2, color="purple")
            time.sleep(0.3)

            # 大力丸的效力只維持10秒
            if round(time.time() - starttime) == 10:
                powerstate = 0

        # 如果場上的點數全部被吃光了，跳出勝利提示訊息
        if beans == 0:
            w.create_text(300, 180, fill="yellow", font="Times 35 italic bold",
                          text="YOU WIN!!!\nYour score : %s" % scores)
            break


# main program
sw = 0;
pacd = 4
img = []
powerstate = 0
beans = 0
scores = 0
matrix = [[-1 if b == 1 else 1 for b in i] for i in map]

root = Tk()
root.title("Pacman")

w = Canvas(root, width=600, height=360, bg="green")
w.pack()

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Down>', downKey)
root.bind('<Up>', upKey)

for i in range(4):
    img.insert(i, PhotoImage(file="map" + str(i) + ".png"))

t = threading.Thread(target=draw, args=(w,)).start()

root.mainloop()
