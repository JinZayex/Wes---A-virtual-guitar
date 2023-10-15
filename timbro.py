from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init

print("ciao")

import math

class Note(Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        sample_rate = get_init()[0]
        period = int(round(sample_rate / self.frequency))
        samples = array("h", [00] * period)

        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        # calcola l'incremento dell'angolo per ogni campione
        increment = 2.0 * math.pi * self.frequency / sample_rate

        # genera le forme d'onda sinusoidali
        angles = [0.0, 0.0, 0.0]
        increments = [increment, increment * 2, increment * 3]  # frequenze 440, 880, 1320 Hz
        weights = [0.6, 0.3, 0.1]  # pesi delle singole forme d'onda

        for i in range(period):
            # somma i campioni delle singole forme d'onda con i relativi pesi
            sample = 0
            for j in range(len(angles)):
                sample += weights[j] * amplitude * math.sin(angles[j])
                angles[j] += increments[j]
            samples[i] = int(sample)

        return samples 


pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
pygame.init()
print("Carico il file timbro.py")

#Note(440.0,0.2).play(300)
#sleep(2)

print("Chiami la musica, \"timbro.py\" risponde")






"""
Per creare un suono che simuli una chitarra, 
puoi utilizzare la sintesi additiva, 
ovvero combinare diverse forme d'onda 
sinusoidali con frequenze multiple della 
frequenza fondamentale (o "nota base") per 
creare un suono più complesso. 
Questo processo è noto come "sintesi armonica".

In pratica, puoi modificare il metodo build_samples 
della classe Note per generare più forme d'onda sinusoidali 
e combinare i loro campioni per creare un suono più ricco. 
Ad esempio, potresti provare a generare forme d'onda sinusoidali 
con frequenze multiple della frequenza fondamentale 
(ad esempio, la nota La a 440 Hz) e sommarle con pesi differenti 
per creare un suono simile a quello di una chitarra.

Ecco un esempio di come potresti modificare il codice 
per generare tre forme d'onda sinusoidali con 
frequenze 440 Hz, 
880 Hz e 
1320 Hz (3° armonica), 
rispettivamente, e sommarle per creare un suono composto:

Ovviamente, puoi sperimentare con diverse frequenze e pesi 
delle forme d'onda sinusoidali per creare il suono desiderato. 
Inoltre, per ottenere un suono più realistico, 
potresti considerare anche l'aggiunta di un leggero effetto 
di distorsione o saturazione, che simula la risposta non lineare 
degli amplificatori e dei diffusori delle chitarre reali.

"""
