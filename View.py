import tkinter as tk
from PIL import Image, ImageTk
import pygame.mixer
from tkinter import messagebox
from tkinter import ttk


class View(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.title("Audio Player")
        self.master.geometry("500x400")

        play_image = Image.open("resources/play.png")
        pause_image = Image.open("resources/pause.png")
        next_image = Image.open("resources/next.png")
        prev_image = Image.open("resources/previous.png")
        add_track_image = Image.open("resources/add_track.png")
        remove_track_image = Image.open("resources/remove_track.png")
        volume_image = Image.open("resources/volume.png")

        play_image = play_image.resize((30, 30))
        pause_image = pause_image.resize((30, 30))
        next_image = next_image.resize((30, 30))
        prev_image = prev_image.resize((30, 30))
        add_track_image = add_track_image.resize((30, 30))
        remove_track_image = remove_track_image.resize((30, 30))
        volume_image = volume_image.resize((30, 30))

        self.play_icon = ImageTk.PhotoImage(play_image)
        self.pause_icon = ImageTk.PhotoImage(pause_image)
        self.next_icon = ImageTk.PhotoImage(next_image)
        self.prev_icon = ImageTk.PhotoImage(prev_image)
        self.add_track_icon = ImageTk.PhotoImage(add_track_image)
        self.remove_track_icon = ImageTk.PhotoImage(remove_track_image)
        self.volume_icon = ImageTk.PhotoImage(volume_image)

        self.track_listbox = tk.Listbox(master, width=60)
        self.track_listbox.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, image=self.add_track_icon, compound=tk.LEFT)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, image=self.remove_track_icon, compound=tk.LEFT)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.play_stop_button = tk.Button(self.button_frame, image=self.play_icon, compound=tk.LEFT)
        self.play_stop_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, image=self.next_icon, compound=tk.LEFT)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(self.button_frame, image=self.prev_icon, compound=tk.LEFT)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        style = ttk.Style()
        style.configure("Custom.Horizontal.TScale",
                        background="lightgray",
                        troughcolor="blue",
                        sliderthickness=15,
                        borderwidth=0)

        self.volume_slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL,
                                       style="Custom.Horizontal.TScale",
                                       length=300)
        self.volume_icon_label = tk.Label(self.master, image=self.volume_icon)
        self.volume_icon_label.pack(side=tk.LEFT, padx=20, pady=20)
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=20, pady=20)

    def select_next_track(self, current_index):
        self.track_listbox.selection_clear(0, tk.END)
        next_index = (current_index + 1) % self.track_listbox.size()
        self.track_listbox.activate(next_index)
        self.track_listbox.selection_set(next_index, last=None)

    def select_prev_track(self, current_index):
        prev_index = (current_index - 1) % self.track_listbox.size()
        self.track_listbox.activate(prev_index)
        self.track_listbox.selection_clear(0, tk.END)
        prev_index = self.track_listbox.size() - 1 if current_index == 0 else current_index - 1
        self.track_listbox.activate(prev_index)
        self.track_listbox.selection_set(prev_index, last=None)

    def insert_track(self, name):
        self.track_listbox.insert(tk.END, name)

    def remove_track(self, index):
        self.track_listbox.delete(index)

    def change_play_to_stop_icon(self):
        self.play_stop_button.config(image=self.pause_icon)

    def change_stop_to_play_icon(self):
        self.play_stop_button.config(image=self.play_icon)

    def show_error(self, message):
        messagebox.showerror('Error', message)
