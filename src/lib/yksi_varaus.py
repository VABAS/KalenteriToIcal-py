#encoding=UTF-8
import sys, http.client, time
from html.parser import HTMLParser
def hae_yksi_varaus(osoite,monistus):
	class TehtavaHakija(HTMLParser):
		linkit=[];
		flip_1=False
		flip_2=False
		flip_data_handle=False
		kaikki=[]
		nama=[]
		def handle_starttag(self, tag, attrs):
			if tag=="tr":
				for attr in attrs:
					if attr[0]=="bgcolor" and attr[1]=="#e7e7e7":
						self.flip_1=True
						break
			if tag=="td":
				self.flip_2=True
		def handle_endtag(self, tag):
			if tag=="tr":
				if self.flip_1:
					self.kaikki.append(self.nama)
					self.nama=[];
				self.flip_1=False
				self.flip_2=False
			elif tag=="td":
				self.flip_2=False
		def handle_data(self, data):
			if self.flip_1 and self.flip_2:
				self.nama.append(data)
	osoite=osoite.replace('https://','').replace('amp.jamk.fi','');#Poistetaan osoitteen alusta https:// mikäli se löytyy ja amp.jamk.fi jos löytyy
	print("Yhdistetään palvelimeen...")
	c = http.client.HTTPSConnection("amp.jamk.fi");#Otetaan yhteys palvelimeen
	c.request("GET", osoite);#Ja tehdään kysely osoitteella
	response = c.getresponse()
	if response.status!=200:#Jos palvelin antaa jonkun muun kuin 200 OK vastauksen niin keskeytetään
		print("VIRHE: "+str(response.status)+" "+response.reason)
		sys.exit("Haku ei onnistunut.")
	data = response.read()
	parser = TehtavaHakija()
	parser.feed(str(data,"iso-8859-1"))
	print("Löydettiin "+str(len(parser.kaikki))+" esiintymää")
	vevents="";
	olemassa=[];
	kurssitunnus="";
	i=0
	while i<len(parser.kaikki):
		kirjoita=True
		viikonpaiva=parser.kaikki[i][0]
		pvm=parser.kaikki[i][1].split('.')
		kello=parser.kaikki[i][2].split(' - ')
		alkuaika=kello[0].split(':')
		loppuaika=kello[1].split(':')
		paikka=parser.kaikki[i][3]
		kohderyhma=parser.kaikki[i][4]
		opettaja=parser.kaikki[i][5]
		kurssitunnus=parser.kaikki[i][6]
		if not(monistus):#Jos käyttäjä ei ole poistanut monistusta käytöstä otetaan uid-lisä käyttöön
			lisa=str(i);
		else:
			lisa="";
		uid=kurssitunnus.replace(' ','_')+"@"+pvm[2]+pvm[1]+pvm[0]+"T"+alkuaika[0]+alkuaika[1]+"00"+lisa;#Tehdään uid kursitunnuksen, timestampin ja lisän perusteella
		if uid in olemassa:#Tarkistetaan ettei uid ole duplikaatti
			print("VIRHE: Kahdentunut UID "+uid+" - Ei kirjoiteta tiedostoon")
			kirjoita=False;#Laitetaan kirjoitus-flagi nolliin
		else:#Jos ei niin laitetaan tämä uid olemassa olevien taulukkoon
			olemassa.append(uid);
		if kirjoita:#Jos kirjoitus-flagi on true
			vevents=vevents+"BEGIN:VEVENT\r\n";
			vevents=vevents+"UID:"+uid+"\r\n";
			vevents=vevents+"DTSTAMP:"+time.strftime("%Y%m%d")+"T"+time.strftime("%H%M%S")+"\r\n";
			vevents=vevents+"DTSTART:"+pvm[2]+pvm[1]+pvm[0]+"T"+alkuaika[0]+alkuaika[1]+"00\r\n";
			vevents=vevents+"DTEND:"+pvm[2]+pvm[1]+pvm[0]+"T"+loppuaika[0]+loppuaika[1]+"00\r\n";
			vevents=vevents+"SUMMARY:"+kurssitunnus+"\r\n";
			vevents=vevents+"LOCATION:"+paikka+"\r\n";
			vevents=vevents+"DESCRIPTION:"+opettaja+"\r\n";
			vevents=vevents+"END:VEVENT\r\n";
		i+=1
	return [kurssitunnus,vevents];#Palautetaan taulukkona pääohjelmaan
