# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:17:40 2024

@author: pcb20
"""
import Board 
import numpy as np
import cv2 as cv
from itertools import product
from matplotlib import pyplot as plt
import App

class BoardDetector:
  
    def getImageToCheck(self,imName,corners):
        im = cv.imread(imName)
        points = Board.GeneratePoints(im)
        dstlattice = Board.getLattice(np.array([0,0]),np.array([1200,0]), np.array([0,1200]), np.array([1200,1200]))
        resPoints,avg = Board.findPoints(points, corners)
        M,_ = cv.findHomography(resPoints,dstlattice)
        dst = cv.warpPerspective(im, M, (1200,1200))
        self.homography = dst.copy()
        self.Name = imName
        for point1,point2 in zip(dstlattice,resPoints): 
            cv.circle(dst,(int(point1[0]),int(point1[1])),radius=0,color=(255,0,0),thickness=30)
            cv.circle(dst,(int(point2[0]),int(point2[1])),radius=0,color=(0,0,255),thickness=30)
        name = ".temp.jpg"
        cv.imwrite(name,dst)
        return name
    def SaveImages(self,pieces): 
        images = Board.splitquare(self.homography)
        splitedImages = {}
        for i in range(64): 
            if (pieces[i] != '0' ):
                if (pieces[i] not in splitedImages):
                    splitedImages[pieces[i]] = []
                splitedImages[pieces[i]].append(images[i])
        
        for Piece in splitedImages:
            if (not Piece.isupper()): 
                name = "w" + Piece.lower()
            else: 
                name = "b" + Piece.lower()
                
            for i,im in enumerate(splitedImages[Piece]):
                
                filename = "./data/"  + name + "/Croped"+ str(i) + self.Name.replace("/","") 
                cv.imwrite(filename, im  )
        