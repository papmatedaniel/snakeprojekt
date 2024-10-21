import pygame
import random
import sys
import time

pygame.init()

# Színek és méretek
KEPERNYO_SZELESSEG = 500
KEPERNYO_MAGASSAG = 500
CELLA_MERET = 50
CELLAK_SZAMA_X = KEPERNYO_SZELESSEG // CELLA_MERET
CELLAK_SZAMA_Y = KEPERNYO_MAGASSAG // CELLA_MERET
KIGYO_SZIN = "green"
ALMA_SZIN = "red"
HATTER_SZIN = "black"
FEHER = (255, 255, 255)
KIVALASZTOTT_SZIN = (255, 0, 0)
FONT = pygame.font.Font(None, 50)

kepernyo = pygame.display.set_mode((KEPERNYO_SZELESSEG, KEPERNYO_MAGASSAG))
clock = pygame.time.Clock()

# Menü opciók
menu_opciok = ["Játék indítása", "Beállítások", "Pontszámok", "Kilépés"]

# Pálya rajzolás
def palya_rajzolo():
    kepernyo.fill(HATTER_SZIN)
    for x in range(0, KEPERNYO_SZELESSEG, CELLA_MERET):
        for y in range(0, KEPERNYO_MAGASSAG, CELLA_MERET):
            rect = pygame.Rect(x, y, CELLA_MERET, CELLA_MERET)
            pygame.draw.rect(kepernyo, (40, 40, 40), rect, 1)

# Kígyó rajzolás
def kigyo_rajzolo(kigyo_test_koordinatak):
    for x, y in kigyo_test_koordinatak:
        rect = pygame.Rect(x * CELLA_MERET, y * CELLA_MERET, CELLA_MERET, CELLA_MERET)
        pygame.draw.rect(kepernyo, KIGYO_SZIN, rect)

# Alma rajzolás
def alma_rajzolo(alma_pozicio):
    x, y = alma_pozicio
    rect = pygame.Rect(x * CELLA_MERET, y * CELLA_MERET, CELLA_MERET, CELLA_MERET)
    pygame.draw.rect(kepernyo, ALMA_SZIN, rect)

# Pontszám kirajzolása
def pontszam_megjelenitese(pontszam):
    szoveg = FONT.render(f"Pontszám: {pontszam}", True, FEHER)
    kepernyo.blit(szoveg, (10, 10))

# Szünet szöveg kirajzolása
def szunet_megjelenitese():
    szoveg = FONT.render("Szünet", True, FEHER)
    kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG // 2 - szoveg.get_width() // 2, KEPERNYO_MAGASSAG // 2))

# Menü megjelenítése
def menu_megjelenitese(kijelolt_opcio):
    kepernyo.fill(HATTER_SZIN)
    for index, opcio in enumerate(menu_opciok):
        if index == kijelolt_opcio:
            szoveg = FONT.render(opcio, True, KIVALASZTOTT_SZIN)
        else:
            szoveg = FONT.render(opcio, True, FEHER)
        
        kepernyo.blit(szoveg, (KEPERNYO_SZELESSEG // 2 - szoveg.get_width() // 2, 150 + index * 60))

    pygame.display.flip()

# Menü kezelése
def menu():
    kijelolt_opcio = 0  # Kezdő opció
    fut = True
    while fut:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    kijelolt_opcio = (kijelolt_opcio + 1) % len(menu_opciok)  # Menüpontok közötti navigálás
                elif event.key == pygame.K_UP:
                    kijelolt_opcio = (kijelolt_opcio - 1) % len(menu_opciok)
                elif event.key == pygame.K_RETURN:
                    if kijelolt_opcio == 0:
                        return "jatek_inditasa"  # Játék indítása
                    elif kijelolt_opcio == 1:
                        return "beallitasok"  # Beállítások
                    elif kijelolt_opcio == 2:
                        return "pontszamok"  # Pontszámok megtekintése
                    elif kijelolt_opcio == 3:
                        pygame.quit()
                        sys.exit()  # Kilépés a játékból

        menu_megjelenitese(kijelolt_opcio)

# Kígyó mozgás
def kigyo_modosito(irany, kigyo_test_koordinatak):
    x1, y1 = irany
    x2, y2 = kigyo_test_koordinatak[-1]
    x3, y3 = (x1 + x2, y1 + y2)

    if (x3, y3) not in kigyo_test_koordinatak[1:] and 0 <= x3 < CELLAK_SZAMA_X and 0 <= y3 < CELLAK_SZAMA_Y:
        kigyo_test_koordinatak.append((x3, y3))
        return True
    return False

# Almaevés kezelése
def alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio):
    if kigyo_test_koordinatak[-1] == alma_pozicio:
        potencialis_alma_pozicio = [(x, y) for x in range(CELLAK_SZAMA_X) for y in range(CELLAK_SZAMA_Y) if (x, y) not in kigyo_test_koordinatak]
        return random.choice(potencialis_alma_pozicio), True  # Visszaadjuk az új almát és hogy evett-e
    else:
        kigyo_test_koordinatak.pop(0)
    return alma_pozicio, False

# Billentyű kezelése
def billentyu_kezelo(utolsoirany, szunet, p_gomb_lenyomva):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and utolsoirany != "k":
        return (-1, 0), szunet, p_gomb_lenyomva
    if keys[pygame.K_RIGHT] and utolsoirany != "ny":
        return (1, 0), szunet, p_gomb_lenyomva
    if keys[pygame.K_UP] and utolsoirany != "d":
        return (0, -1), szunet, p_gomb_lenyomva
    if keys[pygame.K_DOWN] and utolsoirany != "é":
        return (0, 1), szunet, p_gomb_lenyomva

    # Szünet kezelés
    if keys[pygame.K_p]:
        if not p_gomb_lenyomva:  # Csak akkor vált, ha korábban nem volt lenyomva
            szunet = not szunet
            p_gomb_lenyomva = True
    else:
        p_gomb_lenyomva = False  # Ha a P gombot elengedtük, reseteljük

    return utolsoirany, szunet, p_gomb_lenyomva


# Játék indítása
def jatek():
    kigyo_test_koordinatak = [(5, 0)]
    utolsoirany = (1, 0)  # Kezdetben jobbra megy
    alma_pozicio = (2, 3)
    kigyo_sebesseg = 0.2
    pontszam = 0
    szunet = False
    zaszlo = True
    mozgas_idozito = time.time()
    p_gomb_lenyomva = False  # Gomb lenyomva változó inicializálása

    while zaszlo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                zaszlo = False

        utolsoirany, szunet, p_gomb_lenyomva = billentyu_kezelo(utolsoirany, szunet, p_gomb_lenyomva)

        if not szunet:
            if time.time() - mozgas_idozito >= kigyo_sebesseg:
                if not kigyo_modosito(utolsoirany, kigyo_test_koordinatak):
                    print("A kígyó ütközött! Játék vége.")
                    zaszlo = False
                else:
                    alma_pozicio, evett = alma_eves_kezelo(kigyo_test_koordinatak, alma_pozicio)
                    if evett:
                        pontszam += 1
                mozgas_idozito = time.time()

        palya_rajzolo()
        kigyo_rajzolo(kigyo_test_koordinatak)
        alma_rajzolo(alma_pozicio)
        pontszam_megjelenitese(pontszam)
        if szunet:
            szunet_megjelenitese()

        pygame.display.update()
        clock.tick(30)


# Menühívás
valasztas = menu()

if valasztas == "jatek_inditasa":
    jatek()
elif valasztas == "beallitasok":
    # print("Beállítások menü...")
    pass
elif valasztas == "pontszamok":
    # print("Pontszámok megtekintése...")
    pass

pygame.quit()
