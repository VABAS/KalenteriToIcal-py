#!/usr/bin/python3
#coding=UTF-8
from lib.yksi_varaus import hae_yksi_varaus as hae_yksi_varaus;
from lib.hae_lukujarjestys_urlt import hae_lukujarjestys_urlt as hae_lukujarjestys_urlt;
import time,sys;
if len(sys.argv)<3:#Tarkistetaan että käyttäjä on syöttänyt tarvittavat argumentit
	sys.exit("Ei tarpeeksi argumentteja!\nKäyttö: "+sys.argv[0]+" osoite tiedosto.ics [eimon] [eikys]");
monistus=False;
eikys=False
if len(sys.argv)>=4:
	for arg in sys.argv:
		if arg=="eimon":
			print("Tapahtumia ei monisteta käyttäjän pyynnöstä")
			monistus=True;
		if arg=="eikys":
			print("Tuodaan kaikki tapahtumat kysymättä")
			eikys=True;
		
osoite=sys.argv[1];
tiedosto=sys.argv[2];
tapahtumat=hae_lukujarjestys_urlt(osoite);#Kutsutaan osoitteet hakevaa aliohjelmaa
vevents="";
kurssit=[]
for t in tapahtumat:#Käydään osoitteet läpi yksi kerrallaan
	tiedot=hae_yksi_varaus(t,monistus);#Ja kutsutaan jokaisella osoitteella tapahtumat hakevaa aliohjelmaa
	if tiedot[1] in kurssit:#Tarkistetaan ettei kurssia tällä tunnuksella ole jo tuotu
		print("INFO: \"Kurssi "+tiedot[0]+"\" on jo tuotu")
	else:
		if eikys:
			kys="k"
		else:
			kys=input("Haluatko tuoda kurssin "+tiedot[0]+"? K=Kyllä, Kaikki muut=Ei: ");#Tiedustellaan haluaako käyttäjä tuoda löydetyn kurssin
		if kys=="k" or kys=="K":
			vevents=vevents+tiedot[2];#Jos haluaa niin tuodaan
			print("Tuotiin kurssi "+tiedot[0])
		else:
			print("Ei tuotu kurssia "+tiedot[0])
		kurssit.append(tiedot[1])#Kirjoitetaan kurssitunnus tuotujen taulukkoon
print("Kirjoitetaan tapahtumat tiedostoon "+tiedosto)
tied=open(tiedosto,'w');#Kirjoitetaan tapahtumat käyttäjän haluamaan .ics tiedostoon
tied.write("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//sikkela\r\n"+vevents+"END:VCALENDAR\r\n");
tied.close();
print("Valmis")
