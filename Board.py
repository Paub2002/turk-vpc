# -*- coding: utf-8 -*-
"""
Created on Sun May 19 15:55:37 2024

@author: pcb20

"""
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def getLatticeLines(TL,TR,DL,DR):
    # Generate lattice lines for the debug display
    # Get the points : 
    T = TR - TL
    tu = T/ 8
    D = DR - DL
    du = D / 8
    R = DR - TR
    ru = R / 8
    L = DL - TL 
    lu = L / 8
    
    newT = [TL]
    newD = [DL]
    newR = [TR]
    newL = [TL]
    
    for n in range(8): 
        newT.append( TL + (n + 1) * tu )
        newD.append( DL + (n + 1) * du )
        newR.append( TR + (n + 1) * ru )
        newL.append( TL + (n + 1) * lu )
    
    newT =np.array(newT)
    newD =np.array(newD)
    newR =np.array(newR) 
    newL =np.array(newL) 
    v_lines = np.concatenate([newT,newD],axis=1)
    h_lines = np.concatenate([newR,newL],axis=1)

    return np.concatenate([v_lines,h_lines]).astype(np.uint8)

def openResidue(im):
    gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    
    kernel = np.array([[0, 0, 0 ,0, 0, 0, 0], 
                       [0, 1, 1, 1, 1, 1, 0], 
                       [0, 1, 1, 1, 1, 1, 0], 
                       [0, 1, 1, 1, 1, 1, 0], 
                       [0, 1, 1, 1, 1, 1, 0], 
                       [0, 1, 1, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0]])
    
    return gray - cv.filter2D(src=gray,ddepth=-1,kernel=kernel)

def splitquare(im): 
    n = 8 
    size = im.shape[0]//8
    splits = []
    for i in range(n): 
        for j in range(n): 
            splits.append(im[ i * size : (i + 1) * size , j * size  : (j + 1 ) * size ])
    return np.array(splits)


def AutoGetHomography(captura): 
    #Frame Reading
    frame = cv.cvtColor(captura.read()[1],cv.COLOR_BGR2RGB)
    # we define the colors 
    red_low  = np.array([ 150, 70,  70 ])
    red_upp  = np.array([ 255, 150, 150 ])
    blue_low = np.array([ 80, 200, 200 ])
    blue_upp = np.array([ 150, 255, 255 ])

    # Search for biggest blobs 
    hX, hY = find2ColorPoints(frame,red_low,red_upp)
    aX, aY = find2ColorPoints(frame,blue_low,blue_upp)

    #Center calculation 
    centh = hY +     (hX - hY)       / 2 
    centa = aY +     (aX - aY)       / 2 

    cent  = centh +  (centa - centh) / 2 
    cent = cent.astype(np.uint32)

    #Rotation Correction 
    supposedDiff = True
    Ydiff = np.abs(aY - aX)
    if Ydiff[0] < Ydiff[1] :
        supposedDiff = False 
    Xdiff = np.abs(hX - aX) 
    if Xdiff[0 if supposedDiff else  1   ] > Xdiff[ 1 if supposedDiff else 0]:
        tmp = aY
        aY = aX
        aX = tmp

    #Homography
    coords = np.array([hX,aX,hY,aY])
    dst = np.array([[0,512],[512,512],[0,0],[512,0]])

    M,_ = cv.findHomography(coords,dst)
    dst = cv.warpPerspective(frame, M, (512,512))

    splits = splitquare(dst)
    if correctSide (splits[31],splits[39]):
        coords = np.array([hY,aY,hX,aX])
        dst = np.array([[0,512],[512,512],[0,0],[512,0]])
        M,_ = cv.findHomography(coords,dst)
    return M
def correctSide(wSplit, bSplit): 
    return wSplit.mean() < bSplit.mean()

def main():

    #Frame Reading

    captura = cv.VideoCapture(1)
    frame = cv.cvtColor(captura.read()[1],cv.COLOR_BGR2RGB)
    # frame = cv.cvtColor(cv.imread('no-cam.png'),cv.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.show()
    # showHist(frame)


    # we define the colors 
    red_low  = np.array([ 150,  90,  90 ])
    red_upp  = np.array([ 255, 150, 150 ])
    blue_low = np.array([ 80, 200, 200 ])
    blue_upp = np.array([ 150, 255, 255 ])

    # Search for biggest blobs 
    hX, hY = find2ColorPoints(frame,red_low,red_upp)
    aX, aY = find2ColorPoints(frame,blue_low,blue_upp)

    #Center calculation 
    centh = hY +     (hX - hY)       / 2 
    centa = aY +     (aX - aY)       / 2 

    cent  = centh +  (centa - centh) / 2 
    cent = cent.astype(np.uint32)

    #Rotation Correction 
    supposedDiff = True
    Ydiff = np.abs(aY - aX)
    if Ydiff[0] < Ydiff[1] :
        supposedDiff = False 
    Xdiff = np.abs(hX - aX) 
    if Xdiff[0 if supposedDiff else  1   ] > Xdiff[ 1 if supposedDiff else 0]:
        tmp = aY
        aY = aX
        aX = tmp

    #Homography
    coords = np.array([hX,aX,hY,aY])
    dst = np.array([[0,512],[512,512],[0,0],[512,0]])

    M,_ = cv.findHomography(coords,dst)
    dst = cv.warpPerspective(frame, M, (512,512))

    #DEBUG Display
    cv.circle(frame,hX,2,(0,0,255),-1)
    cv.circle(frame,hY,2,(0,0,255),-1)
    cv.circle(frame,aX,2,(0,0,255),-1)
    cv.circle(frame,aY,2,(0,0,255),-1)
    cv.circle(frame,cent,10, (0,100,255),-1)
    cv.circle(frame,centh.astype(np.uint32),10,(0,100,255),-1)
    cv.circle(frame,centa.astype(np.uint32),10,(0,100,255),-1)
   
    plt.imshow(frame)
    plt.show()
    plt.imshow(dst)
    plt.show()

def find2ColorPoints(frame,low,up): 

    mask = cv.inRange(frame,low,up)
    # plt.imshow(mask)
    # plt.show()
    contours,_= cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    areas = []
    for c in contours : areas.append(cv.contourArea(c))
    bigest = np.argsort(areas)[::-1]

    try :
        c1 = contours[bigest[0]]
        M1 = cv.moments(c1)
        center1 = np.array([int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"])])

        c2 = contours[bigest[1]]
        M2 = cv.moments(c2)
        center2 = np.array([int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"])])

        return center1,center2
    except (ZeroDivisionError): 
        return []
    
def showHist(image):
    # Extract 2-D arrays of the RGB channels: red, green, blue
    red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]

    # Flatten the 2-D arrays of the RGB channels into 1-D
    red_pixels = red.flatten()
    green_pixels = green.flatten()
    blue_pixels = blue.flatten()
    plt.figure(figsize=(9,9))
    plt.hist(red_pixels, bins=256, density=False, color='red', alpha=0.5)
    plt.hist(green_pixels, bins=256, density=False, color='green', alpha=0.4)
    plt.hist(blue_pixels, bins=256, density=False, color='blue', alpha=0.3)

    # set labels and ticks

    # Cosmetics
    plt.title('Histograms from color image')
    plt.ylabel('Counts')
    plt.xlabel('Intensity')

    # Display the plot
    plt.show()
if __name__ == "__main__":
    main()