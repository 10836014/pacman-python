import random
import threading
import time
from tkinter import *

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




def rightKey(event):
    global pacd;
    pacd = 0


def downKey(event):
    global pacd;
    pacd = 1


def leftKey(event):
    global pacd;
    pacd = 2


def upKey(event):
    global pacd;
    pacd = 3


def drawmap(w, img):
    for i in range(4):
        corner = 0

        while True:
            x = random.randint(0, 11)
            y = random.randint(0, 19)

            if x == 1 and y == 1:
                corner = 1

            if map[x][y] == 0 and corner == 0:
                map[x][y] = 3
                break
            else:
                continue

    for my in range(0, 12):
        global beans
        count = map[my].count(0) + map[my].count(3)
        beans += count
        for mx in range(0, 20):
            w.create_image(mx * 30, my * 30, anchor=NW, image=img[map[my][mx]])


def pacman(w, xy, di, color):
    global sw;
    r = 30
    global pacd
    global powerstate
    global starttime
    global beans

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

    if map[xy[1]][xy[0]] == 0:
        map[xy[1]][xy[0]] = 2
        beans -= 1
    elif map[xy[1]][xy[0]] == 3:
        map[xy[1]][xy[0]] = 2
        beans -= 1
        starttime = time.time()
        powerstate = 1

    x = xy[0] * r;
    y = xy[1] * r;

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


def Ghost(w, xy, di1, color,pac):
            # 0    1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17 18  19
    matrix= [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,-1, -1],#0
             [-1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 1, -1],#1
             [-1,  1, -1, -1,  1, -1, -1,  1, -1,  1, -1, -1, -1, -1, -1, -1,  1, -1, 1, -1],#2
             [-1,  1, -1,  1,  1, -1, -1,  1, -1,  1, -1, -1,  1,  1,  1,  1,  1,  1, 1, -1],#3
             [-1,  1,  1,  1, -1,  1,  1,  1,  1,  1,  1,  1,  1, -1, -1, -1, -1,  1, 1, -1],#4
             [-1,  1, -1,  1,  1,  1, -1,  1, -1, -1, -1, -1,  1, -1, -1,  1,  1,  1, 1, -1],#5
             [-1,  1, -1,  1, -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, -1, -1, 1, -1],#6
             [-1,  1, -1,  1, -1,  1, -1, -1, -1, -1, -1, -1,  1, -1, -1,  1, -1, -1, 1, -1],#7
             [-1,  1,  1,  1,  1,  1,  1,  1, -1,  1,  1,  1,  1, -1,  1,  1,  1,  1, 1, -1],#8
             [-1,  1,  1, -1, -1,  1,  1,  1, -1,  1, -1,  1,  1, -1,  1, -1,  1, -1, 1, -1],#9
             [-1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 1, -1],#10
             [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,-1, -1]]#11

    grid = Grid(matrix=matrix)

    ex = 0;
    ey = 0;
    iv = [2, 3, 0, 1];
    dl = [0, 0, 0, 0]
    w.create_image(xy[0] * 30, xy[1] * 30, anchor=NW, image=img[map[xy[1]][xy[0]]])
    od1 = iv[di1[0]];
    
    
    print("pacman 位置:"+str(pac))
    print("鬼位置:"+str(xy))
    print(xy[0],xy[1])
    
    
    start = grid.node(xy[0], xy[1])
    print(xy[0], xy[1])
    end = grid.node(pac[0], pac[1])
    print(pac[0], pac[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    print(path)
    # print(path[1][1])
    # print(path[1][0])

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    
    xy[0]=path[1][0];
    xy[1]=path[1][1];
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
    
###當pacman吃大力丸，鬼隨便走------
def Ghost1(w, xy, di1, color):
    ex = 0; ey = 0; iv = [2, 3, 0, 1]; dl = [0, 0, 0, 0]
    w.create_image(xy[0]*30, xy[1]*30, anchor=NW, image=img[map[xy[1]][xy[0]]])
    od1 = iv[di1[0]];
    
    # 哪邊可以走
    if map[xy[1]][xy[0]+1] % 2 == 0 or map[xy[1]][xy[0]+1] % 3 == 0: dl[0] = 1;
    if map[xy[1]+1][xy[0]] % 2 == 0 or map[xy[1] + 1][xy[0]] % 3 == 0: dl[1] = 1;
    if map[xy[1]][xy[0]-1] % 2 == 0 or map[xy[1]][xy[0]-1] % 3 == 0: dl[2] = 1;
    if map[xy[1]-1][xy[0]] % 2 == 0 or map[xy[1]-1][xy[0]] % 3 == 0: dl[3] = 1;

    while True:
        count = dl[0]+dl[1]+dl[2]+dl[3];
        # 如果只有一條可以走
        if count == 1: di1[0] = od1; break;
        # 如果有多條可以走
        ch = random.randint(0, 3)
        # ch = random.randint(0, 3)
        if dl[ch] == 1 and ch != od1: 
            di1[0] = ch
            break
    #向右
    if di1[0] == 0: 
        xy[0] = xy[0]+1
    #向下
    if di1[0] == 1: 
        xy[1] = xy[1]+1
    #向左
    if di1[0] == 2: 
        xy[0] = xy[0]-1
    #向上
    if di1[0] == 3: 
        xy[1] = xy[1]-1
        
    # draw ghost
    x = xy[0]*30; y = xy[1]*30

    # body
    w.create_arc(x+3, y, x+30-3, y+60, start=0, extent=180, fill=color, width=1)
    w.create_oval(x+6, y+9, x+14, y+17, fill="white", width=1)
    w.create_oval(x+16, y+9, x+24, y+17, fill="white", width=1)

    # -eye
    if di1[0] == 0: ex = 1;  ey = 0;
    if di1[0] == 1: ex = 0;  ey = 1;
    if di1[0] == 2: ex = -1; ey = 0;
    if di1[0] == 3: ex = 0;  ey = -1;
    w.create_oval(x+9+ex, y+12+ey, x+11+ex, y+14+ey, fill="black", width=2)
    w.create_oval(x+19+ex, y+12+ey, x+21+ex, y+14+ey, fill="black", width=2)

    # -leg
    w.create_arc(x+13, y+26, x+17, y+34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x+6, y+26, x+10, y+34, start=0, extent=180, fill="black", width=1)
    w.create_arc(x+20, y+26, x+24, y+34, start=0, extent=180, fill="black", width=1)
    


def draw(w):
    global powerstate
    global starttime
    
    # Pacman
    xy = [1, 1];
    di = [0]
    # Ghost red 行,列
    xy1 = [1, 10];
    di1 = [0]
    # Ghost blue
    xy2 = [15, 10];
    di2 = [2]

    drawmap(w=w, img=img)

    while True:
        if powerstate == 0:
            pacman(w=w, xy=xy, di=di, color="yellow")
            print("pacman:xy=["+str(xy[0])+","+str(xy[1])+"]")
            # Pacman碰到Ghost，黃色Game Over
            # if xy[0] == xy1[0] and xy[1] == xy1[1]:
            #     w.create_text(300, 180, fill="yellow", font="Times 35 italic bold", text="Game Over!")
            #     break
            # elif xy[0] == xy2[0] and xy[1] == xy2[1]:
            #     w.create_text(300, 180, fill="yellow", font="Times 35 italic bold", text="Game Over!")
            #     break
            
            #紅鬼
            if xy[0] == xy1[0] and xy[1] == xy1[1]:
                w.create_text(300, 180, fill="red", font="Times 35 italic bold", text="Game Over!")
                break
            Ghost(w=w, xy=xy1, di1=di1, color="red",pac=xy)
            # Red Ghost碰到Pacman，紅色Game Over
            print("red:xy1=["+str(xy1[0])+","+str(xy1[1])+"]")
            
            
            #藍鬼    
            if xy[0] == xy2[0] and xy[1] == xy2[1]:
                w.create_text(300, 180, fill="blue", font="Times 35 italic bold", text="Game Over!")
                break
            Ghost(w=w, xy=xy2, di1=di2, color="blue",pac=xy)
            # Blue Ghost碰到Pacman，藍色Game Over
            print("Blue:xy2=["+str(xy2[0])+","+str(xy2[1])+"]")
            
            
            #速度
            time.sleep(0.3)

        elif powerstate == 1:
            pacman(w=w, xy=xy, di=di, color="yellow")

            # Pacman吃了大力丸後，鬼變紫色且撞到不會Game Over
            Ghost1(w=w, xy=xy1, di1=di1, color="purple")
            Ghost1(w=w, xy=xy2, di1=di2, color="purple")
            time.sleep(0.3)

            if round(time.time() - starttime) == 10:
                powerstate = 0

        if beans == 0:
            w.create_text(300, 180, fill="yellow", font="Times 35 italic bold", text="YOU WIN!!!")
            break


# main program
sw = 0;
pacd = 4
img = []
powerstate = 0
beans = 0

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
