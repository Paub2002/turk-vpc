
from tkinter import * 
from PIL import ImageTk, Image
import numpy as np
import cv2
import Board
import chess
import chess.svg
import os
import ia_funcions

###########TODO####################
# - Tests 
# - Detecció de colors. 
#
##################################


# Para debug
from matplotlib import pyplot as plt
board_indices = [

    "h1","g1","f1","e1","d1","c1","b1","a1",
    "h2","g2","f2","e2","d2","c2","b2","a2",
    "h3","g3","f3","e3","d3","c3","b3","a3",
    "h4","g4","f4","e4","d4","c4","b4","a4",
    "h5","g5","f5","e5","d5","c5","b5","a5",
    "h6","g6","f6","e6","d6","c6","b6","a6",
    "h7","g7","f7","e7","d7","c7","b7","a7",
    "h8","g8","f8","e8","d8","c8","b8","a8"

]
def capture_frame(capture):
    return cv2.cvtColor(capture.read()[1],cv2.COLOR_BGR2RGB)

def getMask(size): 
    blank = np.zeros((size,size),dtype=bool)
    for i in range(0,size,size//8): 
        blank[i,:] = True
        blank[:,i] = True
    return blank

def proecssImage(image): 
    im = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    Blured  = cv2.GaussianBlur(im,(21,21),0)
    return Blured

def getLegalMove(board,sorted_squares): 
    max_back = 3
    sorted_squares = sorted_squares[::-1]
    indices_to_check = sorted_squares[:max_back]
    squares_to_check = []
    for i in indices_to_check: 
        squares_to_check.append(board_indices[i])
        print(board_indices[i])
    possible_moves = []
    for i in range(max_back):
        for j in range ( i+1 , max_back):
            possible_moves.append( squares_to_check[i] + squares_to_check[j] )
            possible_moves.append( squares_to_check[j] + squares_to_check[i] )
    for move in possible_moves: 
        if chess.Move.from_uci(move) in board.legal_moves: 
            return move
        
    ia_funcions.ilegalMove(move)
    return ""
class App: 
    def __init__(self): 
        
        self.root = Tk()
        self.root.title("Calibra al MechanicalTurkChessProMaster2000")
        self.captura = cv2.VideoCapture(1)
        # Initializamos objetos tk
        self.video_frame =      Label(self.root)                             # Frame for video input
        self.transform_frame =  Label(self.root)                             # Frame for transformed input 

        self.go_button =  Button(self.root, text="CONTINUA",command=self.getHomography) # Button for starting transformation

        # Mostramos Objetos TK 
        self.video_frame.grid(row=0,column=0,sticky=E)
        self.transform_frame.grid(row=0,column=2,sticky=W) 
        self.go_button.grid(row=16)

        # Demas variables 
        self.TMat = None
        self.turn = 0
        self.lattice_lines = Board.getLatticeLines(np.array([0,0]),np.array([0,512]),np.array([512,0]),np.array([512,512]))
        self.mask = getMask(512)

        # Bindings de teclas. 
        self.root.bind('<Escape>',quit)                   # Esc Cierra la aplicacion 

        self.video_frame.after(10,self.showFrame)
        self.root.after(20,self.checkServer)

        self.Board = chess.Board()
        self.transform = False
        self.getHomography()
        self.cvImage = capture_frame(self.captura)
        wraped = cv2.warpPerspective(self.cvImage, self.TMat, (512,512))
        self.cvDest = wraped
        self.last_move = proecssImage(wraped)

    def getHomography(self):
        self.TMat =  Board.AutoGetHomography(self.captura)

    def showFrame(self): 

        self.cvImage = capture_frame(self.captura)
        wraped = cv2.warpPerspective(self.cvImage, self.TMat, (512,512))
        self.cvDest = wraped

        dst = wraped.copy()
        dst[self.mask,:] = 0

        image = Image.fromarray(self.cvImage)
        dst = Image.fromarray(dst)

        img = ImageTk.PhotoImage(image = image)
        dst = ImageTk.PhotoImage(image = dst)

        self.capture_image= img
        self.transform_image= dst
        
        self.video_frame.configure(image=img)
        self.transform_frame.configure(image=dst)
        
        self.video_frame.after(10,self.showFrame)

    def checkServer(self): 
        dir = os.listdir()
        if 'move_req.txt' in dir: 
            self.move() 
            os.remove('move_req.txt')

        if 'hint_req.txt' in dir: 
            self.hint() 
            os.remove('hint_req.txt')
        if 'undo_req.txt' in dir: 
            self.undo() 
            os.remove('undo_req.txt')

        self.root.after(20,self.checkServer)
    def move(self):
        if self.turn % 2 == 0: 
            im =self.cvDest 
            image = proecssImage(im)        
            diffs = image - self.last_move
            m = np.logical_and( diffs > 10,diffs < 240) 
            diffs[~m] = 0 
            diffs[m] = 255

            # plt.imshow(diffs)
            # plt.show()
            squares = Board.splitquare(diffs)
            self.last_move = image 
            
            means = np.mean(squares,axis=(1,2))
            a = means.argsort()

            legal_move = getLegalMove(self.Board, a )
            #self.display_move(legal_move)

            turk_move = ia_funcions.Player_moves(self.Board,legal_move)
            print(turk_move)
            if legal_move != "":
                self.Board.push(chess.Move.from_uci(legal_move))
                self.Board.push(chess.Move.from_uci(turk_move))
                print(chess.Move.from_uci(legal_move))
        else: 
            im =self.cvDest 
            image = proecssImage(im)        
            self.last_move = image 
        self.turn+=1

    def hint(self):
        best_move = ia_funcions.getHintMove(self.Board.fen())
        print(best_move)

    def undo(self):
        self.Board.pop() 
        if self.turn % 2 == 0: 
            self.Board.pop()

def run():
    app = App()
    mainloop()
if __name__ == "__main__": 
    run()
        