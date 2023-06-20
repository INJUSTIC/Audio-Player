import os
import time
import unittest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from tkinter import *

from mutagen.mp3 import MP3

from Controller import Controller
from Model import Model
from View import View


def del_file():
    if os.path.exists('tracks.pkl'):
        os.remove('tracks.pkl')


class TestAudioPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.view = View(Tk())

    def set_up(self):
        self.model = Model()
        self.controller = Controller(self.model, self.view)

    def test_add_track_success(self):
        self.set_up()
        track_name = "A Day To Remember - End Of Me"
        duration = 238
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"

        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch("Model.FileManager.update_file") as mock_update_file:
            self.controller.add_track()
            mock_update_file.assert_called_once_with(self.model.tracks)
            self.assertTrue(self.model.check_for_track(track_name))
            self.assertEqual(self.model.read_track(track_name).duration, duration)
            self.assertEqual(self.view.track_listbox.get('end'), track_name)
            del_file()

    def test_add_track_existing(self):
        self.set_up()

        track_name = "A Day To Remember - End Of Me"
        duration = 238
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        self.model.add_track(track_name, duration, location)

        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch("Model.FileManager.update_file"), \
                patch("Controller.messagebox.showerror") as mock_showerror, \
                patch.object(self.view, "show_error"):
            self.controller.add_track()
            mock_showerror.assert_called_once_with('Error', "There is already a soundtrack with such name")
            del_file()

    def test_add_track_incorr_path(self):
        self.set_up()

        location = ""
        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch("Model.FileManager.update_file") as mock_update_file, \
                patch("View.View.show_error") as mock_showerror:
            self.controller.add_track()
            mock_update_file.assert_not_called()
            mock_showerror.assert_not_called()
            del_file()

    def test_remove_track_success(self):
        self.set_up()

        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        with patch("tkinter.filedialog.askopenfilename", return_value=location):
            self.controller.add_track()
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.remove_track()
        self.assertFalse(self.model.check_for_track(track_name))
        self.assertNotIn(track_name, self.view.track_listbox.get(0, "end"))
        del_file()

    def test_remove_track_err(self):
        self.set_up()

        track_name = "A Day To Remember - End Of Me"
        duration = 238
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        self.model.add_track(track_name, duration, location)
        with patch.object(messagebox, "showerror") as mock_showerror:
            self.controller.remove_track()
            mock_showerror.assert_called_once_with("Error", "Choose a track to delete")
            del_file()

    #Poniższe 6 nie działają bo w czasie wykonania funkcji play_track wyskocza błąd rekursji że jest przekroczony jej limit
    # def test_play_track_no_track_selected(self):
    #     self.controller.selected_track_pos = None
    #
    #     with patch.object(View, "show_error") as mock_show_error:
    #         self.controller.play_track()
    #
    #         mock_show_error.assert_called_once_with("Choose track to play")
    #         assert not self.controller.isPlaying
    #
    # def test_play_track_file_not_found(self):
    #     track_to_play = "Track1"
    #     track_path = "/path/to/track.mp3"
    #     self.view.track_listbox.get.return_value = track_to_play
    #     self.model.read_track.side_effect = FileNotFoundError(track_path)
    #
    #     with patch.object(View, "show_error") as mock_show_error:
    #         self.controller.play_track()
    #
    #         mock_show_error.assert_called_once_with(f"No file found: {track_path}")
    #         assert not self.controller.isPlaying
    #
    # def test_play_track_success(self):
    #     track_to_play = "Track1"
    #     track_path = "/path/to/track.mp3"
    #     track_duration = 180
    #     song_length = track_duration * 1000
    #     self.view.track_listbox.get.return_value = track_to_play
    #     self.model.read_track.return_value = Track(track_to_play, track_path, track_duration)
    #
    #     with patch.object(View, "change_play_to_stop_icon") as mock_change_play_to_stop_icon, \
    #             patch.object(View, "set_song_slider") as mock_set_song_slider, \
    #             patch.object(View, "update_song_slider") as mock_update_song_slider, \
    #             patch.object(View, "song_slider_on") as mock_song_slider_on:
    #         self.controller.play_track()
    #
    #         self.controller.mixer.music.load.assert_called_once_with(track_path)
    #         self.controller.mixer.music.play.assert_called_once_with(loops=0)
    #         mock_change_play_to_stop_icon.assert_called_once()
    #         mock_set_song_slider.assert_called_once_with(song_length)
    #         mock_update_song_slider.assert_called_once_with(0)
    #         mock_song_slider_on.assert_called_once_with(track_duration)
    #         assert self.controller.isPlaying
    #         assert self.controller.curr_track_pos == self.controller.selected_track_pos
    #
    #     self.view.show_error.assert_called_once_with("Choose track to play")
    #     assert not self.controller.isPlaying
    # def test_stop_track(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()
    #     del_file()
    #
    # def pause_track(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()
    #     del_file()
    #
    # def unpause_track(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()
    #     del_file()
    #
    # def next_track(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()
    #     del_file()
    #
    # def prev_track(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()
    #     del_file()

    #######################################################################

    def test_song_slider_on(self):
        self.set_up()
        self.view.song_slider_on(185)
        self.assertEqual(self.view.song_time_label.cget("text"), "3:05")
        self.assertEqual(self.view.curr_time_label.cget("text"), "0:00")

    def test_song_position_change(self):
        self.set_up()
        self.controller.mixer.music.load("D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3")
        self.controller.mixer.music.play(loops=0)
        self.view.set_song_slider(500000)
        self.view.song_slider.set(100000)
        self.controller.song_position_change(None)
        self.assertEqual(self.view.curr_time_label.cget("text"), "1:40")

    # def update_slider_pos(self):
    #     self.set_up()
    #     with patch("pygame.mixer.music.stop") as mock_stop:
    #         self.controller.stop_track()
    #         mock_stop.assert_called_once()

    def test_volume_change(self):
        self.set_up()
        self.controller.volume_change(20)
        self.assertAlmostEqual(self.controller.mixer.music.get_volume(), 0.8, places=2)
        del_file()


if __name__ == "__main__":
    unittest.main()
