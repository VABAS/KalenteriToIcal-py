#!/usr/bin/python
#coding=UTF-8
def hae_lukujarjestys_urlt(osoite):
	import sys,httplib;
	#osoite="https://amp.jamk.fi/asio_v16/kalenterit2/index.php?av_v=1&av=160926161002160901&cluokka=TTV15S6&kt=lk&laji=%25||%25&guest=%2Fasiakas12&lang=fin&ui=&yks=&apvm=160725&tiedot=kaikki&ss_ttkal=&ccv=&yhopt=&__cm=&b=1466153181&av_y=0";
	osoite=osoite.replace('https://','').replace('amp.jamk.fi','');
	print "Yhdistetään palvelimeen..."
	c = httplib.HTTPSConnection("amp.jamk.fi")
	c.request("GET", osoite);
	response = c.getresponse()
	if response.status!=200:
		print "VIRHE: "+str(response.status)+" "+response.reason;
		sys.exit("Haku ei onnistunut.")
	data = response.read().replace('\t','').split('\n');
	kivat=[];
	flip_1=False;
	flip_2=False;
	print "Sivu haettu, parsitaan tietoa...";
	for d in data:
		if flip_1:
			kivat.append(d);
			flip_1=False
		if not(flip_1) and d=='<tr><td style="font-family:arial,verdana,helvetica;font-size:10px;"> ':
			flip_1=True;
	print "Löydettiin "+str(len(kivat))+" tapahtumaa";
	urlt=[];
	for k in kivat:
		urlt.append("/asio_v16"+k.replace('<div><a  href="javascript:void(null);" onclick="window.open(\'..','').split("'")[0]);
	return urlt;
