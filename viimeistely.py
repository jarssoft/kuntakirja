import copy
from rutiinit import *
from functools import reduce
import json

def viimeisteleMateriaali(lause):
	lause=poistaPilkut(lause)
	return list(filter(lambda a : a in ["hirsi", "lauta", "puu", "tiili"], lause))

eprint(viimeisteleMateriaali(['Rakennusmateriaali:', 'hirsi', 'lauta', 'puu', 'tiili']))
eprint(viimeisteleMateriaali(['Rakennusmateriaali:', 'tiili']))
eprint(viimeisteleMateriaali(['Rakennusmateriaali:', 'hirsi,', 'lauta']))

def viimeistelePintaala(lause):    
	lause=poistaPilkut(lause)
	lause=list(filter(lambda a : a not in ["n."], lause))
	if(lause[2] not in ["m?", "m2", "ha"]):
		return None
	assert(len(lause)>=3)
	

	try:
		pal = float(lause[1].replace(",","."))
	except ValueError:
		return None


	if(lause[2] in ["m?", "m2"]):
		return pal/10000.0
	if(lause[2] in ["ha"]):
		return pal

eprint(viimeistelePintaala(['Pinta-ala:', '1,2', 'ha']))
eprint(viimeistelePintaala(['Pinta-ala:', '3000', 'm?']))
eprint(viimeistelePintaala(['Pinta-ala:', '132', 'ha,', 'josta', 'peltoa', '43', 'ha']))
eprint(viimeistelePintaala(['Pinta-ala:', 'n.', '2', 'ha']))
eprint(viimeistelePintaala(['Pinta-ala:', 'peltoa', '26', 'ha,', 'metsää', '24', 'ha']))


def viimeisteleRakennusvuosi(lause):    
	assert(len(lause)>=2)
	if len(lause[1])!=4:
		return None
	try:
		pal = int(lause[1])
		return pal
	except ValueError:
		return None

eprint(viimeisteleRakennusvuosi(['Rakennusvuosi:', '1800-luvun', 'puoliväli']))
eprint(viimeisteleRakennusvuosi(['Rakennusvuosi:', '1986']))



def viimeisteleLaajennusTaiRemontti(lause):    
	if len(lause)>3 and lause[0]=='Laajennus' and lause[2]=='remontti:':
		return " ".join(lause[3:])
	else:
		return None


eprint(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1995']))
eprint(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1974,', '1990-91']))
eprint(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1952,', '1993']))

valmiitsukunimet = ("nen", 'ola', 'ala', "salmi", "ola", "mäki", "Kaski", "Liski", "Hopiavuori", "holm", "Ovaska")

def viimeisteleAsukas(lause, ammattilause, psukunimi):

	if lause==['Jaakkola', 'Eeli', 'ja', 'Sylvi,', 'perikunta']:
		return {"etunimet":"Eeli", "sukunimi:": "Jaakkola"}
	if lause==['Kalli', 'Sylvi', 'ja', 'Toivo,', 'perikunta']:
		return {"etunimet":"Sylvi", "sukunimi:": "Kalli"}
	if lause==['Liimola,', 'perikunta']:
		return {"etunimet":"Niilo", "sukunimi:": "Liimola"}
	if lause==['Linnala,', 'perikunta']:
		return {"etunimet":"Esa", "sukunimi:": "Linnala"}
	if lause==['Mäntylä', 'Heikki', 'ja', 'Saara,', 'perikunta']:
		return {"etunimet":"Heikki", "sukunimi:": "Mäntylä"}
	if lause==['Rekola', 'Yrjö', 'ja', 'Toini,', 'perikunta']:
		return {"etunimet":"Yrjö", "sukunimi:": "Rekola"}
	if lause==['Reunanen,', 'perikunta']:
		return {"etunimet":"Aina", "sukunimi:": "Reunanen"}
	if lause==['Siiri', 'Eero,', 'perikunta']:
		return {"etunimet":"Eero", "sukunimi:": "Siiri"}
	if lause==['Suominen,', 'perikunta']:
		return {"etunimet":"?", "sukunimi:": "Suominen"}
	if lause==['Virtanen', 'Olga,', 'perikunta']:
		return {"etunimet":"Olga", "sukunimi:": "Virtanen"}	
			
	eprint(lause)

	lause=poistaPilkut(lause)
	mode=0
	etunimet=[]
	sukunimi=psukunimi
	osnimi=None
	syntymaaika=None
	syntymapaikka=[]
	for s in lause:
		if mode==0 and (s == psukunimi or s.endswith(valmiitsukunimet)):
			assert(mode<1)
			mode=1
			sukunimi=s
			continue
		if s in ['(0.s.','(o.s.','(O.s.']:
			assert(mode<2)
			mode=2
			continue
		if s == 's.':
			assert(mode<3)
			mode=3
			continue
		if mode==0:
			etunimet.append(s)
			continue
		if mode==2:
			osnimi=s[:-1]
			continue
		if mode==3:            
			try:
				syntymaaika=int(s[-4:])
			except ValueError:
				syntymapaikka.append(s)
			continue
		if mode==4:
			syntymapaikka.append(s)
			continue 

	asukas=dict()
	asukas["etunimet"]=etunimet
	assert(len(etunimet)>0)
	if sukunimi != None:
		asukas["sukunimi"]=sukunimi
	if osnimi != None:
		asukas["osnimi"]=osnimi
	if syntymaaika != None:
		asukas["syntymäaika"]=syntymaaika
	if len(syntymapaikka)>0:
		asukas["syntymäpaikka"]=" ".join(syntymapaikka)
	asukas["ammatit"]=poistaPilkut(ammattilause)
	return asukas

eprint(viimeisteleAsukas(['Anna-Liisa',  'Anttila', '(0.s.', 'Pääkkö),', 's.', '7.10.1934', 'Nivala'], ['maatalouslomittaja,', 'eläkeläinen'], 'Anttila'))

eprint(viimeisteleAsukas(['Jukka', 'Sakari', 'Anttila,', 's.', '12.1.1961', 'Turku'], ['kuljetusyrittäjä'], 'Anttila'))

eprint(viimeisteleAsukas(['Aki', 'Aikala,', 's.', '11.4.1960', 'Kurikka'], ['puuseppä'], 'Aikala'))

eprint(viimeisteleAsukas(['Pasi', 'Markus', 'Aho,', 's.', '21.1.1974', 'Eurajoki'], ['maanviljelijä,', 'käytönhoitaja'], 'Aho'))

eprint(viimeisteleAsukas(['Tiina', '(o.s.', 'Nieminen),', 's.', '11.3.1965', 'Eurajoki'], ['varastonhoitaja'], 'Anttila'))

eprint(viimeisteleAsukas(['Aino', 'Helena', '(o.s.', 'Lehtinen),', 's.', '5.3.1932', 'Keuruu'], ['siivooja'], 'Arasmo'))

eprint(viimeisteleAsukas(['Eeva', 'Esteri', 'Ahlman', '(o.s.', 'Valo),', 's.', '24.12.1922', 'Eurajoki'], ['eläkeläinen'], "Ahlman"))

eprint(viimeisteleAsukas(['Aku', 'Franz', 'Aro,', 's.', '4.6.1940', 'Eurajoki'], ['maanviljelijä,', 'eläkeläinen'], 'Aro'))

eprint(viimeisteleAsukas(['Marjatta', 'Ala-Kohtamäki', '(o.s.', 'Karppinen),', 's.', 'Eurajoki'], ['yrittäjä'], 'Ala-Kohtamäki'))

eprint(viimeisteleAsukas(['Seija', 'Hilma', 'Eufrosyne', '(o.s.', 'Kaukkila),', 's.', '30.12.1941'], [], "Aromaa"))

eprint(viimeisteleAsukas(['Kaisa', 'Helena', 'Himanen,', 's.', '11.8.1952', 'Sauvo'], ['sihteeri'], "Aro-Heinilä"))

eprint(viimeisteleAsukas(['Matti', 'Juha,', 's.', '28.12.1959', 'Lappi', 'TI'], ['maanviljelijä'], "Arvela"))

#eprint(viimeisteleAsukas())



def viimeisteleLapset(lause):

	#print(lause)
	#lause=poistaPilkut(lause)
	assert lause[0]=="Lapset:"
	lapset=[]
	uusilapsi=dict()
	uusilapsi["etunimet"]=[]
	kaksoset=[]
	for s in lause[1:]:
		if len(s)>=4 and s[0:4].isdigit() and ")" not in s:			
			uusilapsi["syntymäaika"]=int(s[0:4])
			if len(uusilapsi["etunimet"]) > 0:
				lapset.append(copy.deepcopy(uusilapsi))
			uusilapsi==dict()
			uusilapsi["etunimet"]=[]
			for k in kaksoset:
				k["syntymäaika"]=int(s[0:4])
				lapset.append(copy.deepcopy(k))
			kaksoset=[]
		elif s=="ja" and len(uusilapsi["etunimet"]) > 0:
				kaksoset.append(copy.deepcopy(uusilapsi))
				uusilapsi["etunimet"]=[]
		else:
			if(s[0].isupper()) and len(s)>1 and s[-1]!=":":
				if(s[-1]==","):
					uusilapsi["etunimet"].append(s[0:-1])
					lapset.append(copy.deepcopy(uusilapsi))
					uusilapsi==dict()
					uusilapsi["etunimet"]=[]
				else:
					if s.endswith(valmiitsukunimet):
						uusilapsi["sukunimi"]=s
					else:
						uusilapsi["etunimet"].append(s)
						assert(len(uusilapsi["etunimet"])<=3)
	if(len(uusilapsi["etunimet"])>0):
		lapset.append(copy.deepcopy(uusilapsi))

	entvuosi=1800
	for lapsi in lapset:
		vuosi=lapsi["syntymäaika"] if "syntymäaika" in lapsi else entvuosi
		#assert(vuosi>=entvuosi)
		if vuosi<entvuosi:
			print("Lapset väärässä järjestyksessä.")
		entvuosi=vuosi

		assert(len(lapsi["etunimet"])>0)


	return lapset

eprint(viimeisteleLapset(['Lapset:', 'Tommi', 'Tapani', '1980,', 'Laura-Kaisa', '1983,', 'Teemu', 'Juhani', '1990,']))

eprint(viimeisteleLapset(['Lapset:', 'Tarja', '1961,', 'Kirsi', '1963,', 'Heli', '1967,', 'Merja', '1970,', 'Pasi', '1974']))

eprint(viimeisteleLapset(['Lapset:', 'Outin:', 'Sanna', '1981', 'sairaanhoitajaopiskelija,', 'Aleksi', '1982', 'mate-', 'matiikanopettajaopiskelija,', 'Ilmari', '1989']))

eprint(viimeisteleLapset(['Lapset:', 'Leena', 'Mirjami', '1957,', 'Jaana', 'Kristiina', 'ja', 'Jukka', 'Sakari', '1961,', 'Jarmo', 'Kalevi', '1963,', 'Elina', 'Anna-Liisa', '1966,', 'Tuula', 'Katriina', '1970']))

eprint(viimeisteleLapset(['Lapset:', 'Kari', 'Olavi', '1954,', 'Ari', 'Tapio', '1956', '(k.', '1959),', 'Outi', 'Helena', '1961', '(k.']))

eprint(viimeisteleLapset(['Lapset:', 'Janica', '1988,', 'Susanne', '1989,', 'Jonathan', 'ja', 'Robin', '1992']))

eprint(viimeisteleLapset(['Lapset:', 'Kirsi,', 'Riia']))

eprint(viimeisteleLapset(['Lapset:', 'Roy', 'Krister', 'Mikael', 'Hopiavuori', '1971']))

eprint(viimeisteleLapset(['Lapset:', 'Matti', '1952', 'Erkki', '1955', 'ja', 'Urho', '1956']))

eprint(viimeisteleLapset(['Lapset:', 'Ailin', 'poika:', 'Pekka', '1952']))

eprint(viimeisteleLapset(['Lapset:', 'Aila', '1962,', 'Tuomo', '1963']))

#eprint(viimeisteleLapset(['Lapset:', 'Janica', '2000,', 'Susanne', '1989,', 'Jonathan', 'ja', 'Robin', '1992']))


#eprint(viimeisteleLapset())

def viimeisteleLiitto(lause):    
	assert(len(lause)>=1)
	liitto = dict(tyyppi=lause[0])
	if(len(lause)>1):
		liitto["alkaen"]=int(lause[1])
	return liitto

eprint(viimeisteleLiitto(['avioliitto', '2002']))
eprint(viimeisteleLiitto(['avoliitto']))
eprint(viimeisteleLiitto(['avoliitto', '1993']))

#exit(0) ######################################################################


def viimeistelePerhe(perhe):
	
	if("pinta-ala" in perhe):
		perhe["pinta-ala"]=viimeistelePintaala(perhe["pinta-ala"])
		if(perhe["pinta-ala"]==None):
			del perhe["pinta-ala"]

	if("rakennusvuosi" in perhe):
		perhe["rakennusvuosi"]=viimeisteleRakennusvuosi(perhe["rakennusvuosi"])
		if(perhe["rakennusvuosi"]==None):
			del perhe["rakennusvuosi"]

	if("laajennus/remontti" in perhe):
		perhe["laajennus/remontti"]=viimeisteleLaajennusTaiRemontti(perhe["laajennus/remontti"])
		if(perhe["laajennus/remontti"]==None):
			del perhe["laajennus/remontti"]


	perhe["asukkaat"]=[viimeisteleAsukas(perhe["asukas1"], 
				perhe["ammatti1"] if "ammatti1" in perhe else [], 
				perhe["sukunimi"])]


	if("asukas2" in perhe):
		perhe["asukkaat"].append(viimeisteleAsukas(perhe["asukas2"], 
				perhe["ammatti2"] if "ammatti2" in perhe else [], 
				perhe["sukunimi"]))

	if "asukas1" in perhe:
		del perhe["asukas1"]
	if "asukas2" in perhe:
		del perhe["asukas2"]
	if "ammatti1" in perhe:
		del perhe["ammatti1"]
	if "ammatti2" in perhe:
		del perhe["ammatti2"]

	if "liitto" in perhe:
		perhe["liitto"]=viimeisteleLiitto(perhe["liitto"])

	if("lapset" in perhe):
		perhe["lapset"] = viimeisteleLapset(perhe["lapset"])

	if("rakennusmateriaali" in perhe):
		perhe["rakennusmateriaali"]=list(viimeisteleMateriaali(perhe["rakennusmateriaali"]))

	if("kuvaus" in perhe):
		perhe["kuvaus"]="".join(poistaTavuviivat(perhe["kuvaus"]))

	return perhe