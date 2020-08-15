import numpy as np
import utility as vu
from view import *
from tkinter import *
from datetime import datetime

class Controller():
    def __init__(self):
        self.view = None

        self.numInput = 0
        self.numOutput = 0
        self.numOfHLayers = []
        self.listBiais = []
        self.listFlatBiais = []
        self.listWeight = []
        self.listFlatWeight = []

    # set link to view
    def setView(self, vie):
        self.view = vie

    def randomBiais(self, listvn):
        for i in range(1, listvn.__len__()): # walk through layers
            currentNodeQty = listvn[i].__len__()
            npBiais = np.random.rand(currentNodeQty) # np to generate a list of random numbers
            self.listBiais.append(npBiais)
            self.flattenListBiais(self.listBiais) # put in a flattened list
            self.view.updateBiais(self.listFlatBiais) # update view
    
    def flattenListBiais(self, lb):
        self.listFlatBiais.clear()
        for layer in lb:
            for i in layer:
                self.listFlatBiais.append(i) # walk through 2d list and put into id lis

    def randomWeight(self, listvn):
        for i in range(0, listvn.__len__() - 1): # layers
            currentNodeQty = listvn[i].__len__() # get node number in one layer
            nextNodeQty = listvn[i + 1].__len__() # get node number in next layer
            npMatrixWeight = np.random.rand(currentNodeQty, nextNodeQty) # generate weights for each node, this is a 2D list
            self.listWeight.append(npMatrixWeight) # save it inside a list by layers
            self.flattenListWeight(self.listWeight) # flat
            self.view.updateWeight(self.listFlatWeight) # view to update weights on canvas

    def flattenListWeight(self, lw):
        self.listFlatWeight.clear() # this is 3D list
        for layer in lw:
            for i in layer:
                for j in i:
                    self.listFlatWeight.append(j)
