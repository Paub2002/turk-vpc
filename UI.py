from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import cv2
def capture_frame(capture):
    return cv2.cvtColor(capture.read()[1],cv2.COLOR_BGR2RGB)

class VideoLabel(Label): 

    def onRightclick(self,event): 
        
        x,y = event.x,event.y
        self.selected_points.append([x,y])

    def onLeftclick(self,event): 
        self.show_camera = False 
    def show_frame(self):
        cvImage = capture_frame(self.cap) 

        for x,y in self.selected_points: 
            cv2.circle(cvImage,(x,y),10,(255,0,0),-1)

        image = Image.fromarray(cvImage)
        img = ImageTk.PhotoImage(image = image)

        self.photo_image = img
        self.configure(image=img)
        if (self.show_camera): self.after(10,self.show_frame)
        else : self.cap.release()

    def __init__(self,root,capture,App):
        Label.__init__(self,root)
        self.cap = capture
        self.selected_points = []
        self.show_camera =True 
        self.bind('<Button-1>',App.selectPoint)
class PointsLabel(Label): 
    def __init__(self,root):
        Label.__init__(self,root)
        point1 = Point(self,"TR")
        point2 = Point(self,"TL")
        point3 = Point(self,"BR")
        point4 = Point(self,"BL")

        self.points = [point1,point2,point3,point4]

        point1.grid(row=0,sticky=W) 
        point2.grid(row=1,sticky=W)
        point3.grid(row=2,sticky=W)
        point4.grid(row=3,sticky=W)
    
    def addPoint(self,x,y): 
        for i,p in enumerate( self.points):
            if not p.selected: 
                p.select_point(x,y)
                if i == 3 :
                    self.endButton = Button(self,text="Continua",command=self.SelectPoints)
                    self.endButton.grid(sticky=S+W,row=5)
                break
    def SelectPoints(self): 
        return 0 


        


            
class Point(Frame):
    def unselect_yourself(self):
        self.selected = False
        label = "CORNER " + self.corner 
        self.label = label
        self.text.configure(text=label)
    def __init__(self,root,label):
        Frame.__init__(self,root)
        self.selected = False 

        textlabel = "CORNER " + label 
        self.label = textlabel
        self.corner = label
        self.button = Button(self,text = "X",command=self.unselect_yourself )
        self.text = Label(self,text = textlabel)

        self.text.grid(row=0,column=1,sticky=W)
        self.button.grid(row=0,column=0,sticky=W)

    def select_point(self,x,y): 
        self.selected = True
        label = self.label + ": " + str(x) + ", "+ str(y)
        self.label = label
        self.text.configure(text=label)



class app: 

    def selectPoint(self,event): 
        x,y = event.x,event.y
        self.selected_points.append([x,y])
        self.PointsLabel.addPoint(x,y)
    def __init__(self): 

        root = Tk()
        root.bind('<Escape>', lambda e: root.quit()) 
        self.root = root

        cap = cv2.VideoCapture(0)
        self.videoWindow = VideoLabel(root,cap,self)
        self.PointsLabel = PointsLabel(root)

        self.selected_points = []

        self.videoWindow.pack(anchor=NE,fill=Y,side=LEFT)
        self.PointsLabel.pack(anchor=NW,fill=X)
        
        self.videoWindow.after(10,self.videoWindow.show_frame)

def main():
    App = app()
    mainloop()


if __name__ == "__main__":
    main()