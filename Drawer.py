# -*- coding: utf-8 -*-

import numpy as np
import random
import string
from gurobipy import *

class Command(object):
    def __init__(self):
        self.label=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

class SquareCommand(Command):
    def __init__(self, center, S):
        super(self.__class__, self).__init__()
        self.center=center
        self.S=S
        
    def getString(self):
        return "PAINT_SQUARE %d %d %d" % (self.center[0], self.center[1], self.S)

class LineCommand(Command):
    def __init__(self, start, end):
        super(self.__class__, self).__init__()
        self.start=start
        self.end=end
        
    def getString(self):
        return "PAINT_LINE %d %d %d %d" % (self.start[0], self.start[1], self.end[0], self.end[1])
    
class EraseCommand(Command):
    def __init__(self, spot):
        super(self.__class__, self).__init__()
        self.spot=spot
    
    def getString(self):
        return "ERASE_CELL %d %d" % (self.spot[0], spot.spot[1])


class DrawManager(object):
    def __init__(self, img):
        self.n=np.size(img, axis=0)
        self.m=np.size(img, axis=1)
        self.cmder=Commander([self.n,self.m])
        self.drwer=Drawer([self.n,self.m])
    
    def square(self, cmdObj):
        self.drwer.square(cmdObj)
        self.cmder.square(cmdObj)
        
    def line(self, cmdObj):
        self.drwer.line(cmdObj)
        self.cmder.line(cmdObj)
        
    def erase(self, cmdObj):
        self.drwer.erase(cmdObj)
        self.cmder.erase(cmdObj)
    
    def optimizeCmds(self):
        m=Model("hittingSet")
        
        #variables, all commands used
        v={}
        for c in self.cmder.cmds:
            v[c.label]=m.addVar(vtype=GRB.BINARY, name=c.label)
        
        m.update()
        
        #minimize the number of commands
        m.setObjective(quicksum(v.values()), GRB.MINIMIZE)
        
        #constraints
        f=np.vectorize(lambda x: v[x])
        setList=[list(s.tolist()) for s in np.nditer(self.cmder.cmdMtx, flags=["refs_ok"]) if s]
        sets=[f(l) for l in setList]
        
        for i, s in enumerate(sets):
            m.addConstr(quicksum(s)>=1,'cons%d' % i)
        
        m.optimize()
        #m.printAttr('X')
        for c in self.cmder.cmds:
            if v[c.label].X==1:
                print c.getString()
        

class Commander(object):
    def __init__(self, shape):
        self.cmds=[]
        self.n=shape[0]
        self.m=shape[1]
        self.cmdMtx=np.empty([shape[0], shape[1]], dtype=set)
        self.cmdMtx.fill(set())
    
    def square(self, cmdObj):
        for i in range(cmdObj.center[0]-cmdObj.S, cmdObj.center[0]+cmdObj.S+1):
            if i<0 or i>=self.n: continue
            for j in range(cmdObj.center[1]-cmdObj.S, cmdObj.center[1]+cmdObj.S+1):
                if j<0 or j>=self.m: continue
                self.cmdMtx[i,j]=set.union(self.cmdMtx[i,j], [cmdObj.label])
        self.cmds.append(cmdObj)
        
    def line(self, cmdObj):
        if cmdObj.start[0]==cmdObj.end[0]:
            cmdLabels=self.cmdMtx[cmdObj.start[0],cmdObj.start[1]:cmdObj.end[1]]
            self.cmdMtx[cmdObj.start[0],cmdObj.start[1]:cmdObj.end[1]]=[set.union(el, [cmdObj.label]) for el in cmdLabels]
        elif cmdObj.start[1]==cmdObj.end[1]:
            cmdLabels=self.cmdMtx[cmdObj.start[0]:cmdObj.end[0],cmdObj.start[1]]
            self.cmdMtx[cmdObj.start[0]:cmdObj.end[0],cmdObj.start[1]]=[set.union(el, [cmdObj.label]) for el in cmdLabels]
        self.cmds.append(cmdObj)
        
    def erase(self, cmdObj):
        self.cmds.append(cmdObj)
        
class Drawer(object):
    def __init__(self, shape):
        self.n=shape[0]
        self.m=shape[1]
        self.img=np.zeros([self.n, self.m], dtype=int)
        
    def square(self, cmdObj):
        for i in range(cmdObj.center[0]-cmdObj.S, cmdObj.center[0]+cmdObj.S+1):
            if i<0 or i>=self.n: continue
            for j in range(cmdObj.center[1]-cmdObj.S, cmdObj.center[1]+cmdObj.S+1):
                if j<0 or j>=self.m: continue
                self.img[i, j]=1

    def line(self, cmdObj):
        if cmdObj.start[0]==cmdObj.end[0]:
            self.img[cmdObj.start[0],cmdObj.start[1]:cmdObj.end[1]]=1
        elif cmdObj.start[1]==cmdObj.end[1]:
            self.img[cmdObj.start[0]:cmdObj.end[0],cmdObj.start[1]]=1
        
    def erase(self, cmdObj):
        self.img[cmdObj.spot[0],cmdObj.spot[1]]=0
    
    def readCmd(cmdStr):
        pass