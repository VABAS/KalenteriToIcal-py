#encoding = UTF-8
import sys, http.client, time
from html.parser import HTMLParser
def hae_yksi_varaus(osoite, monistus):
    class TehtavaHakija(HTMLParser):
        flip_1 = False
        flip_2 = False
        flip_data_handle = False
        kaikki = []
        nama = []
        dataProsessoitu = False

        def handle_starttag(self, tag, attrs):
            if tag == "tr":
                for attr in attrs:
                    if attr[0] == "bgcolor" and attr[1] == "#e7e7e7":
                        self.flip_1 = True
                        break

            if tag == "td":
                self.flip_2 = True

        def handle_endtag(self, tag):
            if tag == "tr":
                if self.flip_1:
                    self.kaikki.append(self.nama)
                    self.nama = []

                self.flip_1 = False
                self.flip_2 = False

            elif tag == "td":
                # Jos dataa ei ole prosessoitu, niin lisätään tyhjä rivi
                # taulukkoon.
                if not self.dataProsessoitu and self.flip_1 and self.flip_2:
                    self.nama.append("")

                self.dataProsessoitu = False
                self.flip_2 = False
                
        def handle_data(self, data):
            if self.flip_1 and self.flip_2:
                self.nama.append(data)
                self.dataProsessoitu = True


    # Poistetaan osoitteen alusta https:// mikäli se löytyy ja amp.jamk.fi jos
    # löytyy.
    osoite = osoite.replace('https://', '').replace('amp.jamk.fi', '')

    # Otetaan yhteys palvelimeen.
    print("Yhdistetään palvelimeen...")
    c = http.client.HTTPSConnection("amp.jamk.fi")

    # Ja tehdään kysely osoitteella.
    c.request("GET", osoite)
    response = c.getresponse()
    # Jos palvelin antaa jonkun muun kuin 200 OK vastauksen niin keskeytetään.
    if response.status != 200:
        print("VIRHE: " + str(response.status) + " " + response.reason)
        sys.exit("Haku ei onnistunut.")
    data = response.read()
    parser = TehtavaHakija()
    parser.feed(str(data, "iso-8859-1"))
    print("Löydettiin " + str(len(parser.kaikki)) + " esiintymää")
    vevents = ""
    olemassa = []
    kurssitunnus = ""
    i = 0
    while i < len(parser.kaikki):
        kirjoita = True
        viikonpaiva = parser.kaikki[i][0]
        pvm = parser.kaikki[i][1].split('.')
        kello = parser.kaikki[i][2].split(' - ')
        alkuaika = kello[0].split(':')
        loppuaika = kello[1].split(':')
        paikka = parser.kaikki[i][3]
        kohderyhma = parser.kaikki[i][4]
        opettaja = parser.kaikki[i][5]
        kurssitunnus = parser.kaikki[i][6]

        # Jos käyttäjä ei ole poistanut monistusta käytöstä otetaan uid-lisä
        # käyttöön.
        if not(monistus):
            lisa = str(i)
        else:
            lisa = ""

        #Tehdään uid kursitunnuksen, timestampin ja lisän perusteella.
        uid = kurssitunnus.replace(' ', '_') + \
              "@" + pvm[2] + pvm[1] + pvm[0] + \
              "T" + alkuaika[0] + alkuaika[1] + "00" + lisa

        # Tarkistetaan ettei uid ole duplikaatti.
        if uid in olemassa:
            print("VIRHE: Kahdentunut UID "+uid+" - Ei kirjoiteta tiedostoon")
            # Laitetaan kirjoitus-flagi nolliin.
            kirjoita = False

        # Jos ei niin laitetaan tämä uid olemassa olevien taulukkoon.
        else:
            olemassa.append(uid)

        # Jos kirjoitus-flagi on true.
        if kirjoita:
            vevents = vevents + "BEGIN:VEVENT\r\n"
            vevents = vevents + "UID:" + uid + "\r\n"
            vevents = vevents + "DTSTAMP:" + time.strftime("%Y%m%d") + "T" + \
                              time.strftime("%H%M%S") + "\r\n"
            vevents = vevents + "DTSTART:" + pvm[2] + pvm[1] + pvm[0] + "T" + \
                               alkuaika[0] + alkuaika[1] + "00\r\n"
            vevents = vevents + "DTEND:" + pvm[2] + pvm[1] + pvm[0] + "T" + \
                              loppuaika[0] + loppuaika[1] + "00\r\n"
            vevents = vevents + "SUMMARY:" + kurssitunnus + "\r\n"
            vevents = vevents + "LOCATION:" + paikka + "\r\n"
            vevents = vevents + "DESCRIPTION:" + opettaja + "\r\n"
            vevents = vevents + "END:VEVENT\r\n"
        i += 1

    # Palautetaan taulukkona pääohjelmaan.
    return [kurssitunnus, uid, vevents]
