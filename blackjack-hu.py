import random

# Definiáljuk a kártyapaklit
szinek = ['Kőr', 'Káro', 'Pikk', 'Treff']
ertekek = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11 az Ász

def kartyapakli_letrehozas():
    return [{'ertek': ertek, 'szin': szin} for ertek in ertekek for szin in szinek]

# Függvény a kéz értékének kiszámításához
def ertek_szamitas(kez):
    ertek = sum(kartya['ertek'] for kartya in kez)
    num_aszok = sum(1 for kartya in kez if kartya['ertek'] == 11)

    while num_aszok > 0 and ertek > 21:
        ertek -= 10
        num_aszok -= 1

    return ertek

# Függvény a kártyák megjelenítéséhez
def kez_megjelenites(kez, az_osztó=False, elrejtett_elso_kartya=True):
    if az_osztó and elrejtett_elso_kartya:
        # Az első kártyát "Rejtett Kártya" ként jelenítjük meg
        print("Rejtett Kártya")
        for kartya in kez[1:]:
            print(f"{kartya['ertek']} a {kartya['szin']}")

    else:
        for kartya in kez:
            print(f"{kartya['ertek']} a {kartya['szin']}")
    
    if not az_osztó:
        print(f"Kéz Értéke: {ertek_szamitas(kez)}")

# Függvény a kártya húzásához a pakliból
def kartya_huzas(pakli):
    return pakli.pop(random.randint(0, len(pakli) - 1))

# Kezdeti kártyák osztása
def jatek_kezdes(pakli):
    jatekos_kez = [kartya_huzas(pakli) for _ in range(2)]
    oszto_kez = [kartya_huzas(pakli) for _ in range(2)]
    return jatekos_kez, oszto_kez

# Fő játék ciklus
def jatek():
    bankroll = 1000  # Kezdő bankroll
    while bankroll > 0:
        pakli = kartyapakli_letrehozas()
        jatekos_kez, oszto_kez = jatek_kezdes(pakli)
        
        tet = int(input(f"Jelenlegi bankroll: {bankroll}$. Add meg a téted: "))
        
        # Ellenőrzés, hogy van-e elég pénzed a tét felállításához
        if tet > bankroll:
            print("Nincs elegendő pénz. Kérjük, adj meg érvényes tétet.")
            continue
        
        # Kezdeti kártyák megjelenítése
        print("Játékos Keze:")
        kez_megjelenites(jatekos_kez)
        print("\nOszto Keze:")
        kez_megjelenites(oszto_kez, az_osztó=True)

        # Blackjack ellenőrzése
        if ertek_szamitas(jatekos_kez) == 21:
            print(f"Blackjack! Nyertél {tet}$-t!")
            bankroll += tet
        else:
            # Játékosnak lehetősége van lapot húzni vagy megállni
            while True:
                valasztas = input("\nSzeretnél húzni (huz/hit) vagy megállni (stand)? ").lower()

                if valasztas == 'huz' or valasztas == 'hit':
                    uj_kartya = kartya_huzas(pakli)
                    jatekos_kez.append(uj_kartya)
                    print(f"Húztál egy {uj_kartya['ertek']} a {uj_kartya['szin']} kártyát.")
                    kez_megjelenites(jatekos_kez)

                    # Játékos vesztés ellenőrzése
                    if ertek_szamitas(jatekos_kez) > 21:
                        print(f"Túl sok! Vesztettél {tet}$-t.")
                        bankroll -= tet
                        break
                elif valasztas == 'megáll' or valasztas == 'stand':
                    # Oszto lép
                    while ertek_szamitas(oszto_kez) < 17:
                        uj_kartya = kartya_huzas(pakli)
                        oszto_kez.append(uj_kartya)

                    print("\nOszto Keze:")
                    kez_megjelenites(oszto_kez)
                    print("Oszto Kezének Értéke:", ertek_szamitas(oszto_kez))

                    # Győztes meghatározása
                    if ertek_szamitas(oszto_kez) > 21:
                        print(f"Oszto túllépte a 21-et! Nyertél {tet}$-t!")
                        bankroll += tet
                    elif ertek_szamitas(oszto_kez) >= ertek_szamitas(jatekos_kez):
                        print("Oszto nyert.")
                        bankroll -= tet
                    else:
                        print(f"Nyertél {tet}$-t!")
                        bankroll += tet

                    break
                else:
                    print("Érvénytelen választás. Kérjük, válaszd 'Húz' vagy 'Megáll'.")
                    
        ujra_jatszani = input("Szeretnél újra játszani? (igen/nem): ").lower()
        if ujra_jatszani != 'igen':
            break

if __name__ == '__main__':
    jatek()
