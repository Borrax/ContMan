import tkinter as tk
from tkinter import Tk

from controllers.controllers import FailedReq
from models.models import BaseItem


class ItemCard:
    times_invoked = 0

    def __shorten_text(text: str) -> str:
        if len(text) > 30:
            slice = text[:27]
            return slice + '...'

        return text

    def create(item, parent, max_col):
        title = ItemCard.__shorten_text(item.get('title'))
        year = item.get('year')
        score = item.get('score')
        cover_path = item.get('cover')

        container = tk.Frame(parent,
                             width=80,
                             height=100,
                             bg='blue')
        container.grid(row=ItemCard.times_invoked // max_col,
                       column=ItemCard.times_invoked % max_col)
        container.grid_propagate(0)
        container.columnconfigure(0, weight=1)

        title_label = tk.Label(container,
                               text=title)
        title_label.grid(row=1, column=0)


class AppUi:
    def __init__(self, root: Tk, games_controller,
                 books_controller, movies_controller):
        self.__root = root
        self.__books_controller = books_controller
        self.__games_controller = games_controller
        self.__movies_controller = movies_controller

        self.__init_ui()

    def __init_ui(self):
        self.__root.title('Content Manager')
        self.__root.geometry('800x600')
        self.__root.resizable(0, 0)
        self.__root.columnconfigure(0, weight=1)

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

        for item in collection.values():
            ItemCard.create(item, canvas, 6)
