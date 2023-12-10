import tkinter as tk


class ItemCard:
    def __init__(self, id, item, parent,
                 max_col, curr_index):
        self.id = id
        self.item = item
        self.parent = parent
        self.curr_index = curr_index
        self.max_col = max_col

        self.__create()

    def __shorten_text(self, text: str) -> str:
        if len(text) > 30:
            slice = text[:27]
            return slice + '...'

        return text

    def __create(self):
        title = self.__shorten_text(self.item.get('title'))
        year = self.item.get('year')
        score = self.item.get('score')
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
        image_label = tk.Label(container, image=self.image)
        image_label.grid(row=0, column=0)

        title_label = tk.Label(container,
                               text=title)
        title_label.grid(row=1, column=0)
