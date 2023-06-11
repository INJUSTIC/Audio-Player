import pygame
from tkinter import *

from Controller import Controller
from Model import AudioPlayer
from View import View


def main():
    root = Tk()
    view = View(root)
    audio_player = AudioPlayer()
    controller = Controller(audio_player, view)
    root.mainloop()


if __name__ == "__main__":
    main()

