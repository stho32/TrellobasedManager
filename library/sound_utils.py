import os
import pygame
from time import sleep
import threading


def play_mp3_async(filename):
    def _play_mp3():
        # Initialize pygame mixer
        pygame.mixer.init()

        # Create the path to the Sounds subdirectory
        sounds_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "Sounds"
        )

        # Create the full path to the MP3 file
        mp3_file = os.path.join(sounds_directory, filename)

        # Load the MP3 file
        pygame.mixer.music.load(mp3_file)

        # Play the MP3 file
        pygame.mixer.music.play()

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            sleep(1)

        # Clean up resources
        pygame.mixer.quit()

    # Start the _play_mp3 function in a separate thread
    playback_thread = threading.Thread(target=_play_mp3)
    playback_thread.start()
