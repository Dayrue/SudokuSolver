import pygame as pg
from copy import deepcopy
import numpy as np
import random

pg.init()
win = pg.display.set_mode((900, 900))
pg.display.set_caption("Sudoku Solver")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

win.fill(WHITE)

pg_images = ["pictures/one.png", "pictures/two.png", "pictures/three.png", 
             "pictures/four.png", "pictures/five.png", "pictures/six.png", 
             "pictures/seven.png", "pictures/eight.png", "pictures/nine.png", 
             "pictures/blank.png", "pictures/setOne.png", "pictures/setTwo.png",
             "pictures/setThree.png", "pictures/setFour.png", "pictures/setFive.png",
             "pictures/setSix.png", "pictures/setSeven.png", "pictures/setEight.png", "pictures/setNine.png",]

useImages = []
for i in pg_images:
    useImages.append(pg.image.load(i))

puzzles = [[[0, 0, 0, 2, 6, 0, 7, 0, 1],
          [6, 8, 0, 0, 7, 0, 0, 9, 0],
          [1, 9, 0, 0, 0, 4, 5, 0, 0],
          [8, 2, 0, 1, 0, 0, 0, 4, 0],
          [0, 0, 4, 6, 0, 2, 9, 0, 0],
          [0, 5, 0, 0, 0, 3, 0, 2, 8],
          [0, 0, 9, 3, 0, 0, 0, 7, 4],
          [0, 4, 0, 0, 5, 0, 0, 3, 6],
          [7, 0, 3, 0, 1, 8, 0, 0, 0]],
          [[1, 0, 0, 4, 8, 9, 0, 0, 6], 
          [7, 3, 0, 0, 0, 0, 0, 4, 0],
          [0, 0, 0, 0, 0, 1, 2, 9, 5],
          [0, 0, 7, 1, 2, 0, 6, 0, 0],
          [5, 0, 0, 7, 0, 3, 0, 0, 8],
          [0, 0, 6, 0, 9, 5, 7, 0, 0],
          [9, 1, 4, 6, 0, 0, 0, 0, 0],
          [0, 2, 0, 0, 0, 0, 0, 3, 7],
          [8, 0, 0, 5, 1, 2, 0, 0, 4]],
          [[0, 0, 0, 0, 2, 0, 0, 6, 0], 
          [0, 8, 0, 0, 0, 9, 7, 0, 0],
          [0, 0, 6, 7, 0, 0, 0, 0, 5],
          [3, 4, 0, 0, 0, 0, 0, 2, 0],
          [2, 0, 0, 0, 4, 0, 0, 0, 3],
          [0, 6, 0, 0, 0, 0, 0, 9, 4],
          [9, 0, 0, 0, 0, 4, 5, 0, 0],
          [0, 0, 8, 1, 0, 0, 0, 3, 0],
          [0, 5, 0, 0, 3, 0, 0, 0, 0]]]

puzzleNum = random.randint(0, len(puzzles) - 1)


puzzle = np.array(puzzles[puzzleNum])
origpuzzle = deepcopy(puzzle)

answer = []
for i in range(9):
    answer.append([0 for i in range(9)])
answer = np.array(answer)

for y in range(9):
    for x in range(9):
        if origpuzzle[y][x] != 0:
            answer[y][x] = origpuzzle[y][x]

def checkValid(x, y, num):
    #checks left to right
    for i in range(9):
        if puzzle[y][i] == num:
            return False
    for i in range(9):
        if puzzle[i][x] == num:
            return False
    for i in range(3):
        for q in range(3):
            if puzzle[(int(y / 3) * 3) + i][(int(x / 3) * 3) + q] == num:
                return False
    return True

def solvePuzzleVisual():
    for y in range(9):
        for x in range(9):
            if puzzle[y][x] == 0:
                for i in range(1, 10):
                    if checkValid(x, y, i):
                        puzzle[y][x] = i
                        win.blit(useImages[i - 1], (x * 100, y * 100))
                        pg.draw.rect(win, (0, 255, 0), pg.Rect(x * 100, y * 100, 100, 100), 5)
                        pg.display.update()
                        solvePuzzleVisual()
                        win.blit(useImages[i - 1], (x * 100, y * 100))
                        pg.draw.rect(win, (255, 0, 0), pg.Rect(x * 100, y * 100, 100, 100), 5)
                        pg.display.update()
                        puzzle[y][x] = 0
                return
    for y in range(9):
        for x in range(9):
            answer[y][x] = puzzle[y][x]

def solvePuzzle(checkList = []):
    for y in range(9):
        for x in range(9):
            if puzzle[y][x] == 0:
                for i in range(1, 10):
                    if checkValid(x, y, i):
                        puzzle[y][x] = i
                        solvePuzzle()
                        puzzle[y][x] = 0
                return
    for y in range(9):
        for x in range(9):
            answer[y][x] = puzzle[y][x]




def inputNumber(x, y):
    run2 = True
    truex, truey = x - (x % 100), y - (y % 100)
    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
    pg.display.update()
    while run2:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run2 = False

            if event.type == pg.MOUSEBUTTONUP:
                run2 = False
                win.fill(WHITE)
                drawWindow()
                pos = pg.mouse.get_pos()
                inputNumber(pos[0], pos[1])
                      
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    run2 = False
                if event.key == pg.K_BACKSPACE:
                    puzzle[int(truey / 100)][int(truex / 100)] = 0
                    win.blit(useImages[9], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_1 or event.key == pg.K_KP_1:
                    puzzle[int(truey / 100)][int(truex / 100)] = 1
                    win.blit(useImages[0], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_2 or event.key == pg.K_KP_2:
                    puzzle[int(truey / 100)][int(truex / 100)] = 2
                    win.blit(useImages[1], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_3 or event.key == pg.K_KP_3:
                    puzzle[int(truey / 100)][int(truex / 100)] = 3
                    win.blit(useImages[2], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_4 or event.key == pg.K_KP_4:
                    puzzle[int(truey / 100)][int(truex / 100)] = 4
                    win.blit(useImages[3], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_5 or event.key == pg.K_KP_5:
                    puzzle[int(truey / 100)][int(truex / 100)] = 5
                    win.blit(useImages[4], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_6 or event.key == pg.K_KP_6:
                    puzzle[int(truey / 100)][int(truex / 100)] = 6
                    win.blit(useImages[5], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_7 or event.key == pg.K_KP_7:
                    puzzle[int(truey / 100)][int(truex / 100)] = 7
                    win.blit(useImages[6], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_8 or event.key == pg.K_KP_8:
                    puzzle[int(truey / 100)][int(truex / 100)] = 8
                    win.blit(useImages[7], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()
                if event.key == pg.K_9 or event.key == pg.K_KP_9:
                    puzzle[int(truey / 100)][int(truex / 100)] = 9
                    win.blit(useImages[8], (truex, truey))
                    pg.draw.rect(win, (0, 0, 255), pg.Rect(truex, truey, 100, 100), 5)
                    pg.display.update()

def drawGrid():
    for y in range(9):
        for x in range(9):
            if puzzle[y][x] != 0 and origpuzzle[y][x] == 0:
                win.blit(useImages[puzzle[y][x] - 1], (x * 100, y * 100))
            elif puzzle[y][x] != 0:
                win.blit(useImages[puzzle[y][x] - 1 + 10], (x * 100, y * 100))
                
    blockSize = 100 #Set the size of the grid block
    for x in range(0, 900, blockSize):
        for y in range(0, 900, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(win, BLACK, rect, 1)

def drawWindow():
    drawGrid()

run = True 
while run:
    drawWindow()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LCTRL:
                puzzle = deepcopy(origpuzzle)
                solvePuzzleVisual()
                for y in range(9):
                    for x in range(9):
                        puzzle[y][x] = answer[y][x]
        
        if event.type == pg.MOUSEBUTTONUP:
            print(puzzle)
            print()
            win.fill(WHITE)
            drawWindow()
            pos = pg.mouse.get_pos()
            inputNumber(pos[0], pos[1])
            win.fill(WHITE)
            drawWindow()
            

    pg.display.update()