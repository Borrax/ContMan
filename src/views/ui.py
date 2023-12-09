import tkinter as tk
from tkinter import Tk


class AppUi:
    def __init__(self, root: Tk, games_controller,
                 books_controller, movies_controller):
        self.__root = root
        self.__books_controller = books_controller
        self.__games_controller = games_controller
        self.__movies_controller = movies_controller

        self.__init_ui()

    def __init_ui(self):
        self.__init_section('Movies', 0)

    def __init_section(self, title, row):
        section_frame = tk.Frame(self.__root)
        section_frame.grid(row=row, column=0)

        title_label = tk.Label(section_frame, text=title)
        title_label.grid(row=0, column=0)

        canvas = tk.Canvas(section_frame, height=200,
                           bg='green')
        canvas.grid(column=0, row=1, sticky='ew')
        canvas.grid_propagate(0)
