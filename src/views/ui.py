import tkinter as tk
from tkinter import Tk
from controllers.controllers import FailedReq


class AppUi:
    def __init__(self, root: Tk, games_controller,
                 books_controller, movies_controller):
        self.__root = root
        self.__books_controller = books_controller
        self.__games_controller = games_controller
        self.__movies_controller = movies_controller

        self.__init_ui()

    def __init_ui(self):
        self.__init_section('Movies', 0, self.__movies_controller)

    def __init_section(self, title, row, controller):
        resp = controller.get_collection()

        section_frame = tk.Frame(self.__root)
        section_frame.grid(row=row, column=0)

        title_label = tk.Label(section_frame, text=title)
        title_label.grid(row=0, column=0)

        if isinstance(resp, FailedReq):
            error_text = f'Error occured retrieving {title}\n' \
                f'{resp.err_msg}'
            error_label = tk.Label(section_frame,
                                   text=error_text,
                                   fg='red',
                                   wraplength=200)
            error_label.grid(column=0, row=1)
            return

        collection = resp.payload
        if len(collection) == 0:
            empty_frame = tk.Frame(section_frame,
                                   height=300)
            empty_frame.grid(row=1, column=0)

            msg_label = tk.Label(empty_frame, text='No Items Currently')
            msg_label.grid(column=0, row=0)
            return

        canvas = tk.Canvas(section_frame, height=200,
                           bg='green')
        canvas.grid(column=0, row=1, sticky='ew')


