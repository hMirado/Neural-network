import utility

class VNode:
    def __init__(self): # initialize vNode
        self.biais = 0 # represente biais for each node
        self.leftArrow = [] # reference to lef arrow
        self.rightArrow = [] # reference to right arrow
        self.what = None # to define type
        self.value = 0 # the value of the node

    def create(self, can, x, y): # can canvas, x, y coordinate
        self.startX = x
        self.startY = y
        self.canvas = can
        self.updatePoints()
        self.cid = self.canvas.create_oval(self.startX, self.startY, self.endX, self.endY, fill = "orange", tags = "drag") # create circle
        self.stardId = self.canvas.create_rectangle(
            self.leftX - utility.dotHalfSize,
            self.leftY - utility.dotHalfSize,
            self.leftX + utility.dotHalfSize,
            self.leftY + utility.dotHalfSize,
            fill = "gray", tags = "drag"
        )
        self.endId = self.canvas.create_rectangle(
            self.rightX - utility.dotHalfSize,
            self.rightY - utility.dotHalfSize,
            self.rightX + utility.dotHalfSize,
            self.rightY + utility.dotHalfSize,
            fill = "gray", tags = "drag"
        )
        self.tidbias = self.canvas.create_text(self.textX, self.textY, text=str("B: " + str(self.biais)), fill = "red", tag = "drag")
        self.tidValue = self.canvas.create_text(self.textVX, self.textVY, text=str("V " + str(self.value)), fill = "blue", tag = "drag")


    def updatePoints(self):
        self.endX = self.startX + utility.nodeWidth # get bottom right corner coordinates
        self.endY = self.startY + utility.nodeWidth
        self.centerX, self.centerY = (self.startX + self.endX) / 2, (self.startY + self.endY) / 2 # get center point
        self.leftX, self.leftY = self.startX, self.centerY
        self.rightX, self.rightY = self.endX, self.endY
        self.textX = (self.startX + self.endX) / 2
        self.textY = (self.startY + self.endY) / 2 - utility.textOffsetY # biais on top
        self.textVX = (self.startX + self.endX) / 2
        self.textVY = (self.startY + self.endY) / 2 + utility.textOffsetY # value on bottom
       
    
    def getLeftCod(self):
        return (self.leftX, self.leftY)

    def getRightCod(self):
        return (self.rightX, self.rightY)

    def addLeftArrow(self, la):
        self.leftArrow.append(la)
    
    def addRightArrow(self, ra):
        self.rightArrow.append(ra)

    def containAny(self, id): # check if node contains cliked item 
        if id == self.stardId: # the start point
            return True
        elif id == self.endId:
            return True
        elif id == self.cid: # circle
            return True
        elif id == self.tidbias:
            return True
        elif id == self.tidValue:
            return True
        else:
            return False

    def move(self, x, y):
        # remove elements
        self.canvas.move(self.cid, x, y)
        self.canvas.move(self.stardId, x, y)
        self.canvas.move(self.endId, x, y)
        self.canvas.move(self.tidbias, x, y)
        self.canvas.move(self.tidValue, x, y)

        # update current position
        self.startX += x
        self.startY += y
        self.endX += x
        self.endY += y
        self.updatePoints()

        # arrange display orders
        self.canvas.tag_raise(self.cid)
        self.canvas.tag_raise(self.stardId)
        self.canvas.tag_raise(self.endId)
        self.canvas.tag_raise(self.tidbias)
        self.canvas.tag_raise(self.tidValue)

        # move arrows
        for la in self.leftArrow: # left arrow
            la.movePtRight(self.leftX, self.leftY) # move arrow right end
        for ra in self.rightArrow: # right arrow
            ra.movePtLeft(self.rightX, self.rightY) # move arrow left end