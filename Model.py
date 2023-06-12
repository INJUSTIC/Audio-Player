from FileManager import FileManager


class AudioPlayer:
    def __init__(self):
        self.tracks = FileManager.read_tracks_from_file()

    def add_track(self, name, duration, location):
        track = AudioTrack(name, duration, location)
        self.tracks.append(track)
        FileManager.update_file(self.tracks)

    def remove_track(self, name):
        for track in self.tracks:
            if track.name == name:
                self.tracks.remove(track)
                FileManager.update_file(self.tracks)
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

    def read_track_names(self):
        names = []
        for track in self.tracks:
            names.append(track.name)
        return names

class AudioTrack:
    def __init__(self, name, duration, path):
        self.name = name
        self.duration = duration
        self.path = path
