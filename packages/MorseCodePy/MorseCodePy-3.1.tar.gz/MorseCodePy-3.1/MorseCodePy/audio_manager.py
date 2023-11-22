# Hide the pygame support prompt
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer
from os import path
from time import sleep


class AudioManager:
    def __init__(self, directory: str = 'sounds', file_extension: str = '.wav'):
        self.__directory = directory
        self.__file_extension = file_extension.lower()

        mixer.init()  # Initialize pygame mixer

    # Function to play the dot sound
    def play_dot(self) -> None:
        # Get the absolute path to the sound file within the project directory
        dot_sound_path = path.join(path.dirname(__file__), self.__directory, fr'dot{self.__file_extension}')

        mixer.music.load(dot_sound_path)  # Load the dot.wav sound file
        mixer.music.play()  # Play the sound
        sleep(0.09)  # Add a short delay to simulate the duration of a dot

    # Function to play the dash sound
    def play_dash(self) -> None:
        # Get the absolute path to the sound file within the project directory
        dash_sound_path = path.join(path.dirname(__file__), self.__directory, fr'dash{self.__file_extension}')

        mixer.music.load(dash_sound_path)  # Load the dash.wav sound file
        mixer.music.play()  # Play the sound
        sleep(0.24)  # Add a short delay to simulate the duration of a dash
