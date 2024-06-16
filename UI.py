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
        self.selected_points = []
        self.labels = ['TR','TL','DR','DL']
    def addPoint(self,x,y):
        selected = 0
        if selected < 3:
            point = Point(self,self.labels[selected],x,y)
            point.pack()


            
class Point(Frame):
    def unselect_yourself(self):
        self.grid_forget()
        self.selected = False
    def __init__(self,root,label,x,y):
        Frame.__init__(self,root)
        self.selected = True

        label = "CORNER " + label + ": " + str(x) + ", " + str(y) 
        self.button = Button(self,text = "X",command=self.unselect_yourself )
        self.text = Label(self,text = label)

        self.text.pack(side=RIGHT)
        self.button.pack(side=LEFT)



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