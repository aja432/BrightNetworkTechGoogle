"""A video playlist class."""
from .video import Video


class Playlist:
    """A class used to represent a Playlist."""
    
    def __init__(self, playlist_title: str):
        """Video constructor."""
        self._playlist_title = playlist_title
        self._videos = {}

    @property
    def playlist_title(self) -> str:
        """Returns the title of a playlist."""
        return self._playlist_title

    def get_all_playlist_videos(self):
        """Returns all available video information."""
        return list(self._videos.values())