import tkinter as tk

from controllers.controllers import FailedReq
from views.item_card import ItemCard


class Section:
    def __init__(self, parent, title, row_number, controller):
        self.parent = parent
        self.title = title
        self.row_number = row_number
        self.controller = controller

        self.__create()

    def __create(self):
        resp = self.controller.get_collection()

        section_frame = tk.Frame(self.parent,
                                 bg='red')
        section_frame.grid(row=self.row_number, column=0,
                           sticky='nsew')
        section_frame.columnconfigure(0, weight=1)

        title_label = tk.Label(section_frame, text=self.title)
        title_label.grid(row=0, column=0)

        if isinstance(resp, FailedReq):
            error_text = f'Error occured retrieving {self.title}\n' \
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

        canvas = tk.Canvas(section_frame, height=300,
                           bg='green')
        canvas.grid(column=0, row=1, sticky='ew')
        canvas.grid_propagate(0)
        canvas.columnconfigure((0, 1, 2, 3, 4, 5,
                                6, 7, 8, 9), weight=1)

        item_counter = 0
        for (id, item) in collection.items():
            ItemCard(id, item, canvas, 9, item_counter)
            item_counter += 1
