import pygame

from Model import AudioPlayer
from Model import AudioTrack
from View import View
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import messagebox


class Controller:
    def __init__(self, model: AudioPlayer, view: View):
        self.model = model
        self.view = view
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.view.add_button.config(command=self.add_track)
        self.view.remove_button.config(command=self.remove_track)
        self.view.play_button.config(command=self.play_track)
        self.view.pause_button.config(command=self.pause_track)
        self.view.unpause_button.config(command=self.unpause_track)
        self.view.stop_button.config(command=self.stop_track)
        self.view.next_button.config(command=self.next_track)
        self.view.prev_button.config(command=self.prev_track)

    def add_track(self):
        track_loc = filedialog.askopenfilename(title='Choose a track',
                                               filetypes=(('mp3 files', '*.mp3'),))
        track_name = track_loc.split('/')[-1].split('.')[0]
        if self.model.check_for_track(track_name):
            messagebox.showerror('Error', "There is already soundtrack with such name")
        else:
            duration = MP3(track_loc).info.length
            self.model.add_track(track_name, duration, track_loc)
            self.view.track_listbox.insert(tk.END, track_name)

    def remove_track(self):
        selected_index = self.view.track_listbox.curselection()
        if selected_index:
            track_to_remove = self.view.track_listbox.get(tk.ACTIVE)
            self.view.track_listbox.delete(selected_index)
            self.model.remove_track(track_to_remove)
        else:
            messagebox.showerror('Error', 'Choose track to delete')

    def play_track(self):
        if not self.view.track_listbox.curselection():
            messagebox.showerror('Error', "Choose track to play")
            return
        track_to_play = self.view.track_listbox.get(tk.ACTIVE)
        try:
            track = self.model.read_track(track_to_play)
        except ValueError:
            print('ValueError: no such track')
            return
        try:
            self.mixer.music.load(track.path)
        except pygame.error:
            messagebox.showerror('Error', f'No file found: {track.path}')
            return
        self.mixer.music.play(loops=0)

    def stop_track(self):
        self.mixer.music.stop()

    def pause_track(self):
        self.mixer.music.pause()

    def unpause_track(self):
        self.mixer.music.unpause()

    def next_track(self):
        self.stop_track()
        current_index = self.view.track_listbox.curselection()
        if current_index:
            self.view.select_next_track(current_index[0])

    def prev_track(self):
        self.stop_track()
        current_index = self.view.track_listbox.curselection()
        if current_index:
            self.view.select_prev_track(current_index[0])

    def prev_track(self):
        self.mixer.music.unpause()

