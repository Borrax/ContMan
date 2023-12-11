import tkinter as tk


class ItemCard:
    def __init__(self, id, item, parent,
                 max_col, curr_index, parent_funcs):
        self.id = id
        self.item = item
        self.parent = parent
        self.curr_index = curr_index
        self.max_col = max_col
        self.parent_funcs = parent_funcs

        self.__create()

    def __shorten_text(self, text: str) -> str:
        if len(text) > 13:
            slice = text[:10]
            return slice + '...'

        return text

    def __create(self):
        title = self.__shorten_text(self.item.get('title'))
        cover_path = self.item.get('cover')

        container = tk.Frame(self.parent,
                             width=76,
                             height=100,
                             bg='blue')
        container.grid(row=self.curr_index // self.max_col,
                       column=self.curr_index % self.max_col,
                       padx=5, pady=5, sticky='nesw')
        container.grid_propagate(0)
        container.columnconfigure(0, weight=1)

        self.image = tk.PhotoImage(file=cover_path)
        image_label = tk.Label(container, image=self.image,
                               height=190)
        image_label.grid(row=0, column=0, sticky='nesw',
                         columnspan=2)

        btn_container = tk.Frame(container,
                                 height=15, width=35)
        btn_container.grid(row=0, column=1, sticky='n')
        btn_container.grid_propagate(0)
        btn_container.rowconfigure(0, weight=1)
        btn_container.columnconfigure(0, weight=1)

        del_btn = tk.Button(btn_container, text='X',
                            command=lambda: self.parent_funcs['delete_item'](
                                self.id
                            ))
        del_btn.grid(row=0, column=1)

        edit_btn = tk.Button(btn_container,
                             text='✐',
                             command=lambda: self.parent_funcs[
                                'show_edit_form'](
                                self.id, self.item
                             ))
        edit_btn.grid(row=0, column=0)

        title_label = tk.Label(container, text=title,
                               font='Helvetica 9 bold italic')
        title_label.grid(row=0, column=0, sticky='n',
                         pady=80, columnspan=2)
