import pygame
from Model import Model
from View import View
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import messagebox
import pygame.mixer as mixer


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        for track_name in self.model.read_track_names():
            self.view.insert_track(track_name)
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.view.add_button.config(command=self.add_track)
        self.view.remove_button.config(command=self.remove_track)
        self.view.play_stop_button.config(command=self.play_pause_resume_manage)
        self.view.next_button.config(command=self.next_track)
        self.view.prev_button.config(command=self.prev_track)
        self.view.volume_slider.config(command=self.on_slider_change)
        self.isPlaying = False
        self.isPaused = False

    def add_track(self):
        track_loc = filedialog.askopenfilename(title='Choose a track',
                                               filetypes=(('mp3 files', '*.mp3'),))
        if not track_loc:
            return
        track_name = track_loc.split('/')[-1].split('.')[0]
        if self.model.check_for_track(track_name):
            messagebox.showerror('Error', "There is already a soundtrack with such name")
            self.view.show_error("There is already soundtrack with such name")
        else:
            duration = MP3(track_loc).info.length
            self.model.add_track(track_name, duration, track_loc)
            self.view.insert_track(track_name)

    def remove_track(self):
        selected_index = self.view.track_listbox.curselection()
        if selected_index:
            track_to_remove = self.view.track_listbox.get(tk.ACTIVE)
            self.view.remove_track(selected_index)
            self.model.remove_track(track_to_remove)
        else:
            messagebox.showerror('Error', 'Choose a track to delete')

    def play_pause_resume_manage(self):
        if self.isPlaying:
            self.pause_track()
        else:
            if self.isPaused:
                self.unpause_track()
            else:
                self.play_track()

    def play_track(self):
        if not self.view.track_listbox.curselection():
            self.isPlaying = False
            self.view.show_error("Choose track to play")
            return
        track_to_play = self.view.track_listbox.get(tk.ACTIVE)
        try:
            track = self.model.read_track(track_to_play)
        except ValueError:
            print('ValueError: no such track')
            self.isPlaying = False
            return
        try:
            self.mixer.music.load(track.path)
        except pygame.error:
            self.isPlaying = False
            self.view.show_error("f'No file found: {track.path}'")
            return
        self.mixer.music.play(loops=0)
        self.isPlaying = True
        self.view.change_play_to_stop_icon()

    def stop_track(self):
        self.mixer.music.stop()

    def pause_track(self):
        self.mixer.music.pause()
        self.isPaused = True
        self.isPlaying = False
        self.view.change_stop_to_play_icon()

    def unpause_track(self):
        self.mixer.music.unpause()
        self.isPaused = False
        self.isPlaying = True
        self.view.change_play_to_stop_icon()

    def next_track(self):
        self.stop_track()
        current_index = self.view.track_listbox.curselection()
        if current_index:
            self.view.select_next_track(current_index[0])
            self.play_track()

    def prev_track(self):
        self.stop_track()
        current_index = self.view.track_listbox.curselection()
        if current_index:
            self.view.select_prev_track(current_index[0])
            self.play_track()

    def on_slider_change(self, value):
        volume = float(value) / 100
        mixer.music.set_volume(volume)
