import numpy as np
import utility as vu
from view import *
from tkinter import *
from datetime import datetime
from vNode import VNode

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
        self.flagTrainFeatureLoad = False
        self.flagTrainLabelLoad = False
        self.trainFeatureSet = [] # entrer x
        self.trainLabelSet = [] # sortie x
        self.listAhiddenLayer = [] # node value after sigmoid function
        self.listZhiddenLayer = [] # node sum value before sigmoid function

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

    def loadTrainFeature(self, path):
        if len(path) > 0:
            self.outputTrainFilePath = path
            self.view.statusbar["text"] = "Loading .... please wait for numbers show in output nodes"
            list = [] # temperary store of training feature data as a list
            f = open(path, "r")
            lines = f.read().split('\n') # get lines
            f.close() # close file
            # load into list
            for line in lines:
                if line != "":
                    row = self.strToNp(line.split(",")) # returns a list of np float number
                    list.append(row) # 2D list
            self.trainFeatureSet.clear()
            self.trainFeatureSet = list
            # check input node length, if different update to match train feature data
            if self.trainFeatureSet[0].__len__() != self.view.listInputNode.__len__():
                self.view.combo1input.set(self.trainFeatureSet[0].__len__()) # set input node qty
                self.view.createNodes() # recreate network
            self.setInputValue(self.trainFeatureSet)
            self.flagTrainFeatureLoad = True
            self.view.statusbar["text"] = "training Feature set loaded"
        else: # no path
            self.flagTrainFeatureLoad = False
            self.trainFeatureSet.clear()
            self.view.clearInputValue()
            self.view.statusbar["text"] = "training Feature set failed"

    def setInputValue(self, setV):
        for i in range(setV[0].__len__()):
            self.view.listInputNode[i].updateValue(setV[0][i])

    def strToNp(self, list):
        newList = []
        for i in list:
            newList.append(np.float64(i))
        return newList

    def loadTrainLabel(self, path):
        if len(path) > 0:
            self.outputTrainFilePath=path
            self.view.statusbar["text"] = "Loading..... please wait for numbers shown in output nodes"
            list=[]
            f=open(path,"r")
            lines=f.read().split('\n')
            f.close()
            for l in lines:
                if l != "":
                    # vu.tprint(l)
                    row=self.strToNp(l.split(","))
                    list.append(row)
            self.trainLabelSet.clear()
            self.trainLabelSet = list
            # vu.tprint(self.trainLabelSet)
            # check output node length
            if self.trainLabelSet[0].__len__() != self.view.listOutputNode.__len__():
                self.view.combo5output.set(self.trainLabelSet[0].__len__())
                self.view.createNodes()
                # re-set input node value
                for i in range(self.trainFeatureSet[0].__len__()):
                    self.view.listInputNode[i].updateValue(self.trainFeatureSet[0][i])

            # set output node value
            for i in range(self.trainLabelSet[0].__len__()):
                self.view.listOutputNode[i].updateValue(self.trainLabelSet[0][i])
            self.flagTrainLabelLoad=True
            self.view.statusbar["text"] = "Training label set loaded"
        else:
            # load failed clean output
            self.flagTrainLabelLoad=False
            self.trainLabelSet.clear()
            self.view.clearOutputValue()
            self.view.statusbar["text"] = "Training Load set loading failed"

    def clear(self):
        self.numInput = 0
        self.numOutput = 0
        self.numOfHLayers.clear()
        self.listWeight.clear()
        self.listFlatWeight.clear()
        self.listFlatBiais.clear()
        self.listBiais.clear()

    def startTrain(self):
        startTime = datetime.now() # measure training time
        self.view.text31ErrorTxtbox.delete('1.0', END)  # clean view error index box | 1.0 : commencer à partir du 1er char & 
                                                        # 2è arg définit le dernier caractère à supprimer qui est la fin
        # get how many cycles to refresh training process
        totalCheck = int(self.view.combo7epoch.get()) / (int(self.view.combo8refreshrate.get()))
        i = 1
        for epoch in range(int(self.view.combo7epoch.get())):
            self.trainLoop() # actural network calculation, forward feeling and back propagation
            if epoch % (int(self.view.combo8refreshrate.get())) == 0:  #    if time to refresh network in view
                loss = np.sum(-np.array(self.trainLabelSet) * np.log(self.ao)) # calculate lost function
                lossTxt = str(loss) + "\n" # appendloss
                self.view.text31ErrorTxtbox.insert(INSERT, lossTxt) # insert text on gui
                self.view.text31ErrorTxtbox.update() # update text box
                # show progress percentage
                p = i / totalCheck * 100
                runTime = datetime.now() - startTime
                self.view.statusbar["text"] = ("Training in progress: " + str(int(p)) + "%" + "     Duration:  " + str(runTime))
                i += 1
                # update weights in view
                self.flattenListBiais(self.listBiais)
                self.view.updateBiais(self.listFlatBiais)
        runTime = datetime.now() - startTime
        self.view.statusbar["text"] = "Training Completed. Duration: " + str(runTime)

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def softmax(self, A):
        expA = np.exp(A)
        return expA / expA.sum(axis=1, keepdims=True)

    def trainLoop(self):
        # feed forward
        previous_set = self.trainFeatureSet #initial previouse set
        self.listAhiddenLayer.clear() # list fonct° sigmoïde
        self.listZhiddenLayer.clear() # list fonct° combinaison
        for i in range (self.listWeight.__len__()): # for each layerr
            if i!=self.listWeight.__len__()-1:
                zh=np.dot(previous_set,self.listWeight[i]) + self.listBiais[i] #sum | zh : fonct° de combinaison
                ah = self.sigmoid(zh) # ah : fonct° sigmoïde
                # put into a list
                self. listAhiddenLayer.append(ah) # node value
                self.listZhiddenLayer.append(zh) # sum
                previous_set = ah # lire recherche l'ensemble précédent pour que la valeur des noeuds précédentes devienne
                                    # l'ensemble précédent pour les couches suivant, ce processus est le même pour les masqué
            else: # for output layer
                zo = np.dot(previous_set, self.listWeight[i]) + self.listBiais[i] # output sum
                self.ao = self.softmax(zo)  # value after softmax | utiliser pour mapper la sortie non normalisée d'un réseau
                                            # à une distribution de probabilité sur les classes de sortie prédites
                self.listAhiddenLayer.append(self.ao)
                self.listZhiddenLayer.append(zo)