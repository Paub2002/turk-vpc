# -*- coding: utf-8 -*-
"""
Created on Sun May 19 15:55:37 2024

@author: pcb20

"""
import numpy as np
import cv2 as cv
from itertools import product
from matplotlib import pyplot as plt

## IMAGE TREATMENT FUNCTIONS ====================================================================================================================
##===============================================================================================================================================
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

def canny(im): 
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = openResidue(im)
    gray = clahe.apply(gray)
   
    edge = cv.Canny(gray,threshold1= 100, threshold2=500,apertureSize=3)
    return edge
def splitquare(im): 
    size = 150 
    n = 8 
    splits = []
    for i in range(n): 
        for j in range(n): 
            splits.append(im[ i * size : (i + 1) * size , j * size  : (j + 1 ) * size ])
    return splits
def getCornerSets(points,corners,im):
    
    iters = 7 # return set size = iters ^ 4 
    corner_candidates = [[],[],[],[]]
    points2 = points.copy()
    
    for it in range(iters): 
        
        hull = cv.convexHull(points2)[:,0,:]
        hullmask = np.ones((points2.shape[0]), dtype = bool)
        
        for h in hull: 
            a = np.where(points2[:] == h)[0][0]
            hullmask[a] = False
        for n,(x,y) in enumerate(corners): 
            dists = np.sqrt((x - hull[:,0]) ** 2 + (y - hull[:,1]) ** 2 )
            m = dists.argmin()
            corner_candidates[n].append(hull[m])
               
        points2 = points2[hullmask]
        
    corner1_candidates = np.array(corner_candidates[0])
    corner2_candidates = np.array(corner_candidates[1])
    corner3_candidates = np.array(corner_candidates[2])
    corner4_candidates = np.array(corner_candidates[3])
    
    result = list(product(corner1_candidates,corner2_candidates,corner3_candidates,corner4_candidates))
    return np.array(result)
def printLines(im,linesx,linesy,pointsa,pointsb):
    imx = np.array(im)
    imy = np.array(im)
    for x,y in pointsa:
        if(x == x and y == y):
            cv.circle(imx,(int(x),int(y)),radius=0,color=(255,0,0),thickness=30)
    for x,y in pointsb:
        if(x == x and y == y):
            cv.circle(imx,(int(x),int(y)),radius=0,color=(255,0,255),thickness=30)
    for a,b in linesx: 
        if(a == a and b == b): 
           x0 = 0
           y0 = int(a)
           x1 = 2048 
           y1 = int(a + 2048 * b )
           cv.line(imx,(x0,y0),(x1,y1),(0,255,0),2)
           cv.line(imx,(x0,y0),(x1,y1),(0,255,0),2)
    
    for a,b in linesy: 
        if(a == a and b == b): 
           x0 = 0
           y0 = int(a)
           x1 = 2048 
           y1 = int(a + 2048 * b )
           cv.line(imy,(x0,y0),(x1,y1),(255,255,0),2)
           cv.line(imx,(x0,y0),(x1,y1),(255,255,0),2)


        
    plt.imshow(imx)
    plt.show()

def getHomography(points,im,corners):
    dstlattice = getLattice(np.array([0,0]),np.array([1200,0]), np.array([0,1200]), np.array([1200,1200]))
    if (corners == []): 
        corners = np.array([[0,0],[im.shape[1],0],[0,im.shape[0]],[im.shape[1],im.shape[0]]])
        averages = []
        distances = []
        DetectedPoints = []
        candidates = getCornerSets(points,corners,im)
        for candidat in candidates:
            dstPoints,avg = findPoints(points, candidat)
            DetectedPoints.append(dstPoints)
            averages.append(avg)
            M,_ = cv.findHomography(dstPoints,dstlattice)
            
            dstres = []
            
            for x,y in dstPoints: 
                p = np.array((x,y,1)).reshape((3,1))
                temp_p = M.dot(p)
                sum = np.sum(temp_p ,1)
                px = int(round(sum[0]/sum[2]))
                py = int(round(sum[1]/sum[2]))
                dstres.append([px,py])
                
            dstres = np.array(dstres)
            distancesResult = np.sqrt((dstres[:,0] - dstlattice[:,0]) **2 + (dstres[:,1] - dstlattice[:,1]) **2  ) 
            distances.append(distancesResult.sum()* 2 /  distancesResult.shape[0])
            
        averages = np.array(averages)
        distances = np.array(distances)
        scores=  averages + distances
        m = scores.argmin()
        resPoints = DetectedPoints[m]
    else: 
        resPoints,avg = findPoints(points, corners)
        
    M,_ = cv.findHomography(resPoints,dstlattice)
    dst = cv.warpPerspective(im, M, (1200,1200))
    printLines(im, [],[], resPoints, [])
    
    return dst
## SEGMENT TREATMENT FUNCTIONS ==================================================================================================================
##===============================================================================================================================================
def edge2segment(edge): 
    seg = cv.HoughLinesP(edge,1,np.pi/180,100,minLineLength = 10)
    seg = seg [:,0,:]
    
    theta = abs(np.arctan((seg[:,3] - seg[:,1]) / (seg[:,2] - seg[:,0]) ))
    mask = theta > theta.mean()
    notmask = ~mask
    
    segx = seg[mask]
    segy = seg[notmask]
    return segx,segy

def segments2points(segments):
   
    sizes =  np.sqrt ( (segments[:,1] - segments[:,3]) ** 2 + (segments[:,0] - segments[:,2]) ** 2 )
    v = (segments[:,2] - segments[:,0] , segments[:,3] - segments[:,1])
    n = v / sizes
    points  = []
    for i,size in enumerate (sizes.astype(np.uint8)):
        segment = []
        segment.append([segments[i][0]  ,segments[i][1]])
        for r in range(size):
            x = segments[i][0] + n[0][i] * (r + 1 )
            y = segments[i][1]+ n[1][i] * (r + 1 )
            segment.append([x,y])
        segment = np.array(segment)
        points.append(segment)
    return points
def groupCategories(categories, points): 
    
    nCategories = categories.max()
    
    groupedPoints =  {}
    
    for category in range(1,nCategories+1):
        
        catmask = (categories == category)
        xpoints = []
        ypoints = []

        isfirst = True

        for i, is_in in enumerate(catmask):
            if (is_in):
                if(isfirst):
                    xpoints = points[i][:, 0]
                    ypoints = points[i][:, 1]
                    isfirst = False
                else:
                    xa = points[i][:, 0]
                    ya = points[i][:, 1]
                    xpoints = np.concatenate((xpoints, xa))
                    ypoints = np.concatenate((ypoints, ya))

        groupedPoints[category] = (xpoints, ypoints)

    return groupedPoints
def categorizeSegments(segments):
        w = (np.pi / 2) /  np.power(2048 * 1536 , 1/4)
        t = w * 0.5
        theta = np.arctan((segments[:,3] - segments[:,1]) / (segments[:,2] - segments[:,0]) )
        sth = np.sin(theta)
        cth = np.cos(theta)
        sizes  = np.sqrt ( (segments[:,1] - segments[:,3]) ** 2 + (segments[:,0] - segments[:,2]) ** 2 )

        distances = np.zeros ( (segments.shape[0],segments.shape[0],2))

        for i , line in enumerate(segments): 
            distances[i,:,0] = abs ( cth * ( segments[:,1] - line[1] ) - sth * (segments[:,0] - line[0]))
            distances[i,:,1] = abs ( cth * ( segments[:,1] - line[3] ) - sth * (segments[:,0] - line[2]))

        merges = np.zeros ( (segments.shape[0]) )
        categories = 1
        for i in range(segments.shape[0]):
            if (merges[i] == 0):
                merges[i] = categories 
                for j in range(i,segments.shape[0]):
                    if (merges[j] == 0): 
                        gamma = (distances[i,j,0] + distances[i,j,1] +distances[j,i,0] +distances[j,i,1]) / 4
                        variation = ( sizes[i] + sizes[j] ) * t 
                        if (sizes[i]/gamma > variation and sizes[j] / gamma > variation): 
                            merges[j] = categories
                categories += 1
        
        return np.array(merges,dtype=np.uint8)
## LINE TREATMENT FUNCTIONS =====================================================================================================================
##===============================================================================================================================================
def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)


    sub = n * xbar**2
    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X])
    b = 0
    if (denum != sub): 
        denum = denum - sub
        b = numer / denum
    a = ybar - b * xbar

    return a, b
def getLines(groupedPoints):
    lines = []
    
    aArr = []
    bArr = []
    for X,Y in groupedPoints.values(): 
        a,b =  best_fit(X, Y)
        aArr.append(a)
        bArr.append(b)
        lines.append((a,b))
    A = np.array(aArr)
    B = np.array(bArr)
    lines = np.array(lines)
    A = np.abs(A)
    B = np.abs(B)
    return lines

## INTERSECTIONS 

def lineIntersection(a1,b1,a2,b2):
    x = (a2 - a1) / (b1 - b2)
    y = a1 + b1 * x 
    return x,y
def getIntersections(xl,yl):
    points = []
    for x in xl: 
        for y in yl: 
            a,b = lineIntersection(x[0],x[1],y[0],y[1]) 
            if (a == a and  b == b): 
                points.append((a,b))
                
    points = np.array(points).astype(np.float32)
    negmask = np.logical_or(points[:,0] < 0,  points[:,1]  < 0)
    negmask = ~negmask
    points = points[negmask]
    return points
def findPoints(points,boardCorners):
        ### A partir de aqui se queda en la funcion
        newPoints = getLattice(boardCorners[0],boardCorners[1],boardCorners[2],boardCorners[3])
        
        dstPoints = []
        distances = []
        for point in newPoints: 
            pointV =  point - points
            dists = np.sqrt(pointV[:,0] ** 2 + pointV[:,1] ** 2)
            dstPoints.append(points[dists.argmin()])
            distances.append(dists.min())
        avg = np.array(distances).mean()
              
        return np.array(dstPoints),avg
def getLatticeLines(TL,TR,DL,DR):
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

def getLattice(TL,TR,DL,DR):
    # we create the frame 
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
    
    #Calculate all intersections
    A1 = newD[:,1] - newT[:,1]
    B1 = newT[:,0] - newD[:,0]
    C1 = A1 * newT[:,0] + B1 * newT[:,1]
    
    A2 = newR[:,1] - newL[:,1]
    B2 = newL[:,0] - newR[:,0]
    C2 = A2 * newL[:,0] + B2 * newL[:,1]
    xarr = []
    yarr = []
    for a,b,c in zip(A1,B1,C1): 
        D = a * B2 - A2 * b
        
        x = (B2*c - b*C2) / D
        y = (a*C2 - A2*c) / D
        
        maskd = D != 0
        
        x = x[maskd]
        y = y[maskd]
        xarr += x.tolist()
        yarr += y.tolist()
     
    points = np.zeros((len(xarr),2))
    
    xarr = np.array(xarr)
    yarr = np.array(yarr)
    points[:,0] = xarr
    points[:,1] = yarr
    
    return points
def SplitBoard(im):
    
    
    points = GeneratePoints(im)
    
    board = getHomography(points,im,[])
    
    splitedBoard = splitquare(board)
    
    return splitedBoard
def getImageToCheck(imName,corners):
    im = cv.imread(imName)
    points = GeneratePoints(im)
    dstlattice = getLattice(np.array([0,0]),np.array([1200,0]), np.array([0,1200]), np.array([1200,1200]))
    resPoints,avg = findPoints(points, corners)
    M,_ = cv.findHomography(resPoints,dstlattice)
    dst = cv.warpPerspective(im, M, (1200,1200))
    for point1,point2 in zip(dstlattice,resPoints): 
        cv.circle(dst,(int(point1[0]),int(point1[1])),radius=0,color=(255,0,0),thickness=30)
        cv.circle(dst,(int(point2[0]),int(point2[1])),radius=0,color=(0,0,255),thickness=30)

    name = ".temp.jpg"
    cv.imwrite(name,dst)
    return name

def GeneratePoints(im):
    # Initial treatment and canny edge
   edge = canny(im)
   
   segx,segy = edge2segment(edge)
   
   # Convert the segments to a sets of points
   
   pointsx = segments2points(segx)
   pointsy = segments2points(segy)
   
   # Categorize segments
   categoriesx = categorizeSegments(segx)
   categoriesy = categorizeSegments(segy)
   
   # Group point categories
   groupedPointsx = groupCategories(categoriesx, pointsx)
   groupedPointsy = groupCategories(categoriesy, pointsy)
   
   # Get lines
   linesx = getLines(groupedPointsx)
   linesy = getLines(groupedPointsy)

   
   points = getIntersections(linesx, linesy)
   
   pointmask = np.logical_or(points[:,0] > im.shape[1],  points[:,1] > im.shape[0])
   pointmask = ~pointmask
   points = points[pointmask]
   return points