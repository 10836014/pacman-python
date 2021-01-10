import numpy as np

e = np.zeros((11, 11), dtype=int)
inf = 99999999
key_point = 1

# 讀入頂點個數，邊個數
n, m = map(int, input().split(' '))
# 初始化
for i in range(1, n+1):
    for j in range(1, n+1):
        if i == j : 
            e[i][j] = 0
        else:
            e[i][j] = inf

# 讀入邊
for i in range(1, m+1):
    t1, t2, t3 = map(int, input().split(' '))
    e[t1][t2] = t3

# 初始 dis 陣列，從 key_point 到其餘各點的初始路程
dis = np.zeros(11, dtype=int)
for i in range(1, n+1):
    dis[i] = e[key_point][i]

# 初始 book 陣列
book = np.zeros(11, dtype=int)
book[key_point] = 1

# Dijkstra Algorithm
for i in range(1, n):
    # 找到離 key_point 點最近的頂點
    min = inf
    for j in range(1, n+1):
        if book[j] == 0 and dis[j] < min :
            min = dis[j]
            u = j
    book[u] = 1
    for v in range(1, n+1):
        if e[u][v] < inf:
            if dis[v] > dis[u] + e[u][v]:
                dis[v] = dis[u] + e[u][v]

# 輸出
for i in range(1, n+1):
    print(dis[i])