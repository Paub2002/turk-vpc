# -*- coding: utf-8 -*-
"""
Created on Sun May 19 13:23:08 2024

@author: pcb20
"""
import numpy as np
import chess 
import chess.svg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap



class ui_MainWindow(QWidget):
    def setupUi(self,MainWindow,image):
        
     super().__init__()

     
     MainWindow.setObjectName("MainWindow")
     MainWindow.resize(1500, 1000)
     
     self.centralwidget = QWidget(MainWindow)
     self.centralwidget.setObjectName("centralwidget")
     
     self.photo = QLabel(self.centralwidget)
     self.photo.setGeometry(QtCore.QRect(0, 0, 1000, 1000))     # loading image
     self.pixmap = QPixmap(image)

     # adding image to label
     self.photo.setPixmap(self.pixmap.scaledToWidth(1000))

     # Optional, resize label to image size
     
     self.setGeometry(0,0,1000, self.pixmap.scaledToWidth(1000).height())
     self.photo.installEventFilter(self)
     
     self.selectedPoints = []
     MainWindow.setCentralWidget(self.centralwidget)

     # show all the widgets
     

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                
                mapedPoint = self.photo.mapFromParent(event.pos())
                x,y =  mapedPoint.x(), mapedPoint.y() 
                xScale = self.pixmap.width() / 1000
                voff =( 1000 - self.pixmap.scaledToWidth(1000).height() )/ 2 
                x,y = x* xScale,  y * xScale - voff
                self.selectedPoints.append(np.array([x,y ]))
                if (len(self.selectedPoints) >= 4): 
                    qApp.exit(1)

        return super().eventFilter(obj, event)
  

def LoadSelector(image):
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = ui_MainWindow()
    ui.setupUi(MainWindow,image)
    MainWindow.show()
    app.exec()
    app.exit()
        
    return ui.selectedPoints