import sys
import tkinter as tk
import os

os.chdir(os.path.dirname(__file__))

project_home = r".\src"

if project_home not in sys.path:
    sys.path = [project_home] + sys.path


from guithread import GUI_thread
from datareading import Stochastic_read
from mcplot import *
from statcalculation import *
import activate
from gui import main_GUI


if __name__ == '__main__':             
    root = tk.Tk()
    
    Window=main_GUI(root)

    root.mainloop()