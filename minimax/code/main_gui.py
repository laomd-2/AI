# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tkinter
from gambling.player import *
from gambling.evaluations import *
from sklearn.externals import joblib


class OthelloGUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(width=False, height=False)
        self.canvas = tkinter.Canvas(self.root, height=600, width=600)
        self.canvas.pack()
        self.board = Board(np.array(np.loadtxt("../data/board8.txt", dtype=int)))
        clf1 = joblib.load('../data/NNRegressor.pkl')
        clf2 = joblib.load('../data/NNRegressor.pkl')
        self.players = [MLPlayer(Board.FIRST, self.board, NNEvaluation(clf1)),
                        # SearchPlayer(Board.SECOND, self.board, NNEvaluation(clf2))]
                        HumanPlayer(Board.SECOND, self.board)]
        self.turn = 0
        self.drawBoard()

    def updateGame(self, event):
        print(self.players[self.turn].play())
        self.turn = not self.turn
        self.drawState()

    def drawBoard(self):
        for x in range(8):
            for y in range(8):
                x1 = x * 75
                y1 = y * 75
                x2 = x1 + 75
                y2 = y1 + 75
                item = self.canvas.create_rectangle(x1,y1,x2,y2,fill = '#1C9E18', tags = str(y*8+x))
                self.canvas.tag_bind(item,'<ButtonPress-1>',self.updateGame)
                self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5 ,outline= '#1C9E18', tags = 'tile'+str(y*8+x))
                self.drawState()
        
    def drawState(self):
        for i in range(8):
            for j in range(8):
                char = self.board.getState()[i, j]
                if char == Board.FIRST:
                    self.canvas.itemconfigure('tile' + str(i * 8 + j), fill='white')
                elif char == Board.SECOND:
                    self.canvas.itemconfigure('tile' + str(i * 8 + j), fill='black')

    def run(self):
        self.root.mainloop()


gui = OthelloGUI()
gui.run()
