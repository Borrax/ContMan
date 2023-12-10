from tkinter import Tk

from views.section import Section


class AppUi:
    __sections = []

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

        self.__sections.append(
            Section(self.__root, 'Movies', 0, self.__movies_controller))
