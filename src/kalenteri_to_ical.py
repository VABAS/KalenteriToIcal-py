#!/usr/bin/python
#coding=UTF-8
from lib.yksi_varaus import hae_yksi_varaus as hae_yksi_varaus;
from lib.hae_lukujarjestys_urlt import hae_lukujarjestys_urlt as hae_lukujarjestys_urlt;
import time,sys;
if len(sys.argv)<3:
	sys.exit("Ei tarpeeksi argumentteja!\nKäyttö: "+sys.argv[0]+" osoite tiedosto.ics [eimon]");
monistus=False;
if len(sys.argv)==4:
	if sys.argv[3]=="eimon":
		print "Tapahtumia ei monisteta käyttäjän pyynnöstä";
		monistus=True;
osoite=sys.argv[1];
tiedosto=sys.argv[2];
tapahtumat=hae_lukujarjestys_urlt(osoite);
vevents="";
for t in tapahtumat:
	vevents=vevents+hae_yksi_varaus(t,monistus);
print "Kirjoitetaan tapahtumat tiedostoon "+tiedosto;
tied=open(tiedosto,'w');
tied.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//sikkela\r\n"+vevents+"END:VCALENDAR\r\n");
tied.close();
print "Valmis";
