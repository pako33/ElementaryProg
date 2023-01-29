import random
import sys
import time
import os
import haravasto
 #Tekijät Pyry Myllymäki ja Patrik Koivisto
tila = {
    "kentta": [],
    "kentta_nakyva": [],
    "vuoro_lkm": 0,
    "miinat": 0
}

def alusta_peli(korkeus, leveys, miinat):
    #Luodaan sekä kenttä, jolle miinat asetetaan että pelaajan kenttä
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    tila["kentta"] = kentta

    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))

    kentta_nakyva = []
    for rivi in range(korkeus):
        kentta_nakyva.append([])
        for sarake in range(leveys):
            kentta_nakyva[-1].append(" ")
    tila["kentta_nakyva"] = kentta_nakyva

    miinoitus(kentta, jaljella, miinat)
    return kentta, kentta_nakyva


def luo_kentta():
    #piirtää kentän
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for korkeus, rivi in enumerate(tila["kentta_nakyva"]):
        for leveys, sarake in enumerate(rivi):
            y = korkeus * 40
            x = leveys * 40
            merkki = x
            if merkki == "x":
                avain = "x"
            else:
                avain = " "
            haravasto.lisaa_piirrettava_ruutu(sarake, x, y)
        haravasto.piirra_ruudut()

def miinoitus(kentta, jaljella, miinat_lkm):
    #Luodaan kentälle satunnaisesti miinoja
    for i in range(miinat_lkm):
        a, b = random.choice(jaljella)
        jaljella.remove((a, b))
        kentta[b][a] = "x"


def tyhjat_ruudut():
    #lasketaan tyhjien ruutujen määrä
    kentta = tila["kentta_nakyva"]
    tyhjia = 0
    for i, rivi in enumerate(kentta):
        rivi_tyhjat = rivi.count(" ") + rivi.count("f")
        tyhjia += rivi_tyhjat
    return tyhjia

def viereiset_miinat(x, y, kentta):
    #Lasketaan ruudun vieressä olevat miinat
    miinat_lkm = 0
    y_raja = {y, y -1, y + 1}
    x_raja = {x, x - 1, x + 1}

    for y, rivi in enumerate(kentta):
        for x, ruutu in enumerate(rivi):
            if y in y_raja and x in x_raja and ruutu == "x":
                miinat_lkm += 1
    return miinat_lkm


def tulvataytto(kentta, kentta_nakyva, x, y):
    #käytetään avaamaan miinakentän ruudut
    kentta_korkeus = len(kentta)
    kentta_leveys = len(kentta[0])
    numero = viereiset_miinat(x, y, kentta)
    tutki = [(x, y)]

    while len(tutki) > 0:
        x, y = tutki.pop()
        if kentta[y][x] != "x":
            numero = viereiset_miinat(x, y, kentta)
            if numero > 0:
                kentta_nakyva[y][x] = numero
                kentta[y][x] = numero
                continue
            else:
                kentta_nakyva[y][x] = "0"
                kentta[y][x] = "0"
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if i < kentta_korkeus and i >= 0 and j < kentta_leveys and j >= 0:
                        if kentta_nakyva[i][j] == " ":
                            tutki.append((j, i))

def kasittele_hiiri(x, y, painike, muokkausnapit):
    oikea = haravasto.HIIRI_OIKEA
    vasen = haravasto.HIIRI_VASEN
    kentta_nakyva = tila["kentta_nakyva"]
    kentta = tila["kentta"]

    #miinojen merkkausominaisuus
    if painike == oikea:
        x = int(x / 40)
        y = int(y / 40)
        if kentta_nakyva[y][x] == " ":
            kentta_nakyva[y][x] = "f"
        elif kentta_nakyva[y][x] == "f":
            kentta_nakyva[y][x] = " "    
    #ruutujen valitseminen ja voiton/häviön merkitseminen
    if painike == vasen:
        x = int(x / 40)
        y = int(y / 40)
        if kentta[y][x] == " ":
            kentta[y][x] = "0"
            kentta_nakyva[y][x] = "0"
            tulvataytto(kentta, kentta_nakyva, x, y)
            tila["vuoro_lkm"] += 1
            if tyhjat_ruudut() == tila["miinat"]:
                print("Olet voittanut pelin!")
                tila["lopputulos"] = "voitto"
                haravasto.lopeta()

        elif kentta[y][x] == "x":
            kentta_nakyva[y][x] = "x"
            haravasto.piirra_ruudut()
            tila["vuoro_lkm"] += 1
            print("Räjäytit miinaan! Parempi onni ensi kerralla!")
            tila["lopputulos"] = "häviö"
            haravasto.lopeta() 

def valikko():
    #pelin päävalikko
    while True:

        print(r"""          _ ._  _ , _ ._
        (_ ' ( `  )_  .__)
      ( (  (    )   `)  ) _)
     (__ (_   (_ . _) _) ,__)
         `~~`\ ' . /`~~`
              ;   ;
              /   \
_____________/_ __ \_____________""")
        print("        MIINAHARAVA-The Game!   ")
        valikko = input("Uusi Peli (U), Tilastot (T), Sulje Peli (S)")
        if valikko.lower() == "u":
            break
        elif valikko.lower() == "t":
            avaa_tilastot()
        if valikko.lower() == "s":
            return 0
        else:
            print("Valitse jokin annetuista vaihtoehdoista!")
        return 1

def tallenna_tiedot(pvm, aloitusaika, loppuaika, lopputulos, korkeus, leveys, miinat, vuoro_lkm):

    #Tallentaa pelatun pelin tiedot tekstitiedostoon.
    
    if loppuaika >= aloitusaika:
        pelin_kesto = loppuaika - aloitusaika
    else:
        pelin_kesto = 60 - aloitusaika + loppuaika
    with open("tilastot.txt", "a") as tilastot:
        tilastot.write("Päivämäärä: {}.""\n" "Lopputulos: {}" "\n" "Pelin pelin_kesto: {}.""\n" \
            "Vuorojen määrä: {}.""\n" "Pelikentän koko: {} x {}""\n" "Miinat: {}""\n"\
            .format( pvm, lopputulos, pelin_kesto, vuoro_lkm, leveys, korkeus, miinat))
def avaa_tilastot():
    osCommandString = "notepad.exe tilastot.txt"
    os.system(osCommandString)


def main():
    #main funktiot
    if valikko() == 0:
        sys.exit()    
    korkeus = int(input("Aseta kentän korkeus: "))
    leveys = int(input("Aseta kentän leveys: "))
    try:
        if leveys < 2 or korkeus < 2:
            print("Tällä kentällä ei mahdu pelaamaan!")
    except ValueError:
        print("Käytä vain kokonaislukuja!")
    try:
        miinat = int(input("Montako miinaa?: "))
        tila["miinat"] = miinat
        if miinat < 1:
            print("Et voi pelata ilman miinoja!")
        elif miinat >= korkeus * leveys:
            print("Älä laita liikaa miinoja!")
    except ValueError:
        print("Käytä vain kokonaislukuja!")
    tila["vuoro_lkm"] = 0
    pvm = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    aloitusaika = time.localtime().tm_min
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(leveys * 40, korkeus * 40)
    alusta_peli(korkeus, leveys, miinat)
    haravasto.aseta_piirto_kasittelija(luo_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()
    loppuaika = time.localtime().tm_min
    tallenna_tiedot(pvm, aloitusaika, loppuaika, tila["lopputulos"], korkeus, leveys, miinat, tila["vuoro_lkm"])




if __name__ == "__main__":
    while True:
        main()