# CONTAIN USEFUL FUNCTIONS

canvasWidth = 1000
canvasHeight = 770
windowHeight = 800
windowWight = 1600
networkOffset = -100
nodeWidth = 50
nodeHeight = 50
textOffsetY = 16
dotHalfSize = 4
numberFont = "Helvetica 7"

def getNodePosition(totalcolumn, thisTotalrow, layerno):
    columnDis = (canvasWidth - 100) / (totalcolumn) # get distance between columns
    x = layerno * columnDis + networkOffset # get x coordinate
    yGap = canvasHeight / (thisTotalrow + 2) # get distance between rows
    listCoord = [] # a list to strore coordinates
    for i in range(0, thisTotalrow): # row to create all coordinates for nodes in a column
        y = (i + 1) * yGap
        listCoord.append([x - nodeWidth / 2, y - nodeHeight / 2]) # x,y to be offset so allow node size
    return listCoord # return all coordinate