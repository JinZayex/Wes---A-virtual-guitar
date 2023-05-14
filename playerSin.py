from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init

print("ciao")

import math

class Note(Sound):
    #Costruttore che ha come input la frequenza ("altezza" della nota) e volume
    def __init__(self, frequency, volume):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        sample_rate = get_init()[0]  #frequenza di campionamento (campioni al secondo) ---> è in pre_init
        period = int(round(sample_rate / self.frequency))
        samples = array("h", [0] * period)
        
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        
        # calcola l'incremento dell'angolo per ogni campione
        increment = 2.0 * math.pi * self.frequency / sample_rate

        # genera l'onda sinusoidale
        angle = 0.0
        for i in range(period):
            samples[i] = int(amplitude * math.sin(angle))
            angle += increment
            #print(i, samples[i])
        return samples


pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
pygame.init()
print("CIAO! Vengo dal file playerSin.py")

#Note(440.0,0.6).play(1000)
#sleep(2)

print("Chiami la musica, \"playerSin.py\" risponde")






