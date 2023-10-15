#from array import array
from time import sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init

from functionWes import accordoCorrente, TastoCordaDetector, MenuOptions, circleDrawed, arpeggio, strumming, save, clear, showSaved, render, infoNote
from sorting import *

# Creazione schermo
pygame.init()
RES = WIDTH, HEIGHT = 600,400
SCREEN = pygame.display.set_mode(RES)
pygame.display.set_caption("WES")

background_color = (230,170,100) 

#caricamento clock
clock = pygame.time.Clock()

x_pos, y_pos, z_font_size = 528,50, 50


    
while True:     
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]: # ARRESTA
            print("\nQUIT EVENT")
            pygame.quit()
            exit()
    
        # EVENTI "CLICK"    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            """
            DEFINISCO SU QUALE TASTO E QUALE NOTA HO CLICCATO
            e costruisco accordo
            """
            TastoCordaDetector(mousePos)
            
            #infoNote()

            """xx
            DEFINISCO SU OPZIONE-MENU HO CLICCATO
            """
            MenuOptions(mousePos)
            sleep(0.1)
            


        # EVENTI "TASTIERA"
        if (event.type == pygame.KEYDOWN):
            letter = event.unicode
           #[L]s, [X] accordoCorrente
            if letter == 'x':
                print(accordoCorrente)
                print(circleDrawed)
                
                pass
            
            if letter == "p":
                #ChordAnalyser() 
                pass
            #[A]rpeggio, [S]trumming, #Save[d], [C]lear
            if letter == 'a': arpeggio(accordoCorrente)
            if letter == 's': strumming(accordoCorrente)
            if letter == 'd': save()
            if letter == 'c': clear()
            

            
            #[1,2,3,4,5,6,7,8,9,0]    
            try:
                if letter in "1234567890":
                    key = int(letter)
                    showSaved(key)
            except ValueError:
                print("Arrow!")
                
                                      
    #DISEGNO SFONDO   
    SCREEN.fill(background_color)
    #Richiama le 5 funzioni di render 
    render(WIDTH,SCREEN)
    



    pygame.display.update()
    clock.tick(60)
