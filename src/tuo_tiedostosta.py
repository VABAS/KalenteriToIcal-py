#!/usr/bin/python3
from lib.yksi_varaus import hae_yksi_varaus as hae_yksi_varaus
import sys

args = sys.argv
if len(args) < 3:
    sys.exit("Liian vähän argumentteja!\nKäyttö: " + \
             args[0] + " osoite-tiedosto tallennus-tiedosto [eimon]")

osoitetiedosto = args[1]
tallennustiedosto = args[2]

# Asetetaan monistus status-muuttuja.
eimon = False
if len(args) >= 4:
    if "eimon" in args[3:]:
        eimon = True

if eimon:
    print("Tapahtumia ei monisteta käyttäjän pyynnöstä")


tiedosto = open(osoitetiedosto, "r")
vevents = ""

# Haetaan tapahtumat tiedostossa olevien linkkien perusteella.
for rivi in tiedosto:
    vevents += hae_yksi_varaus(rivi.replace('\n', ''), eimon)[2]

# Kirjoitetaan tapahtumat annettuun tiedostoon.
kirjoitustiedosto = open(tallennustiedosto, "w")
kirjoitustiedosto.write("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//sikkela\r\n"
                        + vevents + "END:VCALENDAR\r\n")
