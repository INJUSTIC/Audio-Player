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

        self.volume_slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.VERTICAL,
                                       style="Custom.Vertical.TScale",
                                       length=200)
        self.volume_icon_label = tk.Label(self.master, image=self.volume_icon)
        self.volume_icon_label.pack(side=tk.LEFT, padx=20, pady=20)
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=20, pady=20)

        self.song_slider = ttk.Scale(self.master, from_=0, orient=tk.HORIZONTAL,
                                     style="Custom.Horizontal.TScale",
                                     length=300)

    def set_song_slider(self, length):
        self.song_slider.config(to=length)

    def update_song_slider(self, position):
        self.song_slider.set(position)

    def select_track(self, index):
        self.track_listbox.selection_clear(0, tk.END)
        self.track_listbox.activate(index)
        self.track_listbox.selection_set(index, last=None)

    def insert_track(self, name):
        self.track_listbox.insert(tk.END, name)

    def remove_track(self, index):
        self.track_listbox.delete(index)

    def change_play_to_stop_icon(self):
        self.play_stop_button.config(image=self.pause_icon)

    def change_stop_to_play_icon(self):
        self.play_stop_button.config(image=self.play_icon)

    def song_slider_on(self):
        self.song_slider.pack(side=tk.LEFT, padx=20, pady=20)

    def song_slider_off(self):
        self.song_slider.pack_forget()

    def show_error(self, message):
        messagebox.showerror('Error', message)
