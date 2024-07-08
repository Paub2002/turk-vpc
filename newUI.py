
from tkinter import * 
from PIL import ImageTk, Image
import numpy as np
import cv2
import Board
import chess
import chess.svg
# import ia_funcions

###########TODO####################
#
# - Remove buttons 
# - Add file listener
# - button action into file 
# - undo functionality 
# - hint functionality ( conexion ) 
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

        self.Board = chess.Board()
        self.transform = False
        self.getHomography()

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

def main():
    app = App()
    mainloop()
if __name__ == "__main__": 
    main()
        