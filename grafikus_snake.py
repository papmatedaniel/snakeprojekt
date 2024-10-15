import pygame
import random
import time

pygame.init()

KEPERNYO_SZELESSEG = 500
KEPERNYO_MAGASSAG = 500
CELLA_MERET = 50
CELLAK_SZAMA_X = KEPERNYO_SZELESSEG // CELLA_MERET
CELLAK_SZAMA_Y = KEPERNYO_MAGASSAG // CELLA_MERET
KIGYO_SZIN = "green"
ALMA_SZIN = "red"
HATTER_SZIN = "black"

kepernyo = pygame.display.set_mode((KEPERNYO_SZELESSEG, KEPERNYO_MAGASSAG))

kigyo_test_koordinatak = [(5, 0)]
iranyok = {
    "d": (0, 1),   
    "é": (0, -1),  
    "ny": (-1, 0), 
    "k": (1, 0)    
}
alma_pozicio = (2, 3)
utolsoirany = "k"
kigyo_sebesseg = 0.2  
mozgas_idozito = time.time()  
zaszlo = True
clock = pygame.time.Clock()

def palya_rajzolo():
    """Pályát rajzol"""
    kepernyo.fill(HATTER_SZIN)
    for x in range(0, KEPERNYO_SZELESSEG, CELLA_MERET):
        for y in range(0, KEPERNYO_MAGASSAG, CELLA_MERET):
            rect = pygame.Rect(x, y, CELLA_MERET, CELLA_MERET)
            pygame.draw.rect(kepernyo, (40, 40, 40), rect, 1)

def kigyo_rajzolo(kigyo_test_koordinatak):
    """Kigyot razol"""
    for x, y in kigyo_test_koordinatak:
        rect = pygame.Rect(x * CELLA_MERET, y * CELLA_MERET, CELLA_MERET, CELLA_MERET)
        pygame.draw.rect(kepernyo, KIGYO_SZIN, rect)

def alma_rajzolo(alma_pozicio):
    """Almát rajzol"""
    x, y = alma_pozicio
    rect = pygame.Rect(x * CELLA_MERET, y * CELLA_MERET, CELLA_MERET, CELLA_MERET)
    pygame.draw.rect(kepernyo, ALMA_SZIN, rect)

def kigyo_modosito(irany, alma_pozicio):
    """Mozgatja a kígyót az aktuális irány alapján"""
    x1, y1 = iranyok[irany]
    x2, y2 = kigyo_test_koordinatak[-1]
    x3, y3 = (x1 + x2, y1 + y2)

    # Ütközike?
    if (x3, y3) not in kigyo_test_koordinatak[1:] and 0 <= x3 < CELLAK_SZAMA_X and 0 <= y3 < CELLAK_SZAMA_Y:
        kigyo_test_koordinatak.append((x3, y3))
        return True
    return False
    

def alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio):
    """Kezeli az almák pozícióját, és újat generál"""
    if kigyo_test_koordinatak[-1] == alma_pozicio:
        potencialis_alma_pozicio = [(x, y) for x in range(CELLAK_SZAMA_X) for y in range(CELLAK_SZAMA_Y) if (x, y) not in kigyo_test_koordinatak]
        return random.choice(potencialis_alma_pozicio)  
    else:
        kigyo_test_koordinatak.pop(0)  
    return alma_pozicio

def billentyu_kezelo(utolsoirany):
    """Kezeli a billentyűk lenyomását, és frissíti az irányt"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and utolsoirany != "k":
        return "ny"
    if keys[pygame.K_RIGHT] and utolsoirany != "ny":
        return "k"
    if keys[pygame.K_UP] and utolsoirany != "d":
        return "é"
    if keys[pygame.K_DOWN] and utolsoirany != "é":
        return "d"
    return utolsoirany


while zaszlo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            zaszlo = False

    utolsoirany = billentyu_kezelo(utolsoirany)

    if time.time() - mozgas_idozito >= kigyo_sebesseg:
        if not kigyo_modosito(utolsoirany, alma_pozicio):
            print("A kígyó ütközött! Játék vége.")
            zaszlo = False
        else:
            alma_pozicio = alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio)
        mozgas_idozito = time.time()

    
    palya_rajzolo()
    kigyo_rajzolo(kigyo_test_koordinatak)
    alma_rajzolo(alma_pozicio)
    pygame.display.flip()

    clock.tick(30) #fps

pygame.quit()
