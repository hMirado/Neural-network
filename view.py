import tkinter as tk
import utility as vu
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import asksaveasfile, asksaveasfilename, askopenfilename
from tkinter import  messagebox
from vNode import VNode
from vArrow import VArrow
from controller import *

class View: # create view class
    def __init__(self, parent): # initialisat° class/object
        # initialisat° des variables
        self.container = parent # parent is the gui entry point give

        self.flagNetworkCreated = False
        self.flagNetworkTrained = False

        self.listComboBox = [] 
        self.listInputNode = []
        self.listOutputNode = []
        self.listVNode = []
        self.listVArrow = []

        self.trainFeaturePath = ""
        self.trainLabelPath = ""
        self.controller = None
        self.listFlatVNode = []
        self.lastx = 0
        self.lasty = 0

        self.flagLoadTrainFeature = False
        self.flagLoadTrainLabel = False

        self.trainLabelPath = "" # to store training label file
        self.trainFeaturePath = ""

    def createArrows(self):
        for i in range(0, len(self.listVNode)): # listVnode contains all the node created, thes vnodes ar 2)d list
            for j in self.listVNode[i]: # get nodes from layer
                arrowStart = j.getRightCod()
                if i < len(self.listVNode) - 1: # i is not the last layer
                    for q in self.listVNode[i + 1]: # q is the next layer nodes
                        arrowEnd = q.getLeftCod()
                        vArrow = VArrow()
                        vArrow.create(self.c, arrowStart, arrowEnd)
                        # give node the reference of its arrows left and right
                        q.addLeftArrow(vArrow) # link from node
                        j.addRightArrow(vArrow)
                        # give arrow the reference of its node
                        vArrow.leftNode = j
                        vArrow.rightNode = q
                        # append all arrows to a list
                        self.listVArrow.append(vArrow)
        return

    def flattenListVNode(self):
        self.listFlatVNode.clear()
        for layer in range(1, self.listVNode.__len__()):
            for n in self.listVNode[layer]:
                self.listFlatVNode.append(n)

    def setupControlNetwork(self):
        self.controller.numInput = len(self.listInputNode) # tell controller how many input nodes
        self.controller.numOutput = len(self.listOutputNode) # tell controller how many output nodes
        
        # tell controller how many hidden layer an nodes
        for i in range(len(self.listComboBox)):
            j = int(self.listComboBox[i].get())
            if j != 0:
                self.controller.numOfHLayers.append(j)
        # we need to pass these info, is for communicating with controller by using a flattened list

    def randomNum(self):
        self.controller.randomWeight(self.listVNode)
        self.controller.randomBiais(self.listVNode)


    def setup(self): # run firts
        """ Calls methods to setup the user interface """
        self.create_widgets() # create widget first
        self.setup_layout() # setup widget inside layouts, and initialize values

    def create_widgets(self):
        """ Create a various widgets in the tkinter window """

        # setup frame
        self.leftFrame = Frame(self.container, width = 100, height = vu.windowHeight)
        self.midFrame = Frame(self.container, width = vu.canvasWidth, height = vu.canvasHeight)
        self.rightFrame = Frame(self.container, width = 100, height = vu.windowHeight)
        self.rightFrame1 = Frame(self.rightFrame) # right top frame
        self.rightFrame2 = Frame(self.rightFrame) # right bootom sub frame

        self.statusbar = tk.Label(self.midFrame, text = "On the way ...", bd = 1, relief = tk.SUNKEN, anchor = tk.W, fg = "red", width = 100)

        self.lab1input = tk.Label(self.leftFrame, text = "Input layer")
        self.combo1input = ttk.Combobox(self.leftFrame, values = [1, 2, 3, 4, 5, 6, 7])

        self.lab2layer1 = tk.Label(self.leftFrame, text = "Mid layer 1")
        self.combo2layer1 = ttk.Combobox(self.leftFrame, values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab3layer2 = tk.Label(self.leftFrame, text = "Mid layer 2")
        self.combo3layer2 = ttk.Combobox(self.leftFrame, values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab4layer3 = tk.Label(self.leftFrame, text = "Mid layer 3")
        self.combo4layer3 = ttk.Combobox(self.leftFrame, values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab5output = tk.Label(self.leftFrame, text = "Output layer")
        self.combo5output = ttk.Combobox(self.leftFrame, values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        self.b2Circle = tk.Button(self.leftFrame, text = "Create Network", command = self.createNodes, width = 20, height = 1)
        # / setup frame

        # LEFT FRAME
        # training section
        self.lab6TrainDiv = tk.Label(self.leftFrame, text = "===Train===")
        self.lab7LerningRate = tk.Label(self.leftFrame, text = "Learning Rate")
        self.combo6learningrate = ttk.Combobox(self.leftFrame, values = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5])

        self.lab8epoch = tk.Label(self.leftFrame, text = "Number of epochs")
        self.combo7epoch = ttk.Combobox(self.leftFrame, values = [10, 5000, 10000, 100000, 200000, 500000, 1000000, 2000000,
                                                                5000000, 10000000, 20000000, 50000000])

        self.lab9refreshrate = tk.Label(self.leftFrame, text = "Refresh rate(epoch)")
        self.combo8refreshrate = ttk.Combobox(self.leftFrame, values = [2, 100, 200, 300, 500, 1000, 2000, 3000])

        self.b8LoadFeature = tk.Button(self.leftFrame, text = "Load Features", command = self.loadTrainFeature, width = 20, height = 1)

        self.b9LoadLabel = tk.Button(self.leftFrame, text = "Load Labels", command = self.loadTrainLabel, width = 20, height = 1)

        self.b10StartTrain = tk.Button(self.leftFrame, text = "Start Training", command = self.StartTrain, width = 20, height = 1)
        # / training section

        # save and load NN section
        self.lab9aSaveLoadFile = tk.Label(self.leftFrame, text = "===Save/Load NN===")
        self.bt10aSaveNN = tk.Button(self.leftFrame, text = "Save Network", command = self.saveNN, width = 20, height = 1)
        self.bt10bLoadNN = tk.Button(self.leftFrame, text = "Load Network", command = self.loadNN, width = 20, height = 1)
        # / save and load NN section

        # prediction section 
        self.lb10DivPrediction = tk.Label(self.leftFrame, text = "===Prediction==")
        self.b11LoadPreFeature = tk.Button(self.leftFrame, text = "Load Predict features", command = self.loadPreFeature, width = 20, height = 1)
        self.b12StartPredict = tk.Button(self.leftFrame, text = "Satrt Prediction", command = self.startPredict, width = 20, height = 1)
        self.lb11PreRounding = tk.Label(self.leftFrame, text = "Roundin")
        self.combo9Prerounding = ttk.Combobox(self.leftFrame, values = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001])
        # / prediction section
        # / LEFT FRAME


        # MID FRAME
        self.c = Canvas(self.midFrame, bg = "white", width = vu.canvasWidth, height = vu.canvasHeight)

        # bind actions
        self.c.tag_bind("drag", "<Button-1>", self.clicked) # click
        self.c.tag_bind("drag", "<B1-Motion>", self.drag) # drag 

        # / MID FRAME


        # RIGHT FRAME
        self.lab31ErrorRate = tk.Label(self.rightFrame1, text = "===Loss Function Value===")
        self.text31ErrorTxtbox = tk.Text(self.rightFrame1, bg="silver", width = 30)
        self.scl31vbar = tk.Scrollbar(self.rightFrame1, orient = VERTICAL)
        self.text31ErrorTxtbox.config(yscrollcommand = self.scl31vbar.set)
        self.scl31vbar.config(command = self.text31ErrorTxtbox.yview)

        self.lab32PredictionResult = tk.Label(self.rightFrame2, text = "===Prediction result===")
        self.text32PredictTxtbox = tk.Text(self.rightFrame2, bg="silver", width = 30)
        self.scl32vbarPre = tk.Scrollbar(self.rightFrame2, orient = VERTICAL)
        self.text32PredictTxtbox.config(yscrollcommand = self.scl32vbarPre.set)
        self.scl32vbarPre.config(command = self.text32PredictTxtbox.yview)
        # / RIGHT FRAME

        # list to point to all layer combo box
        self.listComboBox.append(self.combo1input)
        self.listComboBox.append(self.combo2layer1)
        self.listComboBox.append(self.combo3layer2)
        self.listComboBox.append(self.combo4layer3)
        self.listComboBox.append(self.combo5output)

        # Layout
    def setup_layout(self):
        self.leftFrame.pack(side = LEFT)
        self.midFrame.pack(side = LEFT)
        self.rightFrame.pack(side = RIGHT)
        self.rightFrame1.pack(side = TOP, fill = BOTH)
        self.rightFrame2.pack(side = BOTTOM, fill = BOTH)

        # LEFT FRAME
        # Pack NN parametre top left
        self.lab1input.pack(side = TOP)
        self.combo1input.pack(side = TOP)
        self.lab2layer1.pack(side = TOP)
        self.combo2layer1.pack(side = TOP)
        self.lab3layer2.pack(side = TOP)
        self.combo3layer2.pack(side = TOP)
        self.lab4layer3.pack(side = TOP)
        self.combo4layer3.pack(side = TOP)
        self.lab5output.pack(side = TOP)
        self.combo5output.pack(side = TOP)
        self.b2Circle.pack(side = TOP)

        # Pack training section
        self.lab6TrainDiv.pack(side = TOP)
        self.lab7LerningRate.pack(side = TOP)
        self.combo6learningrate.pack(side = TOP)
        self.lab8epoch.pack(side = TOP)
        self.combo7epoch.pack(side = TOP)
        self.lab9refreshrate.pack(side = TOP)
        self.combo8refreshrate.pack(side = TOP)
        self.b8LoadFeature.pack(side = TOP)
        self.b9LoadLabel.pack(side = TOP)
        self.b10StartTrain.pack(side = TOP)

        # Pack save and load section
        self.lab9aSaveLoadFile.pack(side = TOP)
        self.bt10aSaveNN.pack(side = TOP)
        self.bt10bLoadNN.pack(side = TOP)

        # Pack prediction section
        self.lb10DivPrediction.pack(side = TOP)
        self.b11LoadPreFeature.pack(side = TOP)
        self.b12StartPredict.pack(side = TOP)
        self.combo9Prerounding.pack(side = TOP)
        self.combo9Prerounding.pack(side = TOP)
        # / LEFT FRAME

        # RIGHT FRAME
        self.lab31ErrorRate.pack(side = TOP)
        self.rightFrame1.pack(side = TOP, fill = BOTH)
        self.text31ErrorTxtbox.pack(side = LEFT)
        self.scl31vbar.pack(side = LEFT, fill = Y)

        self.lab32PredictionResult.pack(side = TOP)
        self.rightFrame2.pack(side = BOTTOM, fill = BOTH)
        self.text32PredictTxtbox.pack(side = TOP)
        self.scl32vbarPre.pack(side = TOP, fill = Y)
         # / RIGHT FRAME

        # pack canvas
        self.c.pack(side = TOP)
            
        # pack status bar
        self.statusbar.pack(side = tk.BOTTOM, fill = tk.Y)

        # set default values to combo input boxes
        self.combo1input.current(2)
        self.combo2layer1.current(3)
        self.combo3layer2.current(0)
        self.combo4layer3.current(0)
        self.combo5output.current(2)

        self.combo6learningrate.current(2)
        self.combo7epoch.current(1)
        self.combo8refreshrate.current(2)
        self.combo9Prerounding.current(1)

        # set start up message for statusbar
        self.statusbar["text"] = "Ready."

    def clear(self): # clear methode
        self.c.delete("all")
        self.listVArrow.clear()
        self.lastx = 0
        self.lasty = 0
        self.listVArrow.clear()
        self.listVNode.clear()
        self.listInputNode.clear()
        self.listOutputNode.clear()
        self.listFlatVNode.clear
        self.controller.clear()

        return

    def createNodes(self):
        # check if network exist, clear first
        if self.flagNetworkCreated:
            self.clear() #TODO
        
        # next to need to get nodes info from GUI
        listComboGet = []
        # first is to remove 0 from layer node input
        for cb in self.listComboBox:
            if cb.get() != '0':
                listComboGet.append(cb.get()) # listComboGet is a local variable
        # Step 1 get total columns/layers of the network and get position
        j = 0 # index for current layer
        #index=0

        for i in listComboGet: # go trough combo boxes values, where 0 have been removed
            j += 1 # layer index
            listNodeCoord = vu.getNodePosition(len(listComboGet), int(i), j) # get node position
            listLayer = [] # a list tokeep nodes in one layer
            #index+=1

            # create nodes based on coordinations
            for c1 in listNodeCoord:
                vNode = VNode() # create single node, node is separate class
                vNode.create(self.c, c1[0], c1[1]) # create node in possition
                if j ==  1: # inpute node
                    vNode.what = "input" # set node type to input
                    self.listInputNode.append(vNode) # keep input node in a separate list
                elif j == listComboGet.__len__(): # node with output
                    vNode.what = "output" # set node type output
                    self.listOutputNode.append(vNode) # output node list
                listLayer.append(vNode)
            self.listVNode.append(listLayer)
        
        self.createArrows() # create arrows to link nodes
        self.flattenListVNode() # list is for data transfert from backend neural network
        self.setupControlNetwork() # setup back end neural network
        self.randomNum() # generate random weights and biais

        # set flag as true
        self.flagNetworkCreated = True
        self.flagNetworkTrained = False

        # reload train feature and label if they have been loade before
        if self.controller.flagTrainFeatureLoad:
            self.controller.loadTrainFeature(self.trainFeaturePath)
        if self.controller.flagTrainLabelLoad:
            self.controller.loadTrainLabel(self.trainLabelPath)


    def loadTrainFeature(self):
        if self.flagNetworkCreated == False: # check if a network already created
            tk.messagebox.showinfo(title = "Error", message = "Please create network first")
        else:
            self.trainFeaturePath = ""
            self.trainFeaturePath = askopenfilename(
                                        initialdir = "./",
                                        filetypes = [("Text file", "*.txt"), ("All files", "*.*")],
                                        title = "Choose a file"
                                    ) # get file path
            self.controller.loadTrainFeature(self.trainFeaturePath)

    def loadTrainLabel(self):
        if self.controller.flagTrainFeatureLoad == False:
            tk.messagebox.showinfo(title = "Error", message = "Please create network and load train feature set first")
        else:
            self.trainLabelPath = ""
            self.trainLabelPath = askopenfilename(
                                        initialdir = "./",
                                        filetypes = [("Text file", "*.txt"), ("All files", "*.*")],
                                        title = "Choose a file"
                                    )
            self.controller.loadTrainLabel(self.trainLabelPath)

    def clearInputValue(self):
        for n in self.listInputNode:
            n.updateValue(0.0)

    def StartTrain(self):
        if self.controller.flagTrainLabelLoad == False: # check if data file loaded
            # if no network or file loaded, remind user
            tk.messagebox.showinfo(title = "Error", message = "Please create network and load train feature and label first")
        else:
            self.b10StartTrain["state"] = DISABLED # disable train button
            self.statusbar["text"] = "Training ...."
            self.controller.startTrain()
            self.b10StartTrain["state"] = NORMAL # after training
            self.flagNetworkTrained = True

    def saveNN(self):
        return

    def loadNN(self):
        return

    def loadPreFeature(self):
        return

    def startPredict(self):
        return


    def clicked(self, event):
        self.clickedid = event.widget.find_withtag('current')[0] # get id of clicked item
        self.lastx, self.lasty = event.x, event.y # update item x and w

    def drag(self, event):
        for column in self.listVNode: # go through node layer
            for n in column:
                if n.containAny(self.clickedid): # if node contains click id
                    n.move(event.x - self.lastx, event.y - self.lasty) # move grouped item
                    self.lastx = event.x # update last item position
                    self.lasty = event.y

    def setController(self, con): # set link to controller
        self.controller = con  

    def updateBiais(self, controlFlatBiaisList):
        for i in range(0, controlFlatBiaisList.__len__()):
            self.listFlatVNode[i].updateBiais(controlFlatBiaisList[i]) # call vnode update biais

    def updateWeight(self, controlFlatWeightList): # 1d list
        for i in range(0, controlFlatWeightList.__len__()):
            self.listVArrow[i].updateWeight(controlFlatWeightList[i])

    # def setInputValue(self, setV):
    #     for i in range(0, setV.__len__()):
    #         self.listInputNode[i].updateValue(setV[i])