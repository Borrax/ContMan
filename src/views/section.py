import tkinter as tk

from controllers.controllers import FailedReq, MoviesController
from views.item_card import ItemCard
from views.form_error import FormError


class Section:
    __item_cards = []
    __primary_container = None

    def __init__(self, parent, title, row_number, controller):
        self.parent = parent
        self.title = title
        self.row_number = row_number
        self.controller = controller

        self.__create()

    def __create(self):
        self.__item_cards = []
        resp = self.controller.get_collection()

        section_frame = tk.Frame(self.parent,
                                 bg='red')
        section_frame.grid(row=self.row_number, column=0,
                           sticky='nsew')
        section_frame.columnconfigure(0, weight=1)

        title_label = tk.Label(section_frame, text=self.title)
        title_label.grid(row=0, column=0)

        add_btn = tk.Button(section_frame, text='➕ Add')
        add_btn.configure(command=self.__show_add_view)

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

        empty_frame = tk.Frame(section_frame,
                               height=300)
        empty_frame.grid(row=1, column=0, sticky='ew',
                         columnspan=2)
        empty_frame.columnconfigure(0, weight=1)
        self.__primary_container = empty_frame

        collection = resp.payload
        if len(collection) == 0:
            msg_label = tk.Label(empty_frame, text='No Items Currently')
            msg_label.grid(column=0, row=0)
            return

        canvas = tk.Canvas(empty_frame,
                           bg='green')
        canvas.grid(column=0, row=0, sticky='ew')

        scrollbar = tk.Scrollbar(empty_frame, orient='vertical',
                                 command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        canvas['yscrollcommand'] = scrollbar.set

        items_container = tk.Frame(canvas)
        items_container.grid(row=0, column=0, sticky='ew')

        items_container.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            ))
        canvas.create_window((0, 0), window=items_container,
                             anchor='nw')

        funcs = self.__get_funcs_for_cards()

        item_counter = 0
        for (id, item) in collection.items():
            item_card = ItemCard(id, item, items_container,
                                 9, item_counter, funcs)
            self.__item_cards.append(item_card)
            item_counter += 1

    def __show_add_view(self):

        if isinstance(self.controller, MoviesController):
            sv_default_vals = {
                'title': '',
                'year': '',
                'dur': '',
                'score': ''
            }

            parent = self.__primary_container
            submit_func = self.__submit_movie_item
            self.__movie_add_form(parent, 0, 0,
                                  sv_default_vals, submit_func)

    def __show_edit_form(self, id, item_info):

        if isinstance(self.controller, MoviesController):
            sv_default_vals = {
                'title': item_info.get('title'),
                'year': item_info.get('year'),
                'dur': item_info.get('duration'),
                'score': item_info.get('score')
            }

            parent = self.__primary_container
            submit_func = self.__submit_edit_movie_item
            self.__movie_add_form(parent, 0, 0,
                                  sv_default_vals, submit_func, id,
                                  item_info.get('cover'))

    def __movie_add_form(self, parent, row, col,
                         sv_defaults, submit_func, id=None, cover=None):
        title_sv = tk.StringVar()
        year_sv = tk.StringVar()
        dur_sv = tk.StringVar()
        score_sv = tk.StringVar()

        title_sv.set(sv_defaults.get('title'))
        year_sv.set(sv_defaults.get('year'))
        dur_sv.set(sv_defaults.get('dur'))
        score_sv.set(sv_defaults.get('score'))

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
        title_entry = tk.Entry(container, width=24,
                               textvariable=title_sv)
        title_Label.grid(row=1, column=0, pady=10)
        title_entry.grid(row=1, column=1)

        duration_Label = tk.Label(container, text='Duration:',
                                  font='Helvetica 10 bold')
        duration_entry = tk.Entry(container, width=14,
                                  textvariable=dur_sv)
        duration_Label.grid(row=2, column=0, pady=10)
        duration_entry.grid(row=2, column=1)

        year_Label = tk.Label(container, text='Year:',
                              font='Helvetica 10 bold')
        year_entry = tk.Entry(container, width=7,
                              textvariable=year_sv)
        year_Label.grid(row=3, column=0, pady=10)
        year_entry.grid(row=3, column=1)

        score_Label = tk.Label(container, text='Score:',
                               font='Helvetica 10 bold')
        score_entry = tk.Entry(container, width=7,
                               textvariable=score_sv)
        score_Label.grid(row=4, column=0, pady=10)
        score_entry.grid(row=4, column=1)

        add_btn = tk.Button(container, text='➕',
                            width=5,
                            command=lambda: submit_func(
                                title_sv.get(), year_sv.get(), score_sv.get(),
                                dur_sv.get(), container, id, cover
                             ))
        add_btn.grid(row=5, column=0, columnspan=2)

    def __submit_movie_item(self, title, year, score, duration,
                            add_view, id=None, cover=None):
        resp = self.controller.add_item(title=title, year=year,
                                        score=score, duration=duration,
                                        cover=cover)

        if isinstance(resp, FailedReq):
            FormError(add_view, resp.err_msg, 0, 0)
            return

        add_view.destroy()
        self.__create()

    def __get_funcs_for_cards(self):
        funcs = {}
        if isinstance(self.controller, MoviesController):
            funcs['delete_item'] = self.__delete_movie_item
            funcs['show_edit_form'] = self.__show_edit_form

        return funcs

    def __delete_movie_item(self, id):
        resp = self.controller.delete_item(id)

        if isinstance(resp, FailedReq):
            return

        self.__create()

    def __submit_edit_movie_item(self, title, year, score, dur,
                                 container, id, cover):
        resp = self.controller.edit_item(id, {
            'title': title,
            'year': year,
            'score': score,
            'duration': dur,
            'cover': cover
        })

        if isinstance(resp, FailedReq):
            FormError(container, resp.err_msg, 0, 0)
            return

        container.destroy()
        self.__create()
