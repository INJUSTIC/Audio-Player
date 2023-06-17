from tkinter import *

from Controller import Controller
from Model import Model
from View import View


def main():
    root = Tk()
    view = View(root)
    audio_player = Model()
    controller = Controller(audio_player, view)
    root.mainloop()


if __name__ == "__main__":
    main()

