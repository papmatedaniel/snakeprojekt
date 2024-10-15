import keyboard
import time
import random

kigyo_test_koordinatak = [(5, 0)]
iranyok = {
    "d": (0, 1),   # Lefelé
    "é": (0, -1),  # Felfelé
    "ny": (-1, 0), # Balra
    "k": (1, 0)    # Jobbra
}

alma_pozicio = (2, 3)
utolsoirany = "k"
kigyo_sebesseg = 0.5
mozgas_idozite = 0
zaszlo: bool = True



def kigy_modosito(irany, alma_pozicio):
    """Kígyó pozíciójának módosítása mozgás esetén"""
    x1, y1 = iranyok[irany]
    x2, y2 = kigyo_test_koordinatak[-1]
    x3, y3 = (x1 + x2, y1 + y2)
    
    # Ütközés ellenőrzés
    if (x3, y3) not in kigyo_test_koordinatak[1:] and 0 <= x3 <= 9 and 0 <= y3 <= 9:
        kigyo_test_koordinatak.append((x3, y3))
        return True
    return False

def alma_modosito():
    """A véletlenszerű alma legenerálása"""
    uj_kigyo_test_koordinatak = []

    for i in kigyo_test_koordinatak:
        uj_kigyo_test_koordinatak.extend([(i[0], i[1] + 1), (i[0], i[1] - 1), (i[0] + 1, i[1]), (i[0] - 1, i[1]), (i[0], i[1])])
    
    osszes_tabla_koordinata = []
    for x in range(10):
        for y in range(10):
            osszes_tabla_koordinata.append((x, y))

    potencialis_alma_pozicio = list(set(osszes_tabla_koordinata) - set(uj_kigyo_test_koordinatak))
    uj_alma_pozicio = random.choice(potencialis_alma_pozicio)
    return uj_alma_pozicio

def alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio):
    """Az almaevés kezelése és a kígyó koordinátáinak frissítése"""
    if kigyo_test_koordinatak[-1] == alma_pozicio:
        alma_pozicio = alma_modosito()  # Új alma generálása
    else:
        kigyo_test_koordinatak.pop(0)  # Csak akkor törlünk, ha nem evett almát
    
    return alma_pozicio

def tabla_kezelo():
    """A játéktábla megjelenítése a kígyó és a kigyo_test_koordinátájának alapján"""
    tabla = [["." for _ in range(10)] for _ in range(10)]
    
    for i in kigyo_test_koordinatak:
        x, y = i
        tabla[y][x] = "X"

    xx, yy = alma_pozicio
    tabla[yy][xx] = "O"
    
    print("\033[H\033[J", end="")
    [print(*i) for i in tabla]
    print(kigyo_test_koordinatak)  


def billentyu_kezelo(utolsoirany):
    """A billentyűk lenyomásának kezelése"""
    if keyboard.is_pressed("left") and utolsoirany != "k":  # Balra csak akkor, ha nem jobbra ment
        utolsoirany = "ny"
    elif keyboard.is_pressed("right") and utolsoirany != "ny":  # Jobbra csak akkor, ha nem balra ment
        utolsoirany = "k"
    elif keyboard.is_pressed("up") and utolsoirany != "d":  # Felfelé csak akkor, ha nem lefelé ment
        utolsoirany = "é"
    elif keyboard.is_pressed("down") and utolsoirany != "é":  # Lefelé csak akkor, ha nem felfelé ment
        utolsoirany = "d"
    
    return utolsoirany


while zaszlo:
    tabla_kezelo()
    
    utolsoirany = billentyu_kezelo(utolsoirany)
    
    irany = utolsoirany

    aktualis_ido = time.time()
    if aktualis_ido - mozgas_idozite >= kigyo_sebesseg:
        mozgas_tortent = kigy_modosito(irany, alma_pozicio)
        if not mozgas_tortent:
            print("A kígyó ütközött! Játék vége.")
            zaszlo = False
        mozgas_idozite = aktualis_ido

        # Az almaevés ellenőrzése és kezelése
        alma_pozicio = alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio)

    # Csökkentjük a késleltetést, hogy az irányváltás gyorsabb legyen
    time.sleep(0.05)
