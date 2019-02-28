#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
迷宫 https://www.lintcode.com/problem/the-maze/description
在迷宫中有一个球，里面有空的空间和墙壁。球可以通过滚上，下，左或右移动，
但它不会停止滚动直到撞到墙上。当球停止时，它可以选择下一个方向。

给定球的起始位置，目的地和迷宫，确定球是否可以停在终点。
迷宫由二维数组表示。1表示墙和0表示空的空间。你可以假设迷宫的边界都是墙。开始和目标坐标用行和列索引表示。

1.在迷宫中只有一个球和一个目的地。
2.球和目的地都存在于一个空的空间中，它们最初不会处于相同的位置。
3.给定的迷宫不包含边框(比如图片中的红色矩形)，但是你可以假设迷宫的边界都是墙。
5.迷宫中至少有2个空的空间，迷宫的宽度和高度都不会超过100。

输入:
map =
[
 [0,0,1,0,0],
 [0,0,0,0,0],
 [0,0,0,1,0],
 [1,1,0,1,1],
 [0,0,0,0,0]
]
start = [0,4] end = [3,2] 输出: false

例2:
输入:
map =
[[0,0,1,0,0],
 [0,0,0,0,0],
 [0,0,0,1,0],
 [1,1,0,1,1],
 [0,0,0,0,0]
]
start = [0,4] end = [4,4] 输出: true
"""


class Solution1:
    """
    @param maze: the maze
    @param start: the start
    @param destination: the destination
    @return: whether the ball could stop at the destination
    """

    def hasPath(self, maze, start, destination):
        start, destination = tuple(start), tuple(destination)
        rows, cols = len(maze), len(maze[0])
        visited = set(start)
        q = [start]
        while q:
            x, y = q.pop(0)
            visited.add((x, y))
            if (x, y) == destination:
                return True
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x, y
                while 0 <= nx + dx < rows and 0 <= ny + dy < cols and maze[nx + dx][ny + dy] == 0:
                    nx += dx
                    ny += dy
                if (nx, ny) not in visited:
                    q.append((nx, ny))
                    # end for
        # end while
        return False


"""
迷宫2  https://www.lintcode.com/problem/the-maze-ii/description
在迷宫中有一个球，里面有空的空间和墙壁。球可以通过滚上，下，左或右移动，但它不会停止滚动直到撞到墙上。当球停止时，它可以选择下一个方向。

给定球的起始位置，目标和迷宫，找到最短距离的球在终点停留。距离是由球从起始位置(被排除)到目的地(包括)所走过的空空间的数量来定义的。如果球不能停在目的地，返回-1。
迷宫由二维数组表示。1表示墙和0表示空的空间。你可以假设迷宫的边界都是墙。开始和目标坐标用行和列索引表示。

1.在迷宫中只有一个球和一个目的地。
2.球和目的地都存在于一个空的空间中，它们最初不会处于相同的位置。
3.给定的迷宫不包含边框(比如图片中的红色矩形)，但是你可以假设迷宫的边界都是墙。
4.迷宫中至少有2个空的空间，迷宫的宽度和高度都不会超过100。

样例 1:
	输入:
	(rowStart, colStart) = (0,4)
	(rowDest, colDest)= (4,4)
	0 0 1 0 0
	0 0 0 0 0
	0 0 0 1 0
	1 1 0 1 1
	0 0 0 0 0

	输出:  12

	解释:
	(0,4)->(0,3)->(1,3)->(1,2)->(1,1)->(1,0)->(2,0)->(2,1)->(2,2)->(3,2)->(4,2)->(4,3)->(4,4)

样例 2:
	输入:
	(rowStart, colStart) = (0,4)
	(rowDest, colDest)= (0,0)
	0 0 1 0 0
	0 0 0 0 0
	0 0 0 1 0
	1 1 0 1 1
	0 0 0 0 0

	输出:  6

	解释:
	(0,4)->(0,3)->(1,3)->(1,2)->(1,1)->(1,0)->(0,0)
"""


class Solution2:
    """
    @param maze: the maze
    @param start: the start
    @param destination: the destination
    @return: the shortest distance for the ball to stop at the destination
    """

    def shortestDistance(self, maze, start, destination):
        start, destination = tuple(start), tuple(destination)
        rows, cols = len(maze), len(maze[0])
        visited = set(start)
        q = [(start[0], start[1], 0)]
        while q:
            x, y, step = q.pop(0)
            visited.add((x, y))
            if (x, y) == destination:
                return step
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x, y
                tmp = 0
                while 0 <= nx + dx < rows and 0 <= ny + dy < cols and maze[nx + dx][ny + dy] == 0:
                    nx += dx
                    ny += dy
                    tmp += 1
                if (nx, ny) not in visited:
                    q.append((nx, ny, step + tmp))
                    # end for
        # end while
        return -1


"""
迷宫3 https://www.lintcode.com/problem/the-maze-iii/description
在迷宫中有一个球，里面有空的空间和墙壁。球可以通过滚up (u)、down (d)、left (l)或右right (r)来穿过空的空间，
但它不会停止滚动直到撞到墙上。当球停止时，它可以选择下一个方向。在这个迷宫里还有一个洞。如果球滚到洞里，球就会掉进洞里。
给定球的位置、洞的位置和迷宫，找出球如何通过移动最短距离落入洞内。
距离是由球从起始位置(被排除)到洞(包括)所走过的空空间的数量来定义的。用“u”、“d”、“l”和“r”来输出移动的方向。
由于可能有几种不同的最短路径，所以你应该输出字母顺序中（移动顺序中）最短的方法。如果球打不进洞，输出“impossible”。
迷宫由二维数组表示。1表示墙和0表示空的空间。你可以假设迷宫的边界都是墙。球和孔坐标用行和列的索引表示。

1.迷宫中只有一个球和一个洞。
2.球和洞都存在于一个空的空间中，它们最初不会处于相同的位置。
3.给定的迷宫不包含边框(比如图片中的红色矩形)，但是你可以假设迷宫的边界都是墙。
4.迷宫中至少有2个空的空间，迷宫的宽度和高度不会超过30。
输入:
由二维数组表示的迷宫。

0 0 0 0 0
1 1 0 0 1
0 0 0 0 0
0 1 0 0 1
0 1 0 0 0

球坐标(rowBall, colBall) = (4,3)
孔坐标(roall, colHole) = (0,1)

输出:“lul”
"""


class Solution3:
    """
    @param maze: the maze
    @param ball: the ball position
    @param hole: the hole position
    @return: the lexicographically smallest way
    """

    def findShortestWay(self, maze, ball, hole):
        if ball == hole:
            return ""
        ball, hole = tuple(ball), tuple(hole)
        rows, cols = len(maze), len(maze[0])
        visited = set(ball)
        q = [(ball[0], ball[1], '', 0)]
        ok = True
        ans, min_step = 'z', float('inf')
        while q:
            x, y, path, step = q.pop(0)
            visited.add((x, y))
            for dx, dy, direction in ((1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r'), (-1, 0, 'u')):
                nx, ny = x, y
                tmp = 0
                while 0 <= nx + dx < rows and 0 <= ny + dy < cols and maze[nx + dx][ny + dy] == 0:
                    nx += dx
                    ny += dy
                    tmp += 1
                    if (nx, ny) == hole and (step + tmp) <= min_step:
                        ok = False
                        ans = min(path + direction, ans) if (step + tmp) == min_step else path + direction
                        min_step = step + tmp
                    # end if
                # end while
                if (nx, ny) not in visited and (step + tmp) <= min_step:
                    q.append((nx, ny, path + direction, step + tmp))
            # end for
        # end while
        return "impossible" if ok else ans


maze_ = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 1]]
ball_ = [0, 4]
hole_ = [3, 0]
print(Solution3().findShortestWay(maze_, ball_, hole_))
