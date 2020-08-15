from tkinter import *
from view import View
from controller import Controller
import utility as vu

# test view
if __name__ == "__main__":
    mainwin = Tk() # tk instance
    WIDTH = vu.windowWight
    HEIGHT = vu.windowHeight
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    mainwin.title("Graphical Neural Network")

    # controller view and controller
    view = View(mainwin)
    controller = Controller()
    # cross link view and controller
    controller.setView(view) # link view to controller
    view.setController(controller)

    view.setup()
    mainwin.mainloop()