import keyboard
import time

# Kígyó kezdőállapot
kigyo_test_koordinatak = [(5, 0)]
iranyok = {
    "d": (0, 1),   # lefelé
    "é": (0, -1),  # felfelé
    "ny": (-1, 0), # balra
    "k": (1, 0)    # jobbra
}

# Utolsó irány tárolása
utolsoirany = ["k"]  # Kezdőirány jobbra

# Kígyó mozgásának módosítása
def kigy_modosito(irany):
    x1, y1 = iranyok[irany]
    x2, y2 = kigyo_test_koordinatak[-1]
    x3, y3 = (x1 + x2, y1 + y2)
    
    # Ellenőrizzük, hogy a kígyó nem ütközik-e magába vagy nem megy ki a pályáról
    if (x3, y3) not in kigyo_test_koordinatak[1:] and 0 <= x3 <= 9 and 0 <= y3 <= 9:
        kigyo_test_koordinatak.append((x3, y3))
        kigyo_test_koordinatak.pop(0)  # Töröljük az utolsó elemet, hogy a kígyó hossza állandó maradjon
        return True
    return False

# Mozgási sebesség beállítása
mozgasi_sebesseg = 1  # Másodpercben mért időköz a lépések között
utolso_mozgas_ideje = time.time()

# Fő ciklus
zaszlo = True
while zaszlo:
    # Tábla inicializálása
    tabla = [["." for _ in range(10)] for _ in range(10)]
    
    # Kígyó megjelenítése a táblán
    for i in kigyo_test_koordinatak:
        x, y = i
        tabla[y][x] = "X"
    
    # Tábla kiíratása
    print("\033[H\033[J", end="")  # Képernyő törlése
    [print(*i) for i in tabla]
    
    print(kigyo_test_koordinatak)  # Kígyó jelenlegi helye
    
    # Nyíl billentyűk kezelése a keyboard modul segítségével
    if keyboard.is_pressed("left") and utolsoirany[-1] != "k":  # Balra csak akkor, ha nem jobbra ment
        utolsoirany.append("ny")
    elif keyboard.is_pressed("right") and utolsoirany[-1] != "ny":  # Jobbra csak akkor, ha nem balra ment
        utolsoirany.append("k")
    elif keyboard.is_pressed("up") and utolsoirany[-1] != "d":  # Felfelé csak akkor, ha nem lefelé ment
        utolsoirany.append("é")
    elif keyboard.is_pressed("down") and utolsoirany[-1] != "é":  # Lefelé csak akkor, ha nem felfelé ment
        utolsoirany.append("d")
    
    # Ellenőrizzük, hogy elérkeztünk-e a következő mozgási időponthoz
    if time.time() - utolso_mozgas_ideje > mozgasi_sebesseg:
        # Mozgatjuk a kígyót az utolsó irány alapján
        irany = utolsoirany[-1]
        if not kigy_modosito(irany):
            print("A kígyó ütközött! Játék vége.")
            zaszlo = False
        
        # Frissítjük az utolsó mozgás időpontját
        utolso_mozgas_ideje = time.time()
