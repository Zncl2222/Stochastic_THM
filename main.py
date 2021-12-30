import sys
import tkinter as tk
import os
import numpy as np
import pandas as pd
import time
import ttkthemes as th
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import colorchooser
import pickle
from multiprocessing import Pool

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
    #Window=Options_GUI()

    root.mainloop()