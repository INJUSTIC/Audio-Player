import os
import pickle


class FileManager:
    @staticmethod
    def read_tracks_from_file():
        file_path = 'tracks.pkl'
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "rb") as file:
                tracks = pickle.load(file)
                return tracks
        else:
            with open(file_path, "w"):
                return []

    @staticmethod
    def update_file(tracks):
        with open('tracks.pkl', "wb") as file:
            pickle.dump(tracks, file)
