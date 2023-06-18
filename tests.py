import unittest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from tkinter import *
from Controller import Controller
from Model import Model
from View import View


class TestAudioPlayer(unittest.TestCase):

    def setUp(self):
        self.view = View(Tk())
        self.model = Model()
        self.controller = Controller(self.model, self.view)

    def test_add_track_success(self):
        track_name = "A Day To Remember - End Of Me"
        duration = 238
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"

        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch("Model.FileManager.update_file") as mock_update_file:
            self.controller.add_track()
            mock_update_file.assert_called_once_with(self.model.tracks)
            self.assertTrue(self.model.check_for_track(track_name))
            assert self.model.read_track(track_name).duration == duration
            assert track_name == self.view.track_listbox.get('end')

    def test_add_track_existing(self):
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

    def test_add_track_incorr_path(self):
        location = ""
        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch("Model.FileManager.update_file") as mock_update_file, \
                patch("View.View.show_error") as mock_showerror:
            self.controller.add_track()
            mock_update_file.assert_not_called()
            mock_showerror.assert_not_called()

    def test_remove_track(self):
        track_name = "Test Track"
        self.model.add_track(track_name, 180, "/path/to/track.mp3")
        self.view.insert_track(track_name)

        with patch.object(messagebox, "showerror") as mock_showerror, \
                patch("Model.FileManager.update_file") as mock_update_file:
            # Test removing a selected track
            self.view.select_track(0)
            self.controller.remove_track()
            mock_update_file.assert_called_once_with([])
            self.assertFalse(self.model.check_for_track(track_name))
            self.assertNotIn(track_name, self.view.track_listbox.get(0, "end"))

            # Test removing an unselected track
            self.view.select_track(0)
            self.controller.remove_track()
            mock_showerror.assert_called_once_with("Error", "Choose a track to delete")

    def test_play_track(self):
        track_name = "Test Track"
        duration = 180
        location = "/path/to/track.mp3"
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)

        with patch("pygame.mixer.music.load"), \
                patch("pygame.mixer.music.play"), \
                patch.object(View, "set_song_slider"), \
                patch.object(View, "song_slider_on"), \
                patch.object(View, "change_play_to_stop_icon") as mock_change_play_to_stop_icon:
            self.view.select_track(0)
            self.controller.play_track()

            mock_change_play_to_stop_icon.assert_called_once()

    def test_stop_track(self):
        with patch("pygame.mixer.music.stop") as mock_stop:
            self.controller.stop_track()
            mock_stop.assert_called_once()

    # Add more test cases for other methods in the Controller class


if __name__ == "__main__":
    unittest.main()
