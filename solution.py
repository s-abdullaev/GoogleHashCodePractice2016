# -*- coding: utf-8 -*-

import numpy as np
import re
from Drawer import *

img=None
n=0; m=0

#reading input
with open("right_angle.in", "r") as f:
    s=f.readline()
    s=s.split(" ")
    n=int(s[0])
    m=int(s[1])
    img=np.zeros([n,m], dtype=int)
    for i,l in enumerate(f):
        l=l.replace('\n','')
        img[i,:]=[0 if el=="." else 1 for el in l]

#manager which draws and keeps track of commands
drwMgr=DrawManager(img)

#draws horizontal lines
def drawForRowBlock(subImg, startRow):
    #number of rows
    r=int(np.size(subImg, axis=0))
    
    #draw horizontal lines
    for i in range(r):
        lines=findLines(subImg[i,:])
        for l in lines:
            start=(startRow+i, l.start())
            end=(startRow+i, l.end())
            cmd=LineCommand(start, end)
            drwMgr.line(cmd)

#draws vertical lines
def drawForColumnBlock(subImg, startCol):
    #number of columns
    r=int(np.size(subImg, axis=1))

    #draw vertical lines
    for i in range(r):
        lines=findLines(subImg[:,i])
        for l in lines:
            start=(l.start(), startCol+i)
            end=(l.end(), startCol+i)
            cmd=LineCommand(start, end)
            drwMgr.line(cmd)

#draws boxes for given block
def drawForSlidingBox(subImg, startRow, startCol):
    #number of rows
    r=int(np.size(subImg, axis=0))
        
    #draw boxes
    rowSum=np.sum(subImg, axis=0).tolist()
    boxSum=[r]*r
    if rowSum==boxSum:
        center=(startRow+r-r/2-1, startCol+r-r/2-1)
        S=(r-1)/2
        cmd=SquareCommand(center, S)
        drwMgr.square(cmd)

#finds lines
def findLines(source):
    a="".join([str(el) for el in source])
    return [m for m in re.finditer("(1+)", a)]

#draw for every horizontal block
for i in range(0,n):
    drawForRowBlock(img[i:i+1,:],i)
        
#draw for every vertical block
for i in range(0,m):
    drawForColumnBlock(img[:,i:i+1],i)

#draw for every size of sliding box
maxBoxSize=min(m,n)
for k in range(0, maxBoxSize, 2):
    for i in range(0,n-k):
        for j in range(0, m-k):
            drawForSlidingBox(img[i:i+k+1,j:j+k+1], i, j)

print drwMgr.drwer.img

#remove redundant commands
drwMgr.optimizeCmds()