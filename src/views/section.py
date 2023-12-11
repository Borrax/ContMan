import tkinter as tk

from controllers.controllers import FailedReq, MoviesController
from views.item_card import ItemCard


class Section:
    __item_cards = []

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

        add_btn = tk.Button(section_frame, text='➕ Add')
        add_btn.configure(command=lambda: self.__show_add_view(
            section_frame, 1, 0
        ))
        add_btn.grid(row=0, column=1)

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
        canvas.grid(column=0, row=1, sticky='ew', columnspan=2)
        canvas.grid_propagate(0)
        canvas.columnconfigure((0, 1, 2, 3, 4, 5,
                                6, 7, 8, 9), weight=1)

        item_counter = 0
        for (id, item) in collection.items():
            item_card = ItemCard(id, item, canvas, 9, item_counter)
            self.__item_cards.append(item_card)
            item_counter += 1
        self.__show_add_view(section_frame, 1, 0)

    def __show_add_view(self, parent, row, col):
        if isinstance(self.controller, MoviesController):
            self.__movie_add_view(parent, row, col)

    def __movie_add_view(self, parent, row, col):
        container = tk.Frame(parent, width=300,
                             height=240)
        container.grid(row=row, column=col)
        container.grid_propagate(0)
        container.rowconfigure((1, 2, 3, 4, 5), weight=1)
        container.columnconfigure((0, 1), weight=1)

        close_btn = tk.Button(container, text='X',
                              font='Helvetica 12 bold',
                              command=lambda: container.destroy(),
                              width=2)
        close_btn.grid(row=0, column=1, sticky='e', padx=15, pady=2)

        title_Label = tk.Label(container, text='Title (mandatory):',
                               font='Helvetica 10 bold')
        title_entry = tk.Entry(container, width=24)
        title_Label.grid(row=1, column=0, pady=10)
        title_entry.grid(row=1, column=1)

        duration_Label = tk.Label(container, text='Duration:',
                                  font='Helvetica 10 bold')
        duration_entry = tk.Entry(container, width=14)
        duration_Label.grid(row=2, column=0, pady=10)
        duration_entry.grid(row=2, column=1)

        year_Label = tk.Label(container, text='Year:',
                              font='Helvetica 10 bold')
        year_entry = tk.Entry(container, width=7)
        year_Label.grid(row=3, column=0, pady=10)
        year_entry.grid(row=3, column=1)

        score_Label = tk.Label(container, text='Score:',
                              font='Helvetica 10 bold')
        score_entry = tk.Entry(container, width=7)
        score_Label.grid(row=4, column=0, pady=10)
        score_entry.grid(row=4, column=1)

        add_btn = tk.Button(container, text='➕',
                            width=5)
        add_btn.grid(row=5, column=0, columnspan=2)


