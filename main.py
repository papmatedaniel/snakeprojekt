import time



kigyo_test_koordinatak = [(5,0)]
iranyok = {
    "d": (0, 1),
    "é": (0, -1),
    "ny": (-1, 0),
    "k": (1, 0)
}
def kigy_modosito(irany):
    x1,y1 = iranyok[irany]
    x2, y2 = kigyo_test_koordinatak[-1]
    x3, y3 = (x1 + x2, y1 + y2)
    if (x3, y3) not in kigyo_test_koordinatak[1:] and 0 <= x3 <= 9 and 0 <= y3 <= 9:
        kigyo_test_koordinatak.append((x3, y3))
        kigyo_test_koordinatak.remove(kigyo_test_koordinatak[0])
        return True

    return False

    

utolsoirany = []
zaszlo = True
while zaszlo:
    tabla = [["." for _ in range(10)] for _ in range(10)]

    for i in kigyo_test_koordinatak:
        x, y = i
        tabla[y][x] = "X"


    
    [print(*i) for i in tabla]


    print(kigyo_test_koordinatak)
    irany = input("Add meg az irányt betűjelöléssel(É, D, NY, K): ").lower()
    utolsoirany.append(irany)
    print("\033[H\033[J", end="")

    print(kigy_modosito(utolsoirany[-1]))

    
    
print("Vége")