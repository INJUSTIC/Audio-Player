import os
import unittest
from unittest.mock import patch
from tkinter import messagebox
from tkinter import *
from Controller import Controller
from Model import Model
from View import View
from PIL import Image, ImageTk


def del_file():
    if os.path.exists('tracks.pkl'):
        os.remove('tracks.pkl')


class TestAudioPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.view = View(Tk())

    def set_up(self):
        self.view.track_listbox.delete(0, "end")
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

    def test_add_track_already_exist(self):
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

    def test_play_track_success(self):
        self.set_up()
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        with patch("tkinter.filedialog.askopenfilename", return_value=location):
            self.controller.add_track()
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.assertTrue(self.view.song_slider.winfo_width(), 238)
        self.assertTrue(self.controller.mixer.music.get_busy())
        self.assertTrue(self.controller.isPlaying)
        self.assertTrue(self.view.song_time_label.cget("text") == "3:58")
        del_file()

    def test_play_track_no_track_selected(self):
        self.set_up()
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        with patch("tkinter.filedialog.askopenfilename", return_value=location), \
                patch.object(self.controller.view, "show_error") as mock_show_error:
            self.controller.add_track()
            self.controller.play_track()
            mock_show_error.assert_called_once_with("Choose track to play")
            self.assertFalse(self.controller.isPlaying)
        del_file()

    # def test_play_track_no_file_found(self):
    #     self.set_up()
    #     location = "D:/Users/vopor/Music/Billy Talent - Fallen Leaves.mp3"
    #     with patch("tkinter.filedialog.askopenfilename", return_value=location), \
    #          patch.object(self.controller.view, "show_error") as mock_show_error:
    #         self.controller.add_track()
    #         self.view.select_track(0)
    #         self.controller.listbox_select()
    #         os.remove(location)
    #         self.controller.play_track()
    #         mock_show_error.assert_called_once_with(f"No file found: {location}")
    #     self.assertFalse(self.controller.isPlaying)
    #     del_file()

    def test_stop_track(self):
        self.set_up()
        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration = 238
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.controller.stop_track()
        self.assertFalse(self.controller.mixer.music.get_busy())
        del_file()

    def test_pause_track(self):
        self.set_up()
        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration = 238
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.controller.pause_track()
        self.assertFalse(self.controller.isPlaying)
        self.assertTrue(self.controller.isPaused)
        self.assertFalse(self.controller.mixer.music.get_busy())
        del_file()

    def test_unpause_track(self):
        self.set_up()
        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration = 238
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.controller.pause_track()
        self.controller.unpause_track()
        self.assertTrue(self.controller.isPlaying)
        self.assertFalse(self.controller.isPaused)
        self.assertTrue(self.controller.mixer.music.get_busy())
        del_file()

    def test_next_track_success(self):
        self.set_up()
        del_file()
        track_name1 = "A Day To Remember - End Of Me"
        location1 = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration1 = 238
        self.model.add_track(track_name1, duration1, location1)
        self.view.insert_track(track_name1)
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.controller.next_track()
        print(self.controller.curr_track_pos[0])
        self.assertTrue(self.controller.curr_track_pos[0] == 0)
        self.assertTrue(self.controller.mixer.music.get_busy())
        track_name2 = "Aero Chord - Surface"
        location2 = "D:/Users/vopor/Music/Aero Chord - Surface.mp3"
        duration2 = 254
        self.model.add_track(track_name2, duration2, location2)
        self.view.insert_track(track_name2)
        self.controller.next_track()
        self.assertTrue(self.controller.curr_track_pos[0] == 1)
        self.assertTrue(self.controller.mixer.music.get_busy())
        track_name3 = "AJR - Weak"
        location3 = "D:/Users/vopor/Music/AJR - Weak.mp3"
        duration3 = 201
        self.model.add_track(track_name3, duration3, location3)
        self.view.insert_track(track_name3)
        self.controller.next_track()
        self.assertTrue(self.controller.curr_track_pos[0] == 2)
        self.assertTrue(self.controller.mixer.music.get_busy())
        del_file()

    def test_next_track_fail(self):
        self.set_up()
        self.controller.next_track()
        self.assertEqual(self.controller.curr_track_pos, None)
        self.assertEqual(self.controller.selected_track_pos, None)
        self.assertFalse(self.controller.mixer.music.get_busy())
        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration = 238
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)
        self.controller.next_track()
        self.assertEqual(self.controller.curr_track_pos, None)
        self.assertEqual(self.controller.selected_track_pos, None)
        self.assertFalse(self.controller.mixer.music.get_busy())
        del_file()

    def test_prev_track_success(self):
        self.set_up()
        track_name1 = "A Day To Remember - End Of Me"
        location1 = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration1 = 238
        self.model.add_track(track_name1, duration1, location1)
        self.view.insert_track(track_name1)
        self.view.select_track(0)
        self.controller.listbox_select()
        self.controller.play_track()
        self.controller.prev_track()
        self.assertTrue(self.controller.curr_track_pos[0] == 0)
        self.assertTrue(self.controller.mixer.music.get_busy())
        track_name2 = "Aero Chord - Surface"
        location2 = "D:/Users/vopor/Music/Aero Chord - Surface.mp3"
        duration2 = 254
        self.model.add_track(track_name2, duration2, location2)
        self.view.insert_track(track_name2)
        self.controller.prev_track()
        self.assertTrue(self.controller.curr_track_pos[0] == 1)
        self.assertTrue(self.controller.mixer.music.get_busy())
        track_name3 = "AJR - Weak"
        location3 = "D:/Users/vopor/Music/AJR - Weak.mp3"
        duration3 = 201
        self.model.add_track(track_name3, duration3, location3)
        self.view.insert_track(track_name3)
        self.controller.prev_track()
        self.assertTrue(self.controller.curr_track_pos[0] == 0)
        self.assertTrue(self.controller.mixer.music.get_busy())
        del_file()

    def test_prev_track_fail(self):
        self.set_up()
        self.controller.next_track()
        self.assertEqual(self.controller.curr_track_pos, None)
        self.assertEqual(self.controller.selected_track_pos, None)
        self.assertFalse(self.controller.mixer.music.get_busy())
        track_name = "A Day To Remember - End Of Me"
        location = "D:/Users/vopor/Music/A Day To Remember - End Of Me.mp3"
        duration = 238
        self.model.add_track(track_name, duration, location)
        self.view.insert_track(track_name)
        self.controller.prev_track()
        self.assertEqual(self.controller.curr_track_pos, None)
        self.assertEqual(self.controller.selected_track_pos, None)
        self.assertFalse(self.controller.mixer.music.get_busy())
        del_file()

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

    def update_slider_pos(self):
        self.set_up()
        with patch("pygame.mixer.music.stop") as mock_stop:
            self.controller.stop_track()
            mock_stop.assert_called_once()

    def test_volume_change(self):
        self.set_up()
        self.controller.volume_change(20)
        self.assertAlmostEqual(self.controller.mixer.music.get_volume(), 0.8, places=2)
        del_file()


if __name__ == "__main__":
    unittest.main()
