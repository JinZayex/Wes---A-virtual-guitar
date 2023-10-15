import pygame
from time import sleep
from timbro import Note

from sorting import insertionSort

"""
variabili play
e creazione della lista frequenza
"""
volumeNote = 0.4
durataNota = 50

E2 = 82.41          #frequenza di partenza = E2
st = 2**(1/12)      #semitono  ---> moltiplicare la nota x per st, ti da la nota x+1 (mi*st=fa)

frequenze = [E2]    #lista con tutte le frequenze da E2 a E7   

for i in range(12*5):
    E2 = E2*st
    frequenze.append(E2)
    
""", 
variabili arpeggio e strumming
"""
arpTempo = 0.3
strTempo = 0.02




"""
variabili renderTastiera
"""
dimRect = (rBase, rAltezza) = (30, 145)     #Dimensioni rettangoli neri
nRect = 12     #is it stable?                #Numero rettangoli da disegnare
distRect = 10                               #Distanza fra rettangoli           
O = (Ox, Oy) = (70,140)                     #Origine (punto in alto a sinistra del primo rettangolo)
passo = distRect+rBase                      #Ad ogni "passo" creo il nuovo punto in alto a destra del nuovo rettangolo da creare (spostamento = dimensione del rettangolo più distanza fra rettangoli))
raggioBordi = 5                             #Smussatura
coloreRect = (0,0,0)                        #Colore rettangolo
################
headSpacing = 10                            #Spazio che intercorre fra corda "più in alto" e testa rettangolo (Ox) ---> (lo stesso spazio dovrà intercorrere fra corda "più in basso" e piede del rettangolo)
C = (Cx,Cy) = (Ox, Oy+headSpacing)          #C Coordinata dell'inizio della prima corda
nCorde = 6                      
lunghezCorda = (nRect+1)*passo + passo//2
distCorde = rAltezza//nCorde
coloreCorde = (230,230,230)
cordeDim = 5

"""
renderMenu
"""
menuH = 30
menuColor = (30,30,30)






"""
variabili circleCreation e               variabili renderTastiera
"""
coloreCircles = (233,0,0)

accordoCorrente = {0:None,1:None,2:None,3:None,4:None,5:None}

circleDrawed = {"E_low": None, "A":None, "D":None, "G":None, "B":None, "E_high":None}

noteList = list(circleDrawed.keys())

"""
"""


"""
variabili save
"""

accordiSalvati = {}    # Lista che contiene accordiCorrente, accordoCorrente è una lista che contiene tuple (x,y) 
saveIndex = 0          # Indice al quale salvare l'accordo (se arriva a 9, torna 0 --> permette di sovrascrivere)
maxSavables = 9        # maxSavables


coord = (-1,-1)


tolleranza = 3          #Tolleranza prima dell'angolo upSx in cui il corrente tasto è cliccato
tolleranzaSu = 7
tolleranzaGiu = 8

"""
analysis variables
"""

CHORDANALYSED = []
CHORD_TYPES = [  ([0,4,7]," "),                     #00: M (0)*
                ([0,3,7],"m"),                     #01: m*
                ([0,3,6],"dim"),                     #02: dim*
                ([0,5,7],"sus4"),                     #03: sus4 = Suspended Fourth*
                ([0,5,7,10],"7sus4"),                  #04: 7sus4 = Dominant7, Suspended Fourth*
                ([0,4,7,11],"M7"),                  #05: M7 = Major Seventh*
                ([0,3,7,11],"mMa7"),                  #06: mMa7 = minor Major Seventh*
                ([0,3,7,10],"m7**"),                  #07: m7 = minor Seventh*
                ([0,4,7,10],"m7**"),                  #08: m7 = Dominant Seventh*
                ([0,3,6,9],"dim7"),                   #09: dim7 = Diminished Seventh*
                ([0,4,8,11],"#5Maj7"),                  #10: #5Maj7 = Major Seventh, Raised Fifth*
                ([0,4,8,10],"#57"),                  #11: #57 = Dominant Seventh, Raised Fifth*
                ([0,4,8],"#5"),                     #12: #5 = Majör Raised Fifth*
                ([0,3,6,10],"m7b5"),                  #13: m7b5 = minor 7th, Flat Fifth*
                ([0,4,6,10],"M7b5"),                  #14: M7b5 = Major 7th, Flat Fifth*                     
                
                ([0,2,4,7],"add9*"),                   #15: add9 = Major additional Ninth*
                ([0,2, 4,7,11],"Maj7(9)"),                #16: Maj7(9) = Major Seventh, plus Ninth*
                ([0,2,4,7,10],"7(9)"),                #17: 7(9) = Dominant Seventh, plus Ninth*
                ([0,3,7,2],"add9*"),                   #18: add9 = minor additional Ninth*
                ([0,2,3,7,11],"m9(Maj7)"),                #19: m9(Maj7) = minor Major Seventh, plus Ninth*
                ([0,2,3,7,10],"m7(9)"),                #20: m7(9) = minor Seventh, plus Ninth*
                
                ([0,4,6,7,11],"Maj7(#11)"),                #21: Maj7(#11) = Major Seventh, Sharp Eleventh*
                ([0,2,4,6,7,11],"Maj9(#11)"),              #22: Maj9(#11) = Major Seventh, Sharp Eleventh, plus Ninth*
                ([0,4,6,7,10],"7(#11)"),                #23: 7(#11) =  Dom. Seventh, Sharp Eleventh*
                ([0,2,4,6,7,10],"9(#11)"),              #24: 9(#11) =  Dom. Seventh, Sharp Eleventh, plus Ninth*
                ([0,4,7,9,10],"7(13)"),                #25: 7(13) =  Dom. Seventh, Thirteenth*
                ([0,2,4,7,9,10],"9(13)"),              #26: 9(13) =  Dom. Seventh, Thirteenth, plus Ninth*
                ([0,1,4,7,10],"7(b9)"),                #27: 7(b9) = Dominant Seventh, plus Flattened Ninth*
                ([0,4,7,8,10],"7(b13)"),                #28: 7(b13) =  Dom. Seventh, Flattened Thirteenth*
                ([0,1,4,7,8,10],"7(b13b9)"),              #29: 7(b13b9) =  Dom. Seventh, Flattened Thirteenth, plus Flattened Ninth*
                ([0,1,4,5,7,6,10],"7(b13b911)"),            #30: 7(b13b911) =  Dom. Seventh, Flattened Thirteenth plus Flattenet Ninth, plus Eleventh*
                ([0,3,4,7,10],"7(#9)"),                #31: 7(#9) = Dominant Seventh, plus Sharp Ninth*
                ([0,3,5,7,10],"m7(11)"),                #32: m7(11) = minor Seventh, plus Eleventh*
                ([0,2,3,5,7,10],"m9(11)"),              #33: m9(11) = minor Seventh, plus Eleventh, plus Ninth*
                ([0,0,0], "")]                     #34: Dummy


nomiNote = {0:"E", 1:"F", 2:"F#", 3:"G", 4:"G#", 5:"A", 6:"A#", 7:"B", 8:"C", 9:"C#", 10:"D", 11:"D#"}

noteCorrentiId = []    # accordo corrente tradotto in numeri (guarda chiavi nomiNote)
nomeCorrentiId = []    # accordo corrente tradotto in note   (guarda valori nomiNote)


possibleCord = {}   # dizionario che ha come chiave la nota fondamentale
                    # e come valore una lista con i valori dei rapporti (es. 7 = 5a giusta)
"""
variabili MenuOptions
"""
font_size = 20
font_choice = pygame.font.Font('freesansbold.ttf', font_size)
print("YOUR FONT CHOICE IS", font_choice)



font_color = (230,230,230)
fontbgColor = menuColor
 

TESTO_arpeggio = font_choice.render('Arpeggio', True, font_color, fontbgColor)
TESTO_strumming = font_choice.render('Strumming', True, font_color, fontbgColor)
TESTO_save = font_choice.render('Save', True, font_color, fontbgColor)
TESTO_clear = font_choice.render('Clear', True, font_color, fontbgColor)





TxRect_arpeggio = TESTO_arpeggio.get_rect()
TxRect_strumming = TESTO_strumming.get_rect()
TxRect_save = TESTO_save.get_rect()
TxRect_clear = TESTO_clear.get_rect()



ARP_WID, STRU_WID, SAVE_WID, CLEA_WID, ANAL_WID = 63,79,32,35, 35                            #lunghezza (base) dei testi
arp_x, stru_x, save_x, clea_x = 7,76,162,199                                                    # coordinate in cui inizia x
arp_fin, stru_fin, save_fin, clea_fin=  arp_x+ARP_WID, stru_x+STRU_WID, save_x+SAVE_WID, clea_x + CLEA_WID

text_range = [(arp_x,arp_fin), 
              (stru_x,stru_fin), 
              (save_x,save_fin), 
              (clea_x,clea_fin)]





def play(tastoN, cordaN):
    print("\nplay function called ---->")
    #print(f'Playing {tastoN, cordaN}... <-----\n')
    #Definizione frequenza più bassa (della corda cliccata)
    
    f = cordaN*5                #genero i 
    if cordaN == 4 or cordaN == 5:
        f = (cordaN*5)-1
    #-------> Qui la mia f sarà la frequenza della corda a vuoto a questo 
    
    f += tastoN
    #  Qui avrò aggiunto lo spostamento di x semitoni, spostamento relativo al numero del tasto  <-------
    
    frequenza = frequenze[f] 
    
    
    #Suono la nota cliccata
    #print(f'Sto suonando la frequenza {frequenza}')
    Note(frequenza,volume=volumeNote).play(durataNota) 



def posToCoord(tastoN,cordaN):
    """
    Trasforma informazione posizionale es. (1,2), (0,0)
    In coordinate per (x,y) per i cerchio
    """
    global coord
    #Creo coordinate dei PALLINI DA POSIZIONARE   --->
    if tastoN == 0:
        coord = ((Cx-(passo//2)),                            #X: OrigineX prima corda - mezzo passo    
                 Cy+(cordaN*distCorde)    +2)      #Y:OrigineY - distCode (Py conta da 0a5, ma tasti sono da 1a6, quindi "ricorreggo il range" ) + distanza delle corde per numero corda cliccata, per spostarmi fra le corde  
    else:
        coord = ((Cx+   (rBase//2)+   passo*tastoN   - passo),
                 Cy+(cordaN*distCorde)    +2)       #X: OrigineX prima corda - mezzo passo    Y:OrigineY - distCode (Py conta da 0a5, ma tasti sono da 1a6, quindi "ricorreggo il range" ) + distanza delle corde per numero corda cliccata, per spostarmi fra le corde  
    #<-----
    return coord

def circleCreation(tastoN,cordaN): 
    #print(f'circleCreation function t,c {tastoN, cordaN}')
    #circle creation and destruction
    
    # MODIFICO L'ACCORDO CORRENTE --> dizionario che ha come chiave la corda e come valore il tasto corda: tasto
    # Controllo il valore associato alla cordaN   (sempre in accordoCorrente, chè è un dizionario!)
    # Se il valore iniziale è None ---> Il nuovo valore è tastoN
    #
    # Se il valore iniziale non è None -->  
    #           Se il valore iniziale è TastoN ---> Il nuovo valore sarà None (riclicco su stessa corda)
    #                               Altrimenti ---> Il nuovo valore è tastoN
    valueOfT = accordoCorrente[cordaN]
    if valueOfT == None:                    # aggiungo
        accordoCorrente[cordaN] = tastoN
    else:
        if valueOfT == tastoN:              # cancello
            accordoCorrente[cordaN] = None
        else:                               # sposto
            accordoCorrente[cordaN] = tastoN          
    #print(accordoCorrente) 
    
    play(tastoN, cordaN)
    
    # MODIFICO circleDrawed ---> dizionario che ha come chiave il nome della corda 
    #                            e come valore la tupla x,y che posiziona il pallino
    # (circleDrawed è dipendente da accordoCorrente)
    # Devo aggiungere e rimuovere tuple che contengono coppie di valoi (x,y) per disegnare cerchi
    # (1,2), (0,0) ---> in (x,y)
    
    # Prendo i valori chiave di circleDrawed
    # Questa sarà la corda alla quale dovrò modificare il tasto
    nomeCorda = noteList[cordaN] 
    
    
    if valueOfT == None:                    # aggiungo
        cordaN = (cordaN-5)*(-1)
        circleDrawed [nomeCorda] = posToCoord(tastoN,cordaN)
    else:
        if valueOfT == tastoN:              # cancello
            circleDrawed [nomeCorda] = None
        else:                               # sposto
            cordaN = (cordaN-5)*(-1)
            circleDrawed [nomeCorda] = posToCoord(tastoN,cordaN)    
    
    #print(circleDrawed )


    """
    #SE VOGLIO CHE IL CERCHIO SUONI SOLTANTO SE CLICCAT0
    #E NON SE VIENE CANCELLATO (RICLICCATA)  
    #RICHIAMO QUI play!!!!!! 
    """
    return circleDrawed , accordoCorrente



def arpeggio(accordoCorrente):
    print("arpeggio function")
    
    tastoList = list(accordoCorrente.values())
    #print(accordoCorrente)
    #print(tastoList)
    
    corda = 0
    for corda in accordoCorrente:   
        print("play arpeggio")
        #print(corda)
        if tastoList[corda] == None: 
            pass
        else:
            play(tastoList[corda],corda)
            sleep(arpTempo)
            #print(tastoList[corda],corda)
        corda += 1


def strumming(accordoCorrente):
    print("strumming function")
    
    tastoList = list(accordoCorrente.values())
    #print(accordoCorrente)
    #print(tastoList)
    
    for corda in accordoCorrente:   
        print("play strumming")
        if tastoList[corda] == None: 
            pass
        else:
            play(tastoList[corda],corda)
            sleep(strTempo)
            #print(tastoList[corda],corda)
        corda += 1

def clear():
    # Setto il valore di ogni chiave a None
    for key in circleDrawed :
        circleDrawed [key] = None
  
    for key in accordoCorrente:
        accordoCorrente[key] = None

    return circleDrawed , accordoCorrente



def save():
    """
    Memorizza accordi (in forma di liste di tuple) 
    in un dizionario numerato in ordine crescente --> (1,2,3,4,5,6,7,8,9,0)
    """
    print("save function")
    global saveIndex
    
    if saveIndex > maxSavables: saveIndex -= maxSavables+1   # resetta indice a 0, se si va oltre il 9
    
    
    tastoList = list(accordoCorrente.values())    # Lista contenente lo stato dei 6 tasti         (uno per ogni corda)
    
    # Accordo da salvare è una lista con tuple (nCorda, NTasto)
    accordoSalvatoCT = []
    #  nCorda ---> chiave accordoCorrente
    #  nTasto ---> valore di chiave in accordoCorrente 
    #  se nTasto è None ---> non aggiungo la tupla
    
    nCorda = 0

    for tasto in tastoList:
        if tasto == None: 
            pass
        else:
            accordoSalvatoCT.append((nCorda,tasto))
        nCorda += 1
    
    print(f'accordo da salvarer: {accordoSalvatoCT}')
    
    accordiSalvati.update({saveIndex:list(accordoSalvatoCT)})
   
    saveIndex += 1
    
    return accordiSalvati, accordoCorrente

def showSaved(key):
    k = key                                # k == numero che user pigia
    if key == 0: key += maxSavables        # Trasformare input tastiera "1234567890" 
    else: key -= 1                         # in chiave del diz accordiSalvati "0123456789"
    
    if key in accordiSalvati: 
        print(f'Al tasto {k} hai salvato l\'accordo {accordiSalvati[key]}')
        clear()
        chordToShow = accordiSalvati[key]   #l'accordo da mostrare è una lista con tuple (corda,tasto)
        print(chordToShow)
        
        for cordaTasto in chordToShow:
            circleCreation(cordaTasto[1],cordaTasto[0])
            
    else: 
        print(f'Al numero {k} non è salvato nessun accordo!')
        clear()
        
    return circleDrawed ,accordoCorrente       


def TastoCordaDetector(mousePos):
    """
    DEFINISCO SU QUALE TASTO E QUALE NOTA HO CLICCATO
    """
    #Per ogni tasto (X)
    # Il range in cui il primo tasto è cliccato è fra   (particolare)
    # Origine meno tollenza  ----e----  origine più passo meno tolleranza
    # A questo sottraggo il passo (per "prendere" anche il rettangolo 0, opzione corda a vuoto)
    # Moltiplico, ad ogni loop per passo*t, 
    # così da poter controllare per OGNI TASTO           (generale)
    for t in range(nRect+1):      
        if ((Ox - tolleranza)+(passo*t)  - passo < mousePos[0] < (Ox+passo)-tolleranza+(passo*t) - passo):
           
            for c in range(nCorde):
                if ((Cy-tolleranzaSu)+(distCorde*c) <= mousePos[1] <=  (Cy+tolleranzaGiu)+(distCorde*c)):
                                
                    c = (c-5)*(-1)  # <----- Si occupa di
                                    # Modificare c in modo tale che 
                                    # c del mi basso sia 0 ---> e non 6 
                                    # c del mi cantino sia 5 ---> e non 1
                    
                    circleCreation(t,c)            # Creo/distruggo cerchio

                    #print(f'corda----->{c}')
                    #play(t,c) 
                  
                    
def MenuOptions(mousePos):
    mouse_pos_x, mouse_pos_y= mousePos[0], mousePos[1]
    #print(TxRect_clear)
    if (0<mouse_pos_y<menuH):
        
        option = 0
        for ranges in text_range:
            if (ranges[0]<mouse_pos_x<ranges[1]):
                print(f'Hai CLICCATO sull\'opzione {option}') 
                if option == 0: arpeggio(accordoCorrente) 
                if option == 1: strumming(accordoCorrente) 
                if option == 2: save() 
                if option == 3: clear()
                
            option += 1
                            


def renderMenu(WIDTH,SCREEN):
    menu = pygame.Rect(0, 0, WIDTH, menuH)
    pygame.draw.rect(SCREEN, menuColor, menu) #DISEGNO BARRA DEL MENU
    
    SCREEN.blit(TESTO_arpeggio, (arp_x,5, ARP_WID, font_size))
    SCREEN.blit(TESTO_strumming, (stru_x, 5, STRU_WID, font_size)) #testoRect center = (x,y,width,height)
    SCREEN.blit(TESTO_save, (save_x, 5, SAVE_WID, font_size)) 
    SCREEN.blit(TESTO_clear, (clea_x, 5, CLEA_WID, font_size)) 

def renderTastiera(SCREEN):
    #Disegna rettangoli
    for i in range(0,nRect*passo,passo):
        rettangolo = pygame.Rect(Ox+(i), Oy, rBase, rAltezza)
        pygame.draw.rect(SCREEN, coloreRect, rettangolo, border_radius=raggioBordi) #DISEGNA RETTANGOLI NERI (TASTIERA)
    #DisegnaCorde
    for i in range(0,rAltezza,distCorde+1):
        corde = pygame.draw.line(SCREEN, coloreCorde, (Cx,Cy+i),(lunghezCorda,Cy+i),cordeDim)  #DISEGNA CORDE
    
    cerchioSettimo = pygame.draw.circle(SCREEN, (30,30,30), (Ox+(passo*7)-(rBase)+6,Oy+rAltezza+20),10)

def renderCircle(SCREEN):
    i = 0
    circlePosList = list(circleDrawed .values())
    
    for tuple in circlePosList:
        if tuple == None: pass
        else: pygame.draw.circle(SCREEN, coloreCircles, (tuple[0],tuple[1]),10)
        i+=1

def renderSquare(SCREEN):
    rettangolo = pygame.Rect(600-85-10, menuH+10, 85, 50)
    pygame.draw.rect(SCREEN, coloreRect, rettangolo, border_radius=raggioBordi) #DISEGNA RETTANGOLI NERI (TASTIERA)

def renderAnalis(SCREEN):
    ChordsAnalysed, FONDAMENTAL, TIPOLOGI = ChordAnalyser(accordoCorrente)


    font_size_analis = 35
    #print("\n\nFONT CHOICE E' DI TIPO... ",type(font_choice),"\n\n")
    font_choice_analis = pygame.font.Font(None, font_size_analis)
    

    font_size_alter = 16
    font_choice_alter = pygame.font.Font(None, font_size_alter)

    TESTO_analisi = font_choice_analis.render(FONDAMENTAL, True, (230,0,0), fontbgColor)
    TESTO_alter = font_choice_alter.render(TIPOLOGI, True, (230,0,0), fontbgColor)

    TxRect_analisi = TESTO_analisi.get_rect()
    TxRect_alter = TESTO_alter.get_rect()

    ANAL_WID = 35
    
    SCREEN.blit(TESTO_analisi, (524, 50, ANAL_WID, 50)) 
    SCREEN.blit(TESTO_alter, (554, 50, 50, 50)) 
    
def render(WIDTH,SCREEN):
    renderMenu(WIDTH,SCREEN)
    renderTastiera(SCREEN)
    renderCircle(SCREEN)
    renderSquare(SCREEN)
    renderAnalis(SCREEN)
    




def infoNote(accordoCorrente, possibleCord):
    """
    Argomenti: 
            accordoCorrente = come chiave la corda, come valore il tasto cliccato, 
            ---> DEFAULT--> {0:None, 1:None, 2:None, 3:None, 4:None, 5:None}
    Variabili: 
            noteCorrentiId = []
            nomeCorrentiId = []
            La prima conterrà i numeri (ogni numero corrisponde ad una note---> guarda il Diz nomiNote)
            La seconda conterrà i nomi delle note relative ai numeri
    
    Return:
            possibleCord = {}
            Ha chiave il nome delle note 
            Come valore la lista con i numeri, il primo numero corrisponde alla prima nota
            Es: {   A:[0,1,2],  B:[1,2,0], C:[2,0,1]    }
              
    """
    #print("infoNote function")
    global noteCorrentiId, nomeCorrentiId
    
    # resetto liste
    noteCorrentiId = []
    nomeCorrentiId = []
    
    #################################################################
    #               noteCorrentiId
    # La lista note correnti id contiene una lista con i NUMERI (che indicano le note, secondo il dizionario nomiNote) 
    
    c = 0
    for corda in accordoCorrente: 
        if accordoCorrente[corda] == None:  # Se il tasto ha valore None
            #noteCorrentiId.append(None)     # Append a note correnti il valore none
            pass
        
        # Se il tasto ha un dato valore
        else:                               
            tasto = accordoCorrente[corda]
            # Definisci a quale "nota-numero" corrisponda la corda corrente (0,5,10,3,7,0, perché E, A, D, G, B, E)
            if corda == 4 or corda == 5: corda = ((corda*5)%(12)) -1 
            else: corda = (corda*5)%(12) 
                                            
            indiceNota = (tasto+corda)%(12) # E a questo "aggiungiamo" il tasto (ogni tasto un semitono)
            

            if (indiceNota in noteCorrentiId): # Aggiungo i numeri (che, ripeto, corrispondo a una nota)
                pass                           # soltanto una volta                
            else: 
                noteCorrentiId.append(indiceNota)

        c += 1
    
    # ordino noteCorrentiId
    noteCorrentiId = insertionSort(noteCorrentiId)
    
    #################################################################    
    #              nomeCorrentiID
    # Traduciamo i valori numerici nei nomi delle note
    # Servendoci delle informazioni del dizionario nomiNote   
    # Scriviamo queste informazioni in nomeCorrentiID
    
    for i in noteCorrentiId:
        if i == None: 
            #nomeCorrentiId.append(None)
            pass
        else:
            nome = nomiNote[i] 
            nomeCorrentiId.append(nome)
        
        
    for fondam in nomeCorrentiId:
        possibleCord.update({fondam:noteCorrentiId})
        #print(fondam,noteCorrentiId)
        noteCorrentiId = noteCorrentiId[1:]+noteCorrentiId[:1]
            
    #print("note,note",noteCorrentiId,nomeCorrentiId)
    
    return possibleCord
       
       
       
def fondamentalizzazione(possibleCord):
    # le liste vanno "fondamentalizzate"
    # devono avere come primo valore lo 0 
    # e mantenere lo stesso rapporto con gli altri numeri :)
    
    for fondam in possibleCord:
        #print(fondam)
        lista = possibleCord[fondam]    # LISTA  valore di ogni chiave AKA lista di numeri che corrispondono a note
        setTo = lista[0]                # SETto  valore numerico della fondamentale (in posizione LISTA[0])
        i = 0
        for n in lista:
            #print(n,"x")
            lista[i] = (lista[i]-setTo)%12      # Sottraggo ogni elemento per setTo e faccio il dividendo di 12 (numero di note), per "settare" gli intervalli, ora 
            i += 1
    
        possibleCord.update({fondam:lista})
        #possibleCord contiene chiave:valore,   nomeAccordo:[numeri intervalli]
        
    return possibleCord



def ChordAnalyser(accordoCorrente):
    """_summary_

    Args:
        accordoCorrente (_type_): _description_

    Returns:
        CHORDANALYSED = Lista che contiene somma str(FONDAMENTALE) + str(TIPOLOGIA)
        FONDAMENTALE =  Lista delle chiavi di possibleCord ---> Tutti i nomi dei possibili accordi  (A, B, C, ...)
        TIPOLOGIA = Lista delle tipologie di possibleCord ---> Minore, Maggiore, Settima, etc etc
    """
    global noteCorrentiId, nomeCorrentiId, CHORDANALYSED
    
    CHORDANALYSED = []
    FONDAMENTALE, TIPOLOGIA = "", ""
    
    possibleCord = {}       
    #possibleCord ====> Chiave:Valore --> Fondamentale: [Lista con numeri che indicano esattamente le note]
    possibleCord = infoNote(accordoCorrente, possibleCord)
    #possibleCord ====> Chiave:Valore --> Fondamentale: [Lista con numeri fondamentalizzati]
    possibleCord = fondamentalizzazione(possibleCord)
     
        
    # CONTROLLO SE LA SERIE DI INTERVALLI ESISTE (è presente in Chord_types?)
    poss = 0
    for cord in possibleCord:
        listaIntervalli = possibleCord[cord]
        
        print("possibleCord", possibleCord)
        
        i = 0
        for type in CHORD_TYPES:
            #print(i)
            if listaIntervalli == CHORD_TYPES[i][0]: 
                fondamentale = list(possibleCord.keys())[poss] #A? B? C? D? E? F? G?
                print(fondamentale)
                
                valueFond = int([i for i in nomiNote if nomiNote[i]==str(fondamentale)][0]) #Lista che contiene cerca il valore numerico della fondamentale espressa in stringa - la ricerca avviene nel dizionario nomiNote - la lista conterrà un solo elemento!
                
                tipologia = CHORD_TYPES[i][1]  #E' minore? E' maggiore? E' settimo?  . . .
                
                print("listaINTER", listaIntervalli)
                
                N = {nomiNote[x] for x in listaIntervalli}
                print(N, valueFond)
                
                #print("\nEcco il tuo accordo-->", list(possibleCord.keys())[fond], CHORD_TYPES[i][1])  # <---- Risultato analisi!
                FONDAMENTALE, TIPOLOGIA = "", ""
                CHORDANALYSED.append(fondamentale+tipologia)
                FONDAMENTALE = fondamentale
                TIPOLOGIA = tipologia
            
                break
            i+=1       
 
        poss += 1
    
    
    
    
    #print("ECCO", CHORDANALYSED, FONDAMENTALE, TIPOLOGIA)
    #FONDAMENTALE, ALTERAZIONE = str(list(possibleCord.keys())[fond]), str(CHORD_TYPES[i][1])
    #print("analysed", CHORDANALYSED)
    
    return CHORDANALYSED, FONDAMENTALE, TIPOLOGIA
