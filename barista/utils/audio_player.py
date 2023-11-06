import pygame


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play_audio(self, audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
            pygame.time.Clock().tick(10)

    def stop_audio(self):
        pygame.mixer.music.stop()
