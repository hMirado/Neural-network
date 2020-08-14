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