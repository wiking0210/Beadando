# Osztályok Létrehozása
#   xx Hozz létre egy Szoba absztrakt osztályt, amely alapvető attribútumokat definiál (ár, szobaszám). (5 pont)
#   xx Hozz létre az Szoba osztályból EgyagyasSzoba és KetagyasSzoba származtatott osztályokat, amelyek különböző attributumai vannak, és az áruk
#       is különböző.(5 pont)
#   xx Hozz létre egy Szalloda osztályt, ami ezekből a Szobákból áll, és van saját attributuma is (név pl.) (10 pont)
#   xx Hozz létre egy Foglalás osztályt, amelybe a Szálloda szobáinak foglalását tároljuk (elég itt, ha egy foglalás csak egy napra szól) (10 pont)
#
# Foglalások Kezelése
#   xx Implementálj egy metódust, ami lehetővé teszi szobák foglalását dátum alapján, visszaadja annak árát. (15 pont)
#   xx Implementálj egy metódust, ami lehetővé teszi a foglalás lemondását. (5 pont)
#   xx Implementálj egy metódust, ami listázza az összes foglalást. (5 pont)
#
# Felhasználói Interfész és adatvalidáció
#   xx Készíts egy egyszerű felhasználói interfészt, ahol a felhasználó kiválaszthatja a kívánt műveletet (pl. foglalás, lemondás, listázás). (20 pont)
#   !!! check avail. !!! A foglalás létrehozásakor ellenőrizd, hogy a dátum érvényes (jövőbeni) és a szoba elérhető-e akkor. (10 pont)
#   xx Biztosítsd, hogy a lemondások csak létező foglalásokra lehetségesek. (5 pont)
# #   xx Töltsd fel az futtatás után a rendszert 1 szállodával, 3 szobával és 5 foglalással, mielőtt a felhasználói adatbekérés megjelenik. (10 pont)

from datetime import datetime
import winsound

# Osztályok Létrehozása

class Szoba:
    def __init__(self, szobsz, ar):
        self.szobsz = szobsz
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobsz, bath):
        super().__init__(szobsz, 70000)
        self.bath = bath

class KetagyasSzoba(Szoba):
    def __init__(self, szobsz, extra):
        super().__init__(szobsz, 90000)
        self.extra = extra

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.fgs_ok = []

# Foglalások Kezelése

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    # def fgs(self, szobsz, datum):
    #     for szoba in self.szobak:
    #         if szoba.szobsz == szobsz:
    #             fgs = Foglalas(szoba, datum)
    #             self.fgs_ok.append(fgs)
    #             return szoba.ar
    #     return None
    
    def fgs(self, szobsz, datum):
        for fgs in self.fgs_ok:
            if fgs.szoba.szobsz == szobsz and fgs.datum == datum:
                print("\nA szoba már foglalt ezen a napon. \nVálasszon másik szobát vagy másik dátumot!")
                return
        for szoba in self.szobak:
            if szoba.szobsz == szobsz:
                self.fgs_ok.append(Foglalas(szoba, datum))
                print("Sikeres foglalás!")
                return szoba.ar
        print("\nA megadott szobaszám nem létezik a szállodában.")

    def lmond(self, szobsz, datum):
        for fgs in self.fgs_ok:
            if fgs.szoba.szobsz == szobsz and fgs.datum == datum:
                self.fgs_ok.remove(fgs)
                return True
        return False
    
    def list_fgs_ok(self):
        for fgs in self.fgs_ok:
            print(f"Szoba: {fgs.szoba.szobsz}, Időpont: {fgs.datum}")

# Rendszer feltöltés: Szalloda létrehozása
hotel = Szalloda("Pihenő Hotel")

# Rendszer feltöltés: Szobák hozzáadása
hotel.add_szoba(EgyagyasSzoba("101","Kád"))
hotel.add_szoba(EgyagyasSzoba("102","Zuhany"))
hotel.add_szoba(KetagyasSzoba("201","Jacuzzi"))

# Rendszer feltöltés: Foglalások hozzáadása
hotel.fgs("101", datetime(2024, 5, 10))
hotel.fgs("102", datetime(2024, 5, 12))
hotel.fgs("201", datetime(2024, 5, 15))
hotel.fgs("101", datetime(2024, 5, 15))
hotel.fgs("102", datetime(2024, 5, 15))

# Felhasználói interfész
while True:

    print("\nVálassz műveletet:")
    print("1. Szoba foglalása")
    print("2. Foglalás lemondása")
    print("3. Foglalások listázása")
    print("4. Szobák listázása")
    print("5. Kilépés")
    case = input("Művelet kiválasztása (1/2/3/4/5): ")

    if case == "1":
        szobsz = input("\nAdd meg a foglalandó szoba számát: ")
        datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN, jelenleg csak egy napra lehetséges a foglalás): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            if datum < datetime.now():
                print("\nHibás dátum! A foglalás csak jövőbeni időpontra lehetséges.")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            else:
                ar = hotel.fgs(szobsz, datum)
                if ar:
                    print(f"A foglalás sikeres! Az ár: {ar} Ft")
                else:
                    print("\nHibás szobaszám!")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except ValueError:
            print("\nHibás dátum formátum!")
    elif case == "2":
        szobsz = input("\nAdd meg a lemondandó foglalás szoba számát: ")
        datum = input("Add meg a lemondandó foglalás dátumát (ÉÉÉÉ-HH-NN): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            siker = hotel.lmond(szobsz, datum)
            if siker:
                print("\nA foglalás sikeresen lemondva.")
            else:
                print("\nNincs ilyen foglalás.")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        except ValueError:
            print("\nHibás dátum formátum!")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    elif case == "3":
        hotel.list_fgs_ok()
    elif case == "4":
            print("Szobák száma:")
            print(len(hotel.szobak))
            print("Egyágyas szobák:")
            for szoba in hotel.szobak:
                if isinstance(szoba, EgyagyasSzoba):
                    print(f"Szobaszám: {szoba.szobsz}, Ár: {szoba.ar} Ft, (Fürdő: {szoba.bath})")
            print("\nKétágyas szobák:")
            for szoba in hotel.szobak:
                if isinstance(szoba, KetagyasSzoba):
                    print(f"Szobaszám: {szoba.szobsz}, Ár: {szoba.ar} Ft, (Extra: {szoba.extra})")
    elif case == "5":
        break
    else:
        print("\nHibás választás!")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)