#JAMK kalenteri -> ical

Tämä työkalu hakee JAMK:n kalenterin asiosta ja muuttaa sen ical muotoon, jolloin sen voi tuoda useimpiin kalenteriohjelmiin. 

##Käyttö

Skriptiä käytetään seuraavasti:

`./kalenteri_to_ical.py url tiedosto.ics [eimon] [eikys]` tai `python kalenteri_to_ical.py url tiedosto.ics [eimon] [eikys]`

Edellisessä url on oltava asion lukujärjestyksen osoite kokonaan. 
Osoitteessa on löydyttävä lukujärjestys, joka sisältää tapahtumia. 

Tiedosto.ics on tallennettavan tiedoston nimi suhteessa suoritus hakemistoon. 
Sinulla on oltava oikeudet luoda tiedosto tai muokata sitä. 
**Jos tiedosto on olemassa skripti ylikirjoittaa sen!** 

Joillakin kursseilla on useita esiintymiä samalla ajan hetkellä. 
Jos et halua kaikkia näitä esiintymiä tallennettavan tiedostoosi, lisää komennon perään vielä argumentti _eimon_. 
Tällöin skripti ilmoittaa kun se jättää esiintymiä huomiotta niiden saman tapahtuma-ajan takia. 

Skripti kysyy jokaisen löydetyn kurssin kohdalla haluatko tuoda sen. 
Kun vastaat _k_, hakee se kyseisen kurssin tiedot muistiinsa. 
Voit ohittaa kurssin vastaamalla kysymykseen _e_. 
Voit myös ohittaa kysymyksen antamalla skriptille argumentin _eikys_.
