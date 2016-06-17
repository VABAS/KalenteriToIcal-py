#encoding=UTF-8
import sys, httplib, time;
def hae_yksi_varaus(osoite):
	osoite=osoite.replace('https://','').replace('amp.jamk.fi','');
	print "Yhdistetään palvelimeen..."
	c = httplib.HTTPSConnection("amp.jamk.fi")
	c.request("GET", osoite);
	response = c.getresponse()
	if response.status!=200:
		print "VIRHE: "+str(response.status)+" "+response.reason;
		sys.exit("Haku ei onnistunut.")
	data = response.read().replace('\t','').split('\n');
	kivat="";
	flip_1=False;
	flip_2=False;
	print "Sivu haettu, parsitaan tietoa...";
	for d in data:
		if d.replace(' ','') == "<th>Opintojakso</th><th>Selite</th>":
			flip_1=True;
		if flip_1 and d.replace(' ','') == "<trbgcolor=\"#e7e7e7\">":
			flip_2=True;
		if flip_1 and flip_2:
			if d == "</table></td></tr></table></div>":
				break;
			kivat=kivat+d;

	kivat=kivat.split('<tr  bgcolor="#e7e7e7" >');

	#
	#pvm=0;
	#aika=1;
	#tila=2;
	#ryhma=3;
	#opettaja=4;
	#kurssitunnus=5;
	#
	i=1;
	vevents="";
	while i<len(kivat):
		rivi=kivat[i].replace('<td>','').replace('</td></tr>','').replace('<font face="arial,verdana" size=-1>','').split('</td>');
		pvm=rivi[0].split(';')[1].split('.');#päivä=0, kuukausi=1, vuosi=3
		aika=rivi[1].replace(' - ',':').split(':');#alkutunti=0, alkumin=1,lopputunti=2, loppumin=3
		vevents=vevents+"BEGIN:VEVENT\r\n";
		vevents=vevents+"UID:"+rivi[5].replace(' ','_')+"@"+pvm[2]+pvm[1]+pvm[0]+"T"+aika[0]+aika[1]+"00"+str(i)+"\r\n";
		vevents=vevents+"DTSTAMP:"+time.strftime("%Y%m%d")+"T"+time.strftime("%H%M%S")+"\r\n";
		vevents=vevents+"DTSTART:"+pvm[2]+pvm[1]+pvm[0]+"T"+aika[0]+aika[1]+"00\r\n";
		vevents=vevents+"DTEND:"+pvm[2]+pvm[1]+pvm[0]+"T"+aika[2]+aika[3]+"00\r\n";
		vevents=vevents+"SUMMARY:"+rivi[5]+"\r\n";
		vevents=vevents+"LOCATION:"+rivi[2]+"\r\n";
		vevents=vevents+"DESCRIPTION:"+rivi[4]+"\r\n";
		vevents=vevents+"END:VEVENT\r\n";
		i=i+1;
	print "Löydettiin "+str(len(kivat))+" esiintymää";
	return vevents.decode('iso-8859-1').encode('utf8');
