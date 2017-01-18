#JAMK kalenteri -> ical

Tämä työkalu hakee JAMK:n kalenterin asiosta ja muuttaa sen ical muotoon,
jolloin sen voi tuoda useimpiin kalenteriohjelmiin. Työkalu vaati toimiakseen
python-tulkin version 3 (python3). Ohjelma ei ole yhteensopiva muiden pythonin
versioiden kanssa.

##Käyttö

###kalenteri_to_ical.py

`./kalenteri_to_ical.py url tiedosto.ics [eimon] [eikys]` tai
`python kalenteri_to_ical.py url tiedosto.ics [eimon] [eikys]`

Edellisessä url on oltava asion lukujärjestyksen osoite kokonaan ja sisältää
päiväys. Osoitteessa on löydyttävä lukujärjestys, joka sisältää tapahtumia.

Tiedosto.ics on tallennettavan tiedoston nimi suhteessa suoritus hakemistoon.
Sinulla on oltava oikeudet luoda tiedosto tai muokata sitä. **Jos tiedosto on
olemassa skripti ylikirjoittaa sen!**

Joillakin kursseilla on useita esiintymiä samalla ajan hetkellä. Jos et halua
kaikkia näitä esiintymiä tallennettavan tiedostoosi, lisää komennon perään vielä
argumentti _eimon_. Tällöin skripti ilmoittaa kun se jättää esiintymiä huomiotta
niiden saman tapahtuma-ajan takia.

Skripti kysyy jokaisen löydetyn kurssin kohdalla haluatko tuoda sen. Kun vastaat
_k_, hakee se kyseisen kurssin tiedot muistiinsa. Voit ohittaa kurssin
vastaamalla kysymykseen _e_. Voit myös ohittaa kysymyksen antamalla skriptille
argumentin _eikys_.

###yksi_varaus.py

`lib/yksi_varaus.py url tiedosto.ics [eimon]` tai
`python lib/yksi_varaus.py url tiedosto.ics [eimon]`

On mahdollista myös hakea ainoastaan yksi varaus (kurssi) käyttämällä
yksi_varaus.py-tiedostoa suoraan lib-hakemistosta. Eimon-argumentti ohittaa
tapahtumien monistamisen.
