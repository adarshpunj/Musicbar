from enum import Enum 
import subprocess

class Command(Enum):

    START_PLAYLIST = 'play playlist "{}"'
    PLAYPAUSE = 'playpause playlist "{}"'
    PLAY_NEXT_TRACK = 'play next track'
    PLAY_PREVIOUS_TRACK = 'play previous track'
    STOP_TRACK = 'stop'
    GET_CURRENT_TRACK_NAME = 'get {{name}} of current track'
    GET_TRACK_POSITION = 'player position'
    GET_TRACK_NAME_BY_ID = 'get {{name}} of track id {}'
    PLAY_TRACK_BY_ID = 'play track id {}'
    SEARCH_IN_PLAYLIST = 'search playlist {} for "{}"'
    GET_PLAYLIST_NAME_BY_ID = 'get {{name}} of playlist {}'
    GET_CURRENT_PLAYLIST_NAME = 'get {{name}} of current playlist'
    GET_PLAYLIST_COUNT = 'count playlist'
    QUIT = 'quit'

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)


def exec_command(command: Command, *args) -> str:

    SHELL_ARGS = ['osascript', '-e', 'tell app "Music" to {}']
    SHELL_ARGS[2] = SHELL_ARGS[2].format(
            str(command).format(*args)
        )
    output = subprocess.run(SHELL_ARGS, capture_output=True)
    output = output.stdout.decode("utf-8")
    return output.strip()