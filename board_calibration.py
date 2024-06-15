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

    def __init__(self,root,capture):
        Label.__init__(self,root)
        self.cap = capture
        self.selected_points = []
        self.show_camera =True 
        self.bind('<Button-1>',self.onRightclick)
        self.bind('<Button-3>',self.onLeftclick)
        
class app: 

    def __init__(self): 
        root = Tk()
        root.bind('<Escape>', lambda e: root.quit()) 
        cap = cv2.VideoCapture(0)
        self.mainWindow = VideoLabel(root,cap)
        self.mainWindow.grid(row=0)
        self.mainWindow.after(20,self.mainWindow.show_frame)

def main():
    App = app()
    mainloop()


if __name__ == "__main__":
    main()