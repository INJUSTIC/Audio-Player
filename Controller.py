import threading

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
        self.view.volume_slider.config(command=self.volume_change)
        self.view.song_slider.bind("<ButtonRelease-1>", self.song_position_change)
        self.view.track_listbox.bind("<<ListboxSelect>>", lambda event: self.listbox_select())
        self.update_slider_pos()
        self.mixer.music.set_volume(0.5)
        self.isPlaying = False
        self.isPaused = False
        self.curr_track_pos = None
        self.selected_track_pos = None

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
            duration = int(MP3(track_loc).info.length)
            self.model.add_track(track_name, duration, track_loc)
            self.view.insert_track(track_name)

    def remove_track(self):
        if self.selected_track_pos:
            track_to_remove = self.view.track_listbox.get(tk.ACTIVE)
            self.view.remove_track(self.selected_track_pos[0])
            self.model.remove_track(track_to_remove)
            if self.curr_track_pos == self.selected_track_pos:
                self.isPlaying = False
                self.isPaused = False
                self.curr_track_pos = None
                self.selected_track_pos = None
                self.view.change_stop_to_play_icon()
                self.stop_track()
                self.view.song_slider_off()
            elif not self.curr_track_pos:
                self.selected_track_pos = None
            else:
                if self.selected_track_pos[0] < self.curr_track_pos[0]:
                    self.curr_track_pos = (self.curr_track_pos[0] - 1,)
                self.selected_track_pos = self.curr_track_pos
                self.view.select_track(self.selected_track_pos[0])
                if self.isPlaying:
                    self.view.change_play_to_stop_icon()
                else:
                    self.view.change_stop_to_play_icon()
        else:
            messagebox.showerror('Error', 'Choose a track to delete')

    def play_pause_resume_manage(self):
        if self.isPlaying and self.curr_track_pos == self.selected_track_pos:
            self.pause_track()
        elif self.isPaused and self.curr_track_pos == self.selected_track_pos:
            self.unpause_track()
        else:
            self.stop_track()
            self.play_track()

    def play_track(self):
        if not self.selected_track_pos:
            self.isPlaying = False
            self.view.show_error("Choose track to play")
            return
        track_to_play = self.view.track_listbox.get(tk.ACTIVE)
        track = self.model.read_track(track_to_play)
        try:
            self.mixer.music.load(track.path)
            song = MP3(track.path)
        except pygame.error:
            self.isPlaying = False
            self.view.show_error(f'No file found: {track.path}')
            return
        self.mixer.music.play(loops=0)
        self.view.change_play_to_stop_icon()
        self.view.set_song_slider(song.info.length * 1000)
        self.view.update_song_slider(0)
        self.view.song_slider_on(track.duration)
        self.isPlaying = True
        self.curr_track_pos = self.selected_track_pos
        # thread = threading.Thread(target=self.check_for_track_ending)
        # thread.start()
       # self.check_for_track_ending()

    def listbox_select(self):
        self.selected_track_pos = self.view.track_listbox.curselection()
        if self.isPlaying:
            if self.selected_track_pos != self.curr_track_pos:
                self.view.change_stop_to_play_icon()
            else:
                self.view.change_play_to_stop_icon()

    def check_for_track_ending(self):
        if self.isPlaying:
            if self.mixer.music.get_busy():
                self.view.master.after(1000, self.check_for_track_ending)
            else:
                self.next_track()

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
        self.check_for_track_ending()

    def next_track(self):
        self.stop_track()
        if self.curr_track_pos:
            self.selected_track_pos = self.curr_track_pos
            self.view.select_track((self.curr_track_pos[0] + 1) % self.view.track_listbox.size())
            self.listbox_select()
            self.play_track()

    def prev_track(self):
        self.stop_track()
        if self.curr_track_pos:
            self.selected_track_pos = self.curr_track_pos
            self.view.select_track((self.curr_track_pos[0] - 1) % self.view.track_listbox.size())
            self.listbox_select()
            self.play_track()

    def song_position_change(self, event):
        position = self.view.song_slider.get() / 1000
        self.mixer.music.set_pos(position)
        self.view.update_song_slider(position * 1000)

    def update_slider_pos(self):
        if self.mixer.music.get_busy():
            self.view.update_song_slider(self.view.song_slider.get() + 1000)
        self.view.master.after(1000, self.update_slider_pos)

    def volume_change(self, value):
        volume = 1 - (float(value) / 100)
        mixer.music.set_volume(volume)
