"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
import operator

Playing = None
Paused = None

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlists = {}
        self.Playing = None
        self.Paused = None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        #print(type(self._video_library.get_all_videos()))
        #print(self._video_library.get_all_videos())
        #print(type(self._video_library.get_all_videos()[0]))
        #print(dir(self._video_library.get_all_videos()[0]))
        if len(self._video_library.get_all_videos())>0:
            print("Here's a list of all available videos: ")
            vidlist = sorted(self._video_library.get_all_videos(),key=operator.attrgetter('_title'))
            for vid in vidlist:
                tags = ""
                if len(vid._tags)>0:
                    tags = vid._tags[0]
                    if len(vid._tags)>1:
                        idx=1
                        while idx<len(vid._tags):
                            tags += " " + vid._tags[idx]
                            idx +=1
                out = vid._title + " (" + vid._video_id + ") [" + tags + "]"
                if vid._flag:
                    out += " - FLAGGED (reason: " + vid._flag + ")"
                print(out)
        else:
            print("No videos available")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        vid = self._video_library.get_video(video_id)
        if vid is None:
            print("Cannot play video: Video does not exist")
        else:
            if vid._flag:
                print("Cannot play video: Video is currently flagged (reason:", vid._flag + ")")
            else:
                if self.Playing:
                    print("Stopping video:", self.Playing._title)
                self.Playing = self._video_library.get_video(video_id)
                self.Paused = None
                print("Playing video:", self.Playing._title)

    def stop_video(self):
        """Stops the current video."""
        
        if self.Playing:
            print("Stopping video:", self.Playing._title)
            self.Playing = None
            self.Paused = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        vids = self._video_library.get_all_videos()
        
        available_vids = []
        i = 0
        while i<len(vids):
            if not vids[i]._flag:
                available_vids.append(vids[i])
            i += 1
                
        if not len(available_vids):
            print("No videos available")
        else:
            randvid = random.choice(available_vids)
            self.play_video(randvid._video_id)        

    def pause_video(self):
        """Pauses the current video."""
        if self.Playing:
            if self.Paused:
                print("Video already paused:", self.Paused._title)
            else:
                print("Pausing video:", self.Playing._title)
                self.Paused = self.Playing
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.Playing:
            if self.Paused:
                print("Continuing video:", self.Paused._title)
                self.Paused = None
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.Playing:
            tags = ""
            if len(self.Playing._tags)>0:
                tags = self.Playing._tags[0]
                if len(self.Playing._tags)>1:
                    idx=1
                    while idx<len(self.Playing._tags):
                        tags += " " + self.Playing._tags[idx]
                        idx +=1
            out = self.Playing._title + " (" + self.Playing._video_id + ") [" + tags + "]"
            if self.Paused:
                out += " - PAUSED"
            print("Currently playing:", out)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.lower() in self._playlists:    #self._playlists.contains_key(lower(playlist_name)):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[playlist_name.lower()] = Playlist(playlist_name)
            print("Successfully created new playlist:",playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() in self._playlists:
            vid = self._video_library.get_video(video_id)
            if vid:
                if vid._flag:
                    print("Cannot add video to my_playlist: Video is currently flagged (reason:", vid._flag + ")")
                else:
                    playlist = self._playlists.get(playlist_name.lower(), None)
                    if video_id in playlist._videos:      #playlist exists, video exists, video in playlist
                        out = "Cannot add video to " + playlist_name + ": Video already added"
                        print(out)
                    else:   #playlist exists, video exists, video not in playlist
                        video = self._video_library.get_video(video_id)
                        playlist._videos[video_id] = video
                        out = "Added video to " + playlist_name + ": " + video._title
                        print(out)
            else:    #playlist exists, video does not exist
                out = "Cannot add video to " + playlist_name + ": Video does not exist"
                print(out)     
        else: 
            out = "Cannot add video to " + playlist_name + ": Playlist does not exist"
            print(out)   

    def show_all_playlists(self):
        """Display all playlists."""
        if len(list(self._playlists.values()))>0:
            print("Showing all playlists:")
            pllist = sorted(list(self._playlists.values()),key=operator.attrgetter('_playlist_title'))
            for pl in pllist:
                print(pl._playlist_title)
        else:
            print("No playlists exist yet")   

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self._playlists:
            print("Showing playlist:",playlist_name)
            playlist = self._playlists.get(playlist_name.lower(), None)
            vidlist = playlist.get_all_playlist_videos()
            if len(vidlist)>0:
                for vid in vidlist:
                    tags = ""
                    if len(vid._tags)>0:
                        tags = vid._tags[0]
                        if len(vid._tags)>1:
                            idx=1
                            while idx<len(vid._tags):
                                tags += " " + vid._tags[idx]
                                idx +=1
                    out = vid._title + " (" + vid._video_id + ") [" + tags + "]"
                    if vid._flag:
                        out += " - FLAGGED (reason: " + vid._flag + ")"
                    print(out)
            else:
                print("No videos here yet")
        else:
            out = "Cannot show playlist " + playlist_name + ": Playlist does not exist"
            print(out)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() in self._playlists:
            if self._video_library.get_video(video_id):
                playlist = self._playlists.get(playlist_name.lower(), None)
                if video_id in playlist._videos:      #playlist exists, video exists, video in playlist
                    video = self._video_library.get_video(video_id)
                    del playlist._videos[video_id]
                    out = "Removed video from " + playlist_name + ": " + video._title
                    print(out)
                else:   #playlist exists, video exists, video not in playlist
                    out = "Cannot remove video from " + playlist_name + ": Video is not in playlist"
                    print(out)
            else:    #playlist exists, video does not exist
                out = "Cannot remove video from " + playlist_name + ": Video does not exist"
                print(out)     
        else:
            out = "Cannot remove video from " + playlist_name + ": Playlist does not exist"
            print(out)   

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self._playlists:
            playlist = self._playlists.get(playlist_name.lower(), None)
            playlist._videos = {}
            print("Successfully removed all videos from", playlist_name)
        else:
            out = "Cannot clear playlist " + playlist_name + ": Playlist does not exist"
            print(out) 

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self._playlists:
            del self._playlists[playlist_name.lower()]
            print("Deleted playlist:", playlist_name)
        else:
            out = "Cannot delete playlist " + playlist_name + ": Playlist does not exist"
            print(out)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        results = {}
        vidlist = self._video_library.get_all_videos()
        for vid in vidlist:
            if search_term.lower() in vid._title.lower() and not vid._flag:
                results[vid._video_id] = vid
                
        results = sorted(results.values(),key=operator.attrgetter('_title'))
        if len(results):
            print("Here are the results for", search_term + ":")
            counter = 1
            for vid in results:
                tags = ""
                if len(vid._tags)>0:
                    tags = vid._tags[0]
                    if len(vid._tags)>1:
                        idx=1
                        while idx<len(vid._tags):
                            tags += " " + vid._tags[idx]
                            idx +=1
                out = str(counter) + ") " + vid._title + " (" + vid._video_id + ") [" + tags + "]"
                print(out)
                counter += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            vidnum = input()
            try:
                vidnum = int(vidnum)
                if vidnum <= len(results):
                    self.play_video(results[vidnum-1]._video_id)
            except ValueError:
                pass
        else:
            print("No search results for", search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        results = {}
        vidlist = self._video_library.get_all_videos()
        for vid in vidlist:
            tags_lower = (tag.lower() for tag in vid._tags)
            if video_tag.lower() in tags_lower and not vid._flag:
                results[vid._video_id] = vid
                
        results = sorted(results.values(),key=operator.attrgetter('_title'))
        if len(results) and video_tag[0] == "#":
            print("Here are the results for", video_tag + ":")
            counter = 1
            for vid in results:
                tags = ""
                if len(vid._tags)>0:
                    tags = vid._tags[0]
                    if len(vid._tags)>1:
                        idx=1
                        while idx<len(vid._tags):
                            tags += " " + vid._tags[idx]
                            idx +=1
                out = str(counter) + ") " + vid._title + " (" + vid._video_id + ") [" + tags + "]"
                print(out)
                counter += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            vidnum = input()
            try:
                vidnum = int(vidnum)
                if vidnum <= len(results):
                    self.play_video(results[vidnum-1]._video_id)
            except ValueError:
                pass
        else:
            print("No search results for", video_tag)


    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        vid = self._video_library.get_video(video_id)
        if vid:
            if vid._flag:
                print("Cannot flag video: Video is already flagged")
            else:
                vid._flag = flag_reason
                if self.Playing == vid:
                    self.stop_video()
                print("Successfully flagged video:", vid._title, "(reason:", flag_reason + ")")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        vid = self._video_library.get_video(video_id)
        if vid:
            if vid._flag:
                vid._flag = None
                print("Successfully removed flag from video:",vid._title)
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")

