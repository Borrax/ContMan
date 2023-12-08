import tkinter as tk
from tkinter import Tk
import controllers.controllers

root = Tk()
root.title('Content Manager')
root.geometry('400x400')
root.resizable(0, 0)
root.columnconfigure(0, weight=1)

root.mainloop()
