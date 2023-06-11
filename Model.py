import pygame


class AudioPlayer:
    def __init__(self):
        self.tracks: list = []

    def add_track(self, name, duration, location):
        track = AudioTrack(name, duration, location)
        self.tracks.append(track)

    def remove_track(self, name):
        for track in self.tracks:
            if track.name == name:
                self.tracks.remove(track)
                return

    def check_for_track(self, name):
        for track in self.tracks:
            if track.name == name:
                return True
        return False

    def read_track(self, track_name):
        for track in self.tracks:
            if track.name == track_name:
                return track
        raise ValueError()
class AudioTrack:
    def __init__(self, name, duration, path):
        self.name = name
        self.duration = duration
        self.path = path
