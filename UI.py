
from tkinter import * 
from PIL import ImageTk, Image
import numpy as np
import cv2
import Board
# Para debug
from matplotlib import pyplot as plt
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
    Blured  = cv2.GaussianBlur(im,(11,11),0)
    return Blured
class App: 
    def __init__(self): 
        
        self.root = Tk()
        self.root.title("Calibra al MechanicalTurkChessProMaster2000")
        self.captura = cv2.VideoCapture(0)


        # Placeholder per la homografia 
        self.placeholder =ImageTk.PhotoImage(Image.open("check.jpg"))

        # Initializamos objetos tk
        self.video_frame =      Label(self.root)                             # Frame for video input
        self.transform_frame =  Label(self.root,image=self.placeholder)      # Frame for transformed input 

        self.points_frame = LabelFrame(self.root,text="Selected Points: ")                  # Frame for poitns
        self.go_button = Button(self.points_frame,text="CONTINUA",command=self.nextStage)   # Button for starting transformation
        self.moveButton = Button(self.points_frame,text="MOVE",command=self.getMove)   # Button for starting transformation

        # Mostramos Objetos TK 
        self.video_frame.grid(row=0,column=0,sticky=E)
        self.points_frame.grid(row=0,column=1,sticky=NW,rowspan=3)
        self.transform_frame.grid(row=0,column=2,sticky=W) 
        self.moveButton.grid(row= 10)

        # Inicializaoms los puntos a seleccionar
        point0 = point(self.points_frame,-1,-1,"TL",0)
        point1 = point(self.points_frame,-1,-1,"TR",1)
        point2 = point(self.points_frame,-1,-1,"BL",2)
        point3 = point(self.points_frame,-1,-1,"BR",3)

        self.selected_points = [point0,point1,point2,point3]
        self.TMat = None
        self.coords = None
        self.dstPoints = np.array([[0,0],[0,512],[512,0],[512,512]])
        self.lattice_lines = Board.getLatticeLines(np.array([0,0]),np.array([0,512]),np.array([512,0]),np.array([512,512]))
        self.mask = getMask(512)
        # Bindings de teclas. 
        self.video_frame.bind('<Button-1>',self.addPoint) # Registra un punto al hacer clic derecho
        self.root.bind('<Escape>',quit)                   # Esc Cierra la aplicacion 

        self.video_frame.after(10,self.showFrame)

    def getMove(self): 
        im =self.cvDest 
        image = proecssImage(im)        
        diffs = image - self.last_move
        m = np.logical_and( diffs > 10,diffs < 240) 
        diffs[~m] = 0 
        diffs[m] = 255

        plt.imshow(diffs,'gray')
        plt.show()
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
        self.transform_frame.after(30,self.showTransform)

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
        