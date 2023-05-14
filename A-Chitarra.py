from array import array
from time import sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init

from playerSin import Note

# Creazione schermo
pygame.init()
RES = WIDTH, HEIGHT = 500,400
SCREEN = pygame.display.set_mode(RES)
pygame.display.set_caption("CHITARRA")
background_color = (9,109,140) # HEX:   096D8C
#caricamento clock
clock = pygame.time.Clock()


#Frequenza in Hz, da E2 a E7
frequenze = [ 82.41,  87.31,   92.5,  98.0,  103.83, 110.0, 
    116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 
    
    164.81, 174.61, 185.0,  196.0,  207.65, 220.0, 
    233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 
    
    329.63, 349.23, 369.99, 392.0,  415.3,  440.0, 
    466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 
    
    659.26, 698.46, 739.99, 783.99,  830.61,  880.0, 
    932.33, 987.77, 1046.5, 1108.73, 1174.66, 1244.51, 
    
    1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 
    1864.66, 1975.53, 2093.0, 2217.46, 2349.32, 2489.02, 
    
    2637.02]

frequenzeNomi = ['E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 
    'C3', 'C#3', 'D3', 'D#3', 
    
    'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 
    'C4', 'C#4', 'D4', 'D#4', 
    
    'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 
    'C5', 'C#5', 'D5', 'D#5', 
    
    'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 
    'C6', 'C#6', 'D6', 'D#6', 
    
    'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 
    'C7', 'C#7', 'D7', 'D#7',
    
    'E6']

durata_nota = 50
volumeNote = 0.6

#Posizione x e cose relative a TASTI
primaLineaX = 50 #Corrisponde alla prima linea della chitarra (non la linea 0!)
lunghTasto = 50 #Distanza fra linee

# Coordinate y delle corde
altezzaTastiera = 150

primaCordaY = (HEIGHT-altezzaTastiera)//2 #La prima corda sarà sempre centrata

cordeLista = [] #Posizione delle altre 5 corde
distanzaCorde = altezzaTastiera//5 
for i in range(0,altezzaTastiera+1,distanzaCorde):
    cordeLista.append(primaCordaY+i)

#########################                   ##############################
#########################   Stuff pallini   ##############################
#########################                   ##############################

# QUESTO e' L'ACCORDO CORRENTE!
coordsXY = [] #coordinate dei pallini (x,y)
coordsX = [] #coordinate x dei pallini
coordsY = [] #coordinate y dei pallini
chordsSound = [] #contiene hz delle note selezionate in ordine crescente (da Mi basso a Mi cantino)

def sort_by_y(tuple):
    return -tuple[1]

noteNome = [' ',' ',' ',' ',' ',' ']

def circleSpawn(cordaClicked,tastoClicked):
    #tastoClicked
    global coordsXY, coordsX, coordsY

    #INPUT: (x,y)  ---> (numero che identifica tasto, numero che identifica corda)
    #OUTPUT: (X,Y) ---> (coordinate specifiche dei pallini)
    coordX = primaLineaX-(lunghTasto//2)+  (lunghTasto)*tastoClicked
    coordY = primaCordaY+(distanzaCorde*(cordaClicked-1))
    center = (coordX,coordY)

    #ELIMINA CERCHIO
    if center in coordsXY: #Se clicci su cerchio già cliccato, lo rimuove dalle 3 listt
        print("\nAlready clicked this\n")
        i = coordsXY.index(center)
        print(i)
        coordsX.pop(i)
        coordsY.pop(i)
        coordsXY.pop(i)
        noteNome[cordaClicked-1] = " "

    #AGGIUNGE CERCHIO
    else:  
        #AGGIUNGE CERCHIO SU STESSA CORDA
        if coordY in coordsY: #cambia note sulla stessa corda
            print(f'coordY ({coordY}) è in coordsY')
            i = coordsY.index(coordY)
            coordsX.pop(i)
            coordsY.pop(i)
            coordsXY.pop(i)


        #AGGIUNGE ALLA LISTA coordsXY SOLO SE LA NOTA NON E' MAI STATA REGISTRATA (EVITARE)
        if (coordX,coordY) not in coordsXY: # aggiunge note
            coordsX.append(coordX)         # se la nota non è stata aggiunta
            coordsY.append(coordY)
            coordsXY.append(center)

            ogcordaClicked = cordaClicked
            cordaClicked = (cordaClicked-7)*-1      # Ad ogni corda è collegato un numero legato alla posizione y, il mi cantino sarà 1, il mi basso sarà 6, # 
                                                    # Dunque all'aumentare dell'altezza "fisica" ("andando verso il basso" nella schermata pygame),
                                                    # Aumenta l'altezza "in frequenza" ---> in quanto cordaClicked sarà legato alle frequenze in Hz
                                                    # Le due grandezze sono inversamente proporzionali --> con questa riga le rendiamo direttamente proporzionali


            m = (((cordaClicked-1)*5)+tastoClicked)         # indice della frequenza cliccata
            if cordaClicked == 5 or cordaClicked == 6:
                m = (((cordaClicked-1)*5)+tastoClicked)-1   # indice della frequenza cliccata
            

            print(f'Frequenza[{m}] = {frequenze[m]} Hz')
            print(f'{frequenzeNomi[m]} = {frequenze[m]} Hz')
            noteNome[ogcordaClicked-1] = frequenzeNomi[m]

            Note(frequenze[m],volume=volumeNote).play(durata_nota)      #SUONA NUOTA APPENA CLICCATA

    print(f'Chords: {coordsXY}')
    sleep(0.1)

isPressed = False
#nTasti
nTasti = 9

keys = pygame.key.get_pressed()

savedChords = []
allChordsSaved = ["Empty"]

def arpeggio():
    print("[A]rpeggio")
    Note(frequenze[m],volume=volumeNote).play(durata_nota)
    sleep(0.2)

def strumming():
    print("[S]trumming")
    Note(frequenze[m],volume=volumeNote).play(durata_nota)

def clear(coordsXY,coordsX,coordsY,chordsSound):
    coordsXY.clear()
    coordsX.clear()
    coordsY.clear()
    chordsSound.clear()
    return coordsXY,coordsX,coordsY,chordsSound

def salvataggioAccordo(chordSaved,allChordsSaved):
    print("\nCreazione accordo!")
    print(f'Accordo che stai tentando di salvare: {chordSaved}')
    
    if (len(chordSaved)) != 0:               # Se chordSaved non è vuoot
        if chordSaved in allChordsSaved:     # Non far nulla se l'accordo è già stato salvato
            print("Accordo già salvato")                                                           
        else:                               # Altrimenti "salvalo" --> Aggiungilo alla lista allChordsSaved
            print(f'\nAccordo salvato al numero: {len(allChordsSaved)}')
            print(f'Indici frequenze accordo: {chordSaved}')
            allChordsSaved.append(chordSaved) 
            print(f'Lista accordi salvati: {list(enumerate(allChordsSaved))}')
    
    print(allChordsSaved)
    sleep(0.1)

def suonaSalvati():
    try:
        indexSaved = int(event.unicode)                 # indexSaved -> numero selezionato ("input" dell'user)
        if indexSaved < len(allChordsSaved):            # Se indexSaved è all'interno della lista allChordsSaved
            print(f'L\'accordo {allChordsSaved[indexSaved]} salvato al n.{indexSaved}') # Stampa ...

            for freq in allChordsSaved[indexSaved]:                                     # Suona tutte le frequenze (le note)
                print(f'Sto suonando l\'accordo salvato al n.{indexSaved}')             # di cui è composto il detto accordo
                Note(frequenze[freq],volume=volumeNote).play(durata_nota)                     # accordo = allChordsSaved[indexSaved] --> sarà una lista composta di frequenze

        else:
            print(f'Nessun accordo al n.{indexSaved}') # Altrmineti
    except ValueError:
        print("ValueError in suonaSalvati function")

def draw():
    #DISEGNA CERCHI
    i = 0
    for note in coordsXY:
        pygame.draw.circle(SCREEN, (0,0,0), (coordsX[i],coordsY[i]),10)
        i+=1
    
    #DISEGNA LINEE E CORDE
    for x in range(primaLineaX,(lunghTasto*nTasti)+1,lunghTasto):
        lines = [pygame.draw.line(SCREEN, (0,0,0), (x,primaCordaY),(x,primaCordaY+altezzaTastiera),3)]
    for k in range(6):
        corda = pygame.draw.line(SCREEN, (0,0,0), (primaLineaX,cordeLista[k]),(lunghTasto*nTasti, cordeLista[k]),3)
    linea_0 = [pygame.draw.line(SCREEN, (0,0,0), (primaLineaX//2,primaCordaY),(primaLineaX//2,primaCordaY+altezzaTastiera),3)]

menu_rects = []
def drawMenu():
    #Disegna quadrati del menù
    rect_color = pygame.Color(3,43,56)
    rect_a = pygame.draw.rect(SCREEN, rect_color, (10, 10, 30, 30))
    rect_s = pygame.draw.rect(SCREEN, rect_color, (60, 10, 30, 30))
    rect_c = pygame.draw.rect(SCREEN, rect_color, (110, 10, 30, 30))
    rect_spacebar = pygame.draw.rect(SCREEN, rect_color, (160, 10, 30, 30))
    menu_rects.append(rect_a)
    menu_rects.append(rect_s)
    menu_rects.append(rect_c)
    menu_rects.append(rect_spacebar)

    #PRINTA LETTERE
    image = pygame.image.load("menu/gomma.png")
    new_image = pygame.transform.scale(image, (50, 50))

    #SCREEN.blit(new_image,(0,0))


    #PRINTA LETTERE
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    text_a = font.render('A', True, (250,250,250))
    textRect_a = text_a.get_rect()
    textRect_a.center = (25, 25)

    text_s = font.render('S', True, (250,250,250))
    textRect_s = text_s.get_rect()
    textRect_s.center = (75, 25)

    text_c = font.render('C', True, (250,250,250))
    textRect_c = text_c.get_rect()
    textRect_c.center = (125, 25)

    SCREEN.blit(text_a, textRect_a)
    SCREEN.blit(text_s, textRect_s)
    SCREEN.blit(text_c, textRect_c)

   


def nomeNote():
    font_nota = pygame.font.Font('freesansbold.ttf', 20)
    i = 0
    for nome in noteNome:
        nota = font_nota.render(nome, True, (250,250,250))
        notaRect = nota.get_rect()
        notaRect.center = (WIDTH-25, primaCordaY+(distanzaCorde*i))
        SCREEN.blit(nota, notaRect)
        i += 1
    
while True:
    gotMenuChoice = False
    aMenuArpeggio, aMenuStrumming, aMenuSaving, aMenuCleaning = False, False, False, False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            print("\nQUIT EVENT")
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            isPressed = True
            print(f'Mouse Down event, isPressed: {isPressed}')

            i = 0
            for rect in menu_rects:                                 # Controlla, per ogni singolo rect
                if rect.collidepoint(pygame.mouse.get_pos()):       # Se questo viene cliccado dal mouse
                    print(f'MI HAI CLICCATO! -> {i}')               # in quel caso
                    gotMenuChoice = True                            # l'indice i indicherà quale quadrato è stato cliccato 
                    if i == 0: aMenuArpeggio = True                 # 0 ---> Arpeggio
                    elif i == 1: aMenuStrumming = True              # 1 ---> Strumming
                    elif i == 2: aMenuCleaning = True               # 2 ---> Cleaning
                    elif i == 3: aMenuSaving = True                 # 3 ---> Saving
                    break
                i += 1

        if (gotMenuChoice) or (event.type == pygame.KEYDOWN):
            if (event.type == pygame.KEYDOWN): print("\nKEYDOWN EVENT\n")
            if (gotMenuChoice): print("\nMENUCHOICE EVENT\n")

            saving = False
            playChord = sorted(coordsXY, key=sort_by_y) # ((( Lista con coordinate pallini in ordine decrescente di y, da MI BASSO a MI CANTINO)))
                                                        # playChord = coordsXY con le coordinate in ordine decrescente di y (x,y)
                                                        # Il valore di y coorrisponde alla coordinata della corda
                                                        # Ponendolo in decrescenza playChord avrà i pallini ordinati dal MI basso al MI cantino
            
            chordSaved = [] #accordo da salvare, conterrà indici delle frequenze

            for circle in playChord:  #ciclo che si ripete per i pallini presenti nell'accordo da suonare
                whatTasto = ((circle[0]-primaLineaX)//lunghTasto)+1 
                whatChord = (((circle[1]-primaCordaY-(distanzaCorde//2))//(distanzaCorde) +1) -5)*(-1)
                #Indice della frequenza

                m = ((((whatChord)*5)+whatTasto)) # La tastiera sarebbe al contrario
                if m > 19:      # La quinta corda (SI) non corrisponde a whatChord*5 (4*5Hz), cioè il 20° Hz, ma al 24°
                    m -= 1

                print(f'Corda: {whatChord}, Tasto: {whatTasto}, Indice frequenza: {m}')
                chordSaved.append(m)
                
                # ARPEGGIO, STRUMMING o SALVATAGGIO 
                # triggered      TRY --> se viene premuto il tasto 's','a',' '
                # triggered   EXCEPT --> se viene premuto il menu
                try:
                    evento = event.unicode
                    if event.unicode == 'a': arpeggio()
                    if event.unicode == 's': strumming()
                    if event.unicode == ' ': saving = True, print(f'chordSaved-->{chordSaved}')
                except AttributeError:
                    if aMenuArpeggio: arpeggio()                 # arpeggio
                    if aMenuStrumming: strumming()               # strumming
                    if aMenuSaving: saving = True                # salvataggio accordo
                    else: print("AttributeError! 1 (nel for)")
            
            # Salvataggio dell'accordo
            if saving:
                salvataggioAccordo(chordSaved,allChordsSaved)
                saving = False
            
            # CLEARm SUONARE SALVATI
            # triggered      TRY --> se viene premuto il tasto ('c','123456789')
            # triggered   EXCEPT --> se viene premuto il menu
            try: 
                evento = event.unicode
                if evento == 'c': clear(coordsXY,coordsX,coordsY,chordsSound)
                if evento in '123456789': suonaSalvati()
            except AttributeError:
                if aMenuCleaning: clear(coordsXY,coordsX,coordsY,chordsSound)
                elif aMenuSaving: print("Collegare funzione suona salvati al pulsante")
                else: print("AttributeError! 2 (sotto CleanAndSave)")
        
        if isPressed:
            #Siamo all'interno della chitarra?
            isInsideManico_X = (primaLineaX-lunghTasto < pygame.mouse.get_pos()[0] < lunghTasto*nTasti) 
            isInsideTastiera_Y = (primaCordaY-(distanzaCorde//2) < pygame.mouse.get_pos()[1] < primaCordaY+altezzaTastiera+(distanzaCorde//2) )

            if isInsideManico_X and isInsideTastiera_Y:
                whatTasto = ((pygame.mouse.get_pos()[0]-primaLineaX)//lunghTasto)+1 
                whatCord = (pygame.mouse.get_pos()[1]-primaCordaY-(distanzaCorde//2))//(distanzaCorde) +2
                print(f'X: {whatCord} Y: {whatTasto}  --> Corda,Tasto: ({whatCord},{whatTasto})')
                #noteNome[whatCord-1] = str(whatTasto)
                circleSpawn(whatCord,whatTasto)
     
    SCREEN.fill(background_color)
    draw()
    drawMenu()

    nomeNote()    

    isPressed = False
    pygame.display.update()
    clock.tick(60)
