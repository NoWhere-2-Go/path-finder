import curses
from curses import wrapper
import enum
import queue
import time
from turtle import st

# 'O' is the beginning, '#' are obstacles in the path
# 'X' is the exit of the maze, " " are open paths
maze = [
    ["#", "#", "#", "#", "#", "#", "#", "O", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):
    CYAN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row, in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, CYAN)


def find_start(maze, start):

    # iterate though each row and column to find the starting position
    for i , row in  enumerate(maze):
        for j, value in enumerate(row):
            # once "O" is found return it's position
            if value == start:
                return i, j

    # if "O" isn't found print not found and return none
    print("start of maze not found!")
    return None

# function to find shortest path possible
def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    # will for now [start_pos] but every iteration it will grow and change
    q1 = queue.Queue()
    q1.put((start_pos, [start_pos]))

    visited = set()

    # while the queue isn't empty get the current position and the path
    while not q1.empty():
        current_pos, path = q1.get()
        row, col = current_pos

        # clear screen and print this iteration of the path
        stdscr.clear()
        print_maze(maze, stdscr, path)
        # change the time of the printing so it can illustrate BFS
        time.sleep(0.3)
        stdscr.refresh()

        # check if we have found 'X'
        if maze[row][col] == end:
            return path
    
        # find neighbors of the node (but is array in this case, so index???)
        # add those neighbors to the path and put them in queue
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue
        
            new_path = path + [neighbor]
            q1.put((neighbor, new_path))
            visited.add(neighbor)

def find_neighbors(maze, row, col):
    # create empty list of neighbors
    neighbors = []

    if row > 0:     # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):     # DOWN
        neighbors.append((row + 1, col))
    if col > 0:    # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)