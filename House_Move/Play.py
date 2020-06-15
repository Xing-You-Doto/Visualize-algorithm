
from tkinter import *
import time

def find_start(board):
    for i  in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i,j] == 1:
                tmp_point = (i,j)
                return (i,j)
def drawboard(root,canvas,board,startx=50,starty=50,cellwidth=20):

    width=2*startx+len(board)*cellwidth
    height=2*starty+len(board)*cellwidth
    canvas.config(width=width,height=height)
    for i  in range(board.shape[0]):
        for j in range(board.shape[1]):
            cellx=startx+i*cellwidth
            celly=starty+j*cellwidth
            canvas.create_rectangle(cellx,celly,cellx+cellwidth,celly+cellwidth,
                outline="black")
    canvas.update()
    tmp_point = find_start(board)
    flag = 1
    while(True):
        cellx = startx+tmp_point[0]*cellwidth
        celly = starty+tmp_point[1]*cellwidth
        canvas.create_rectangle(cellx,celly,cellx+cellwidth,celly+cellwidth,
                fill='black',outline="black")
        canvas.create_text(cellx+cellwidth//2,celly+cellwidth//2,text=str(flag),fill='white')
        canvas.update()
        flag += 1
        if flag == board.shape[0]*board.shape[1]+1:
            break 
        for pp in [(1,-2),(1,2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]:
            x = tmp_point[0]+pp[0]
            y = tmp_point[1]+pp[1]
            if 0 <= x < board.shape[0] and 0 <= y < board.shape[1]:
                if board[x,y] == flag:
                    tmp_point = (x,y)
        time.sleep(0.3)
def play_move(board):
    root=Tk()
    canvas=Canvas(root,bg="white")
    canvas.pack()
    drawboard(root,canvas,board)
    root.mainloop()