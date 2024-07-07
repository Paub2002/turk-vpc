
from tkinter import * 
from PIL import ImageTk, Image
import numpy as np
import cv2
import Board
import chess
import chess.svg
import ia_funcions

##################################
# TODO 
# - Remove buttons 
# - Add file listener
# - button action into file 
# - undo functionality 
# - hint functionality ( conexion ) 
# - Detecció de colors. 
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
        self.placeholder = ImageTk.PhotoImage(Image.open("check.jpg"))
        self.video_frame =      Label(self.root)                             # Frame for video input
        self.transform_frame =  Label(self.root,image=self.placeholder)      # Frame for transformed input 

        self.points_frame = LabelFrame(self.root,text="Selected Points: ")                  # Frame for poitns
        self.go_button = Button(self.points_frame,text="CONTINUA",command=self.nextStage)   # Button for starting transformation
        self.moveButton = Button(self.points_frame,text="MOVE",command=self.getMove)   # Button for starting transformation
        self.hintButton = Button(self.points_frame,text="HINT",command=self.getHint)   # Button for starting transformation

        # Mostramos Objetos TK 
        self.video_frame.grid(row=0,column=0,sticky=E)
        self.points_frame.grid(row=0,column=1,sticky=NW,rowspan=3)
        self.transform_frame.grid(row=0,column=2,sticky=W) 
        self.moveButton.grid(row= 10)
        self.hintButton.grid(row=15)

        # Inicializaoms los puntos a seleccionar
        point0 = point(self.points_frame,-1,-1,"H8",0)
        point1 = point(self.points_frame,-1,-1,"A8",1)
        point2 = point(self.points_frame,-1,-1,"H1",2)
        point3 = point(self.points_frame,-1,-1,"A1",3)

        self.selected_points = [point0,point1,point2,point3]
        self.TMat = None
        self.coords = None
        self.turn = 0
        self.dstPoints = np.array([[0,512],[512,512],[0,0],[512,0]])
        self.lattice_lines = Board.getLatticeLines(np.array([0,0]),np.array([0,512]),np.array([512,0]),np.array([512,512]))
        self.mask = getMask(512)
        # Bindings de teclas. 
        self.video_frame.bind('<Button-1>',self.addPoint) # Registra un punto al hacer clic derecho
        self.root.bind('<Escape>',quit)                   # Esc Cierra la aplicacion 

        self.video_frame.after(10,self.showFrame)

        self.Board = chess.Board()
        self.transform = False

    def getMove(self): 
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

    def getHint(self):
        best_move = ia_funcions.getHintMove(self.Board.fen())
        print(best_move)
        #hint_move = ia_funcions.stockfish.get_best_move()

    def showFrame(self): 
         
        self.cvImage = capture_frame(self.captura)

        image = Image.fromarray(self.cvImage)
        img = ImageTk.PhotoImage(image = image)

        self.capture_image= img
        self.video_frame.configure(image=img)
        self.video_frame.after(10,self.showFrame)

    # Calcula la transformada del frame i lo muestra en el recuadro adecuado
    def showTransform(self): 


        wraped = cv2.warpPerspective(self.cvImage, self.TMat, (512,512))
        self.cvDest = wraped
        dst = wraped.copy()
        dst[self.mask,:] = 0
        image = Image.fromarray(dst)
        dst = ImageTk.PhotoImage(image = image)
        self.transform_image= dst 
        self.transform_frame.configure(image=dst)
        if self.transform == True : self.transform_frame.after(30,self.showTransform)

    # Completa la calibracion y muestra la transformacion 
    def nextStage(self):
        coords = []
        for point in self.selected_points:
            coords.append( [ point.getCoord() ] )
        coords = np.array(coords)
        self.coords = coords
        M,_ = cv2.findHomography(self.coords,self.dstPoints)
        self.TMat = M
        self.video_frame.after(10,self.showTransform)
        dst = cv2.warpPerspective(self.cvImage, self.TMat, (512,512))
        self.cvDest = dst
        self.last_move =proecssImage(dst)
        self.transform = True
    # Añade las coordenadas a un punto nuevo 
    def addPoint(self,event): 
        for p in self.selected_points:
            if not p.selected: 
                p.setCoord(event.x,event.y)
                break
        for p in self.selected_points:
            if not p.selected: 
                return
        # Si todos los puntos estan seleccionados muestra el boton para terminar la calibracion 
        self.spawnButton()
    # Muestra el boton 
    def spawnButton(self):
        self.go_button.grid(sticky=S + W + E)

         

class point: 
    def __init__(self,parent,x,y,cornerTag,row): 


        self.y = y
        self.selected = False 
        self.corner_tag = cornerTag
        text = "Corner {0}:".format(cornerTag)
        
        # Inicializamos los objetos TK 
        self.point_label = Label(parent,text= text)
        self.delete_button = Button(parent,text="X",command=self.unselect)

        # Mostramos los objetos TK 
        self.point_label.grid(row=row,column=0,sticky=W)
        self.delete_button.grid(row=row,column=1,sticky=E )

    # Deselecciona el punto, borra sus coordenadas. Llamada al hacer clic en el boton de la cruz
    def unselect(self): 

        self.x = -1
        self.y = -1
        self.selected = False
        text = "Corner {0}:".format(self.corner_tag)
        self.point_label.configure(text =text )

    def getCoord(self):
        return self.x,self.y

    # Setea las coordenadas y actualiza el texto
    def setCoord(self,x,y): 
        self.x = x
        self.y = y
        self.selected = True
        text = "Corner {0}: ({1}, {2})".format(self.corner_tag,x,y)
        self.point_label.configure(text =text )

def main():
    app = App()
    mainloop()
if __name__ == "__main__": 
    main()
        