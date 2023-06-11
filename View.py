import tkinter as tk
from PIL import Image, ImageTk

class View(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.title("Audio Player")
        self.master.geometry("500x400")

        play_image = Image.open("play.png")
        pause_image = Image.open("pause.png")
        stop_image = Image.open("stop.png")
        next_image = Image.open("next.png")
        prev_image = Image.open("previous.png")
        resume_image = Image.open("resume.png")
        add_track_image = Image.open("add_track.png")
        remove_track_image = Image.open("remove_track.png")

        play_image = play_image.resize((30, 30))
        pause_image = pause_image.resize((30, 30))
        stop_image = stop_image.resize((30, 30))
        next_image = next_image.resize((30, 30))
        prev_image = prev_image.resize((30, 30))
        resume_image = resume_image.resize((30, 30))
        add_track_image = add_track_image.resize((30, 30))
        remove_track_image = remove_track_image.resize((30, 30))

        self.play_icon = ImageTk.PhotoImage(play_image)
        self.pause_icon = ImageTk.PhotoImage(pause_image)
        self.stop_icon = ImageTk.PhotoImage(stop_image)
        self.next_icon = ImageTk.PhotoImage(next_image)
        self.prev_icon = ImageTk.PhotoImage(prev_image)
        self.resume_icon = ImageTk.PhotoImage(resume_image)
        self.add_track_icon = ImageTk.PhotoImage(add_track_image)
        self.remove_track_icon = ImageTk.PhotoImage(remove_track_image)

        self.track_listbox = tk.Listbox(master, width=60)
        self.track_listbox.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, image=self.add_track_icon, compound=tk.LEFT)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, image=self.remove_track_icon, compound=tk.LEFT)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.play_button = tk.Button(self.button_frame, image=self.play_icon, compound=tk.LEFT)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, image=self.stop_icon, compound=tk.LEFT)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, image=self.pause_icon, compound=tk.LEFT)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.unpause_button = tk.Button(self.button_frame, image=self.resume_icon, compound=tk.LEFT)
        self.unpause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, image=self.next_icon, compound=tk.LEFT)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(self.button_frame, image=self.prev_icon, compound=tk.LEFT)
        self.prev_button.pack(side=tk.LEFT, padx=5)

    def select_next_track(self, current_index):
        next_index = (current_index + 1) % self.track_listbox.size()
        self.track_listbox.activate(next_index)

    def select_prev_track(self, current_index):
        next_index = abs(current_index - 1) % self.track_listbox.size()
        self.track_listbox.activate(next_index)
