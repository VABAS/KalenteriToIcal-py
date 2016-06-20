#!/usr/bin/python
#coding=UTF-8
import sys,httplib;
def hae_lukujarjestys_urlt(osoite):
	osoite=osoite.replace('https://','').replace('amp.jamk.fi','');#Poistetaan osoitteen alusta https:// mikäli se löytyy ja amp.jamk.fi jos löytyy
	print "Yhdistetään palvelimeen..."
	c = httplib.HTTPSConnection("amp.jamk.fi");#Otetaan yhteys palvelimeen
	c.request("GET", osoite);#Ja tehdään kysely osoitteella
	response = c.getresponse()
	if response.status!=200:#Jos palvelin antaa jonkun muun kuin 200 OK vastauksen niin keskeytetään
		print "VIRHE: "+str(response.status)+" "+response.reason;
		sys.exit("Haku ei onnistunut.")
	data = response.read().replace('\t','').split('\n');#Otetaan data ulos ja korvataan tabit pois sekä splitataan välilyöntien kohdalta
	kivat=[];
	flip_1=False;
	flip_2=False;
	print "Sivu haettu, parsitaan tietoa...";
	for d in data:#Käydään dataa rivi kerrallaan läpi
		if flip_1:#Jos ollaan aikaisemmin löydetty stop-rivi niin kirjoitetaan tämä rivi taulukkoon
			kivat.append(d);
			flip_1=False
		if not(flip_1) and d=='<tr><td style="font-family:arial,verdana,helvetica;font-size:10px;"> ':#Jos stoppi kohta löytyy asetetaan flagi yköseksi
			flip_1=True;
	print "Löydettiin "+str(len(kivat))+" tapahtumaa";
	urlt=[];
	for k in kivat:#Käydään löydetyt rivit yksi kerrallaan läpi ja korvataan siten, että jätetään vain url osoite ja sisällytetään prefixin kanssa taulukkoon
		urlt.append("/asio_v16"+k.replace('<div><a  href="javascript:void(null);" onclick="window.open(\'..','').split("'")[0]);
	return urlt;#Palautetaan taulukko pääohjelmaan
