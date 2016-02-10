# -*- coding: utf-8 -*-

import numpy as np
import re
from Drawer import *

img=None
n=0; m=0

#reading input
with open("learn_and_teach.in", "r") as f:
    s=f.readline()
    s=s.split(" ")
    n=int(s[0])
    m=int(s[1])
    img=np.zeros([n,m], dtype=int)
    for i,l in enumerate(f):
        l=l.replace('\n','')
        img[i,:]=[0 if el=="." else 1 for el in l]


drwMgr=DrawManager(img)

#optimal commands cost per init row i, per block size k
#cmdCosts=np.zeros([n, n/2])
#cmdCosts.fill(np.Inf)

#finds optimal drawing for given block
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

def findLines(source):
    a="".join([str(el) for el in source])
    return [m for m in re.finditer("(1+)", a)]
    
def hasSequence(source, seq):
    a="".join([str(el) for el in source])
    b="".join([str(el) for el in seq])
    if b in a:
        return [m.start() for m in re.finditer(b, a)]
    return []

#draw for every horizontal block
for i in range(0,n):
    drawForRowBlock(img[i:i+1,:],i)
        
#draw for every vertical block
for i in range(0,m):
    drawForColumnBlock(img[:,i:i+1],i)

#draw for every vertical block
maxBoxSize=min(m,n)
for k in range(0, maxBoxSize):
    for i in range(0,n-k):
        for j in range(0, m-k):
            drawForSlidingBox(img[i:i+k+1,j:j+k+1], i, j)

print drwMgr.drwer.img

drwMgr.optimizeCmds()
        
