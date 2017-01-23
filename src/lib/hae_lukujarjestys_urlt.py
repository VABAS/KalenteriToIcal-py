#coding = UTF-8
import sys, http.client
from html.parser import HTMLParser

def hae_lukujarjestys_urlt(osoite):
    class LinkkiEtsija(HTMLParser):
        linkit = []
        def handle_starttag(self, tag, attrs):
            if tag == "a":
                flip = False
                for attr in attrs:
                    if flip:
                        self.linkit.append("/asio_v16"+attr[1]. \
                                           split("\\\'")[1]. \
                                           replace('..', ''))
                        break

                    if attr[0] == "href" and attr[1] == "javascript:void(null);":
                        flip = True

    # Poistetaan osoitteen alusta https:// mikäli se löytyy ja amp.jamk.fi jos
    # löytyy.
    osoite = osoite.replace('https://', '').replace('amp.jamk.fi', '')
    print("Yhdistetään palvelimeen...")

    # Otetaan yhteys palvelimeen.
    c = http.client.HTTPSConnection("amp.jamk.fi")

    # Ja tehdään kysely osoitteella.
    c.request("GET", osoite)
    response = c.getresponse()

    # Jos palvelin antaa jonkun muun kuin 200 OK vastauksen niin keskeytetään.
    if response.status != 200:
        print("VIRHE: " + str(response.status) + " " + response.reason)
        sys.exit("Haku ei onnistunut.")

    data = response.read()
    kivat = []
    #print(data)
    parser = LinkkiEtsija()
    parser.feed(str(data))
    print("Löydettiin " + str(len(parser.linkit)) + " tapahtumaa")
    return parser.linkit
