import utility

class VArrow(object):
    def __init__(self):
        # super().__init__()
        self.weight = 0
        self.leftNode = None
        self.rightNode = None
        self.what = "arrow"

    def create(self, can, s, e):
        self.startX, self.startY = s
        self.endX, self.endY = e
        self.updatePoints()
        self.canvas = can
        self.aid = self.canvas.create_line(self.startX, self.startY, self.endX, self.endY, arrow = "last", tags = "arrow")
        self.tid = self.canvas.create_text(self.textX, self.textY, text = "W " + str(self.weight), fill = "red", tag = "arrow", font = utility.numberFont)

    def updatePoints(self):
        self.textX = (self.startX + self.endX) / 2
        self.textY = (self.startY + self.endY) / 2

    def movePtLeft(self, x, y):
        self.startX, self.startY = x, y
        self.canvas.coords(self.aid, self.startX, self.startY, self.endX, self.endY)
        self.updatePoints() # recalculate element points
        self.canvas.coords(self.tid, self.textX, self.textY) # move text

    def movePtRight(self, x, y):
        self.endX, self.endY = x, y
        self.canvas.coords(self.aid, self.startX, self.startY, self.endX, self.endY)
        self.updatePoints() # recalculate element points
        self.canvas.coords(self.tid, self.textX, self.textY) # move text 

    def updateWeight(self, w):
        self.weight = w
        self.canvas.itemconfig(self.tid, text = "W: " + str(self.weight))
        if (0 >= float(w)):
            self.canvas.itemconfig(self.tid, fill = "green")
        else:
            self.canvas.itemconfig(self.tid, fill = "red")