import pygame


class SampleManager:
    __initialized = False
    __sounds = {}
    
    @staticmethod
    def init():
        pygame.mixer.init(channels=36, buffer=4096)
        SampleManager.__initialized = True

    @staticmethod
    def playFromFile(filename):
        if SampleManager.__initialized is False:
            SampleManager.init()

        try:
            SampleManager.__sounds[filename].stop()
            SampleManager.__sounds[filename].play()
        except KeyError:
            sound = pygame.mixer.Sound(filename)
            SampleManager.__sounds[filename] = sound
            sound.play()
