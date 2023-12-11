import tkinter as tk


class FormError:
    def __init__(self, parent, err_msg, row, col):
        self.__create(parent, err_msg, row, col)

    def __create(self, parent, err_msg, row, col):
        error_label = tk.Label(parent,
                               text=f'❌ {err_msg}')

        error_label.grid(row=row, column=col)
