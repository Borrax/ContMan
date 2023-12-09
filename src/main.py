import tkinter as tk
from tkinter import Tk

from db_provider import DbProvider
from controllers.controllers import (
    GamesController, MoviesController, BooksController)
from views.ui import AppUi

root = Tk()
root.title('Content Manager')
root.geometry('400x400')
root.resizable(0, 0)
root.columnconfigure(0, weight=1)

games_controller = GamesController(DbProvider)
books_controller = BooksController(DbProvider)
movies_controller = MoviesController(DbProvider)

AppUi(root, games_controller, books_controller,
      movies_controller)

root.mainloop()
