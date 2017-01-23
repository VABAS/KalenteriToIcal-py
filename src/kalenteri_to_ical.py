#!/usr/bin/python3
#coding = UTF-8
from lib.yksi_varaus import hae_yksi_varaus as hae_yksi_varaus
from lib.hae_lukujarjestys_urlt import hae_lukujarjestys_urlt as hae_lukujarjestys_urlt
import time, sys

# Tarkistetaan että käyttäjä on syöttänyt tarvittavat argumentit.
if len(sys.argv) < 3:
    sys.exit("Ei tarpeeksi argumentteja!\nKäyttö: " +
             sys.argv[0] +
             " osoite tiedosto.ics [eimon] [eikys]")
monistus = False
eikys = False

if len(sys.argv) >=  4:
    for arg in sys.argv:
        if arg  ==  "eimon":
            print("Tapahtumia ei monisteta käyttäjän pyynnöstä")
            monistus = True
        if arg  ==  "eikys":
            print("Tuodaan kaikki tapahtumat kysymättä")
            eikys = True

osoite = sys.argv[1]
tiedosto = sys.argv[2]

# Kutsutaan osoitteet hakevaa aliohjelmaa.
tapahtumat = hae_lukujarjestys_urlt(osoite)
vevents = ""
kurssit = []

# Käydään osoitteet läpi yksi kerrallaan.
for t in tapahtumat:
    # Ja kutsutaan jokaisella osoitteella tapahtumat hakevaa aliohjelmaa.
    tiedot = hae_yksi_varaus(t, monistus)

    # Tarkistetaan ettei kurssia tällä tunnuksella ole jo tuotu.
    if tiedot[1] in kurssit:
        print("INFO: \"Kurssi " + tiedot[0] + "\" on jo tuotu")
    else:
        if eikys:
            kys = "k"
        else:
            # Tiedustellaan haluaako käyttäjä tuoda löydetyn kurssin.
            kys = input("Haluatko tuoda kurssin " + \
                       tiedot[0] + \
                       "? K = Kyllä, Kaikki muut = Ei: ")

        # Jos haluaa niin tuodaan.
        if kys  ==  "k" or kys  ==  "K":
            vevents = vevents + tiedot[2]
            print("Tuotiin kurssi " + tiedot[0])
        else:
            print("Ei tuotu kurssia " + tiedot[0])

        # Kirjoitetaan kurssitunnus tuotujen taulukkoon.
        kurssit.append(tiedot[1])

print("Kirjoitetaan tapahtumat tiedostoon " + tiedosto)

# Kirjoitetaan tapahtumat käyttäjän haluamaan .ics tiedostoon.
tied = open(tiedosto, 'w')
tied.write("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//sikkela\r\n" + vevents +
           "END:VCALENDAR\r\n")
tied.close()
print("Valmis")
