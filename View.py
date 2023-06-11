import tkinter as tk
from tkinter import messagebox


class View(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.title("Audio Player")
        self.master.geometry("500x400")

        self.track_listbox = tk.Listbox(master, width=60)
        self.track_listbox.pack()

        self.add_button = tk.Button(master, text="Add Track")
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remove Track")
        self.remove_button.pack()

        self.play_button = tk.Button(master, text="Play")
        self.play_button.pack()

        self.stop_button = tk.Button(master, text="Stop")
        self.stop_button.pack()

        self.pause_button = tk.Button(master, text="Pause")
        self.pause_button.pack()

        self.unpause_button = tk.Button(master, text="Resume")
        self.unpause_button.pack()

        self.next_button = tk.Button(master, text="Next")
        self.next_button.pack()

        self.prev_button = tk.Button(master, text="Previous")
        self.prev_button.pack()

    def select_next_track(self, current_index):
        self.track_listbox.selection_clear(0, tk.END)
        next_index = (current_index + 1) % self.track_listbox.size()
        self.track_listbox.activate(next_index)
        self.track_listbox.selection_set(next_index, last=None)

    def select_prev_track(self, current_index):
        self.track_listbox.selection_clear(0, tk.END)
        prev_index = self.track_listbox.size() - 1 if current_index == 0 else current_index - 1
        self.track_listbox.activate(prev_index)
        self.track_listbox.selection_set(prev_index, last=None)

    def insert_track(self, name):
        self.track_listbox.insert(tk.END, name)

    def remove_track(self, index):
        self.track_listbox.delete(index)

    def show_error(self, message):
        messagebox.showerror('Error', message)
