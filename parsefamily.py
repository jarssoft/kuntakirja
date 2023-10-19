import math  
# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import copy
import pickle
import os.path
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
ap.add_argument("-r", "--refresh",
	help="mininum confidence value to filter weak text detection")
ap.add_argument("-v", "--verbose",
	help="")

def eprint(*args, **kwargs):
    #print(*args, file=sys.stderr, **kwargs)
    pass

args = vars(ap.parse_args())

ocrcachefile="cache/"+args["image"]+".cache"

if not os.path.isfile(ocrcachefile) or args["refresh"]:
    # load the input image, convert it from BGR to RGB channel ordering,
    # and use Tesseract to localize each area of text in the input image
    image = cv2.imread("images/"+args["image"])
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='fin')
    eprint(results)

    with open(ocrcachefile, "wb") as fp:   #Pickling
        pickle.dump(results, fp)

with open(ocrcachefile, "rb") as fp:   # Unpickling
    results = pickle.load(fp)


def poistaTavuviivat(lause):
    return list(map(lambda a : (a+" " if (a=="" or a[-1]!='-') else a[0:-1]) , lause))

def poistaPilkut(lause):
    return list(map(lambda a : (a if (a=="" or a[-1]!=',') else a[0:-1]) , lause))

eprint(poistaTavuviivat(["Tämä","on","koe-","kutsu."]))
eprint(poistaTavuviivat(["Tämä","on","kutsu", "kokeilemista", "varten."]))
eprint(poistaTavuviivat(["Tämä","on","-"]))
eprint(poistaTavuviivat(["-"]))
eprint(poistaTavuviivat([]))

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

valmiitsukunimet = ("nen", 'ola', 'ala', "salmi", "ola", "mäki", "ila")

def viimeisteleAsukas(lause, ammattilause, psukunimi):   
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
    #lause=poistaPilkut(lause)
    assert lause[0]=="Lapset:"
    lapset=[]
    uusilapsi=dict()
    uusilapsi["etunimet"]=[]
    kaksoset=[]
    for s in lause[1:]:
        if len(s)>=4 and s[0:4].isdigit() and ")" not in s:
            uusilapsi["syntynyt"]=int(s[0:4])
            lapset.append(copy.deepcopy(uusilapsi))
            uusilapsi==dict()
            uusilapsi["etunimet"]=[]
            for k in kaksoset:
                k["syntynyt"]=int(s[0:4])
                lapset.append(copy.deepcopy(k))
            kaksoset=[]
        elif (s=="ja"):
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
                    uusilapsi["etunimet"].append(s)
                    assert(len(uusilapsi["etunimet"])<=3)
    if(len(uusilapsi["etunimet"])>0):
        lapset.append(copy.deepcopy(uusilapsi))
    return lapset

eprint(viimeisteleLapset(['Lapset:', 'Tommi', 'Tapani', '1980,', 'Laura-Kaisa', '1983,', 'Teemu', 'Juhani', '1990,']))

eprint(viimeisteleLapset(['Lapset:', 'Tarja', '1961,', 'Kirsi', '1963,', 'Heli', '1967,', 'Merja', '1970,', 'Pasi', '1974']))

eprint(viimeisteleLapset(['Lapset:', 'Outin:', 'Sanna', '1981', 'sairaanhoitajaopiskelija,', 'Aleksi', '1982', 'mate-', 'matiikanopettajaopiskelija,', 'Ilmari', '1989']))

eprint(viimeisteleLapset(['Lapset:', 'Leena', 'Mirjami', '1957,', 'Jaana', 'Kristiina', 'ja', 'Jukka', 'Sakari', '1961,', 'Jarmo', 'Kalevi', '1963,', 'Elina', 'Anna-Liisa', '1966,', 'Tuula', 'Katriina', '1970']))

eprint(viimeisteleLapset(['Lapset:', 'Kari', 'Olavi', '1954,', 'Ari', 'Tapio', '1956', '(k.', '1959),', 'Outi', 'Helena', '1961', '(k.']))

eprint(viimeisteleLapset(['Lapset:', 'Janica', '1988,', 'Susanne', '1989,', 'Jonathan', 'ja', 'Robin', '1992']))

eprint(viimeisteleLapset(['Lapset:', 'Kirsi,', 'Riia']))


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



# 1. blokki
# ylin,vasemmaisin
# alapuoliskon ylin, oikeapuoliskon vasemmaisin
# sama nimi/alku/peräkkäinen aakkosissa
# tekstin korkeus
# tasaus muihin todennäköisiin (x: 1133-1135, y: 1619-1622)
# ei usein käytetty termi / kylännimi

# loop over each of the individual text localizations

def eprintdict(cars):
    for value in cars:
        eprint (value,':',cars[value])

def ero(nimi, vnimi):
    return abs(ord(nimi[0])-ord(vnimi[0]))*255 + abs(ord(nimi[1])-ord(vnimi[1]))

sukunimet=[]
kylat=[]
topleft=-1
kylanimet=["Kirkonkylä", "Kuivalahti", "Verkkokari", "Irjanne", "Lapijoki", "Kainu", "Uusi", \
        "Riiko", "Linnamaa", "Saari", "Sydänmaa", "Orjasaari", "Vuojoki", "Huhta", "Köykkä", \
        "Pappila", "Vaimala", "Hankkila"]
    
ammatit=("eläkeläinen", "varastomies", "varastonhoitaja", "maanviljelijä", "painaja", \
        "käytönhoitaja", "tradenomi", "siistijä", "parturi-kampaaja", "hitsaaja", "ahtaaja", \
        "kartanpiirtäjä", "merimies", "pituusleikkurinhoitaja", "huoltaja", "päällikkö", \
        "palveluneuvoja", "merkantti", "laborantti", "opettaja", "seppä", "asentaja", "ahtaaja", \
        "operaattori", "emäntä", "kanslisti", "toimihenkilö", "kotiäiti", "lehtori" , "painaja", \
        "insinööri", "hoitaja", "puutarhuri", "apulainen", "muusikko", "asiakaspalveluhenkilö", \
        "muurari", "suunnittelija", "asentaja", "myyjä", "kirjanpitäjä", "kokki", "yrittäjä", \
        "työntekijä", "kuljettaja", "sihteeri", "maalari", "siivooja", "suunnittelija", "insinööri", \
        "johtaja", "teknikko", "ylioppilas", "palkanlaskija", "tarkastaja", "kokooja", "päällystäjä", \
        "kirvesmies", "verhooja", "kotirouva", "keittäjä", "kalastaja", "laatoittaja", "ompelija", \
        "koulunkäyntiavustaja", "sähkömestari", "opiskelija", "autoilija", "virkailija", "lomittaja", \
        "palomies", "talonmies", "kiinteistöhuoltomies", "kirjaltaja", "lääke-esittelijä", "rakennusmies", \
        "käynnissäpitäjä", "työläinen", "rehtori", "stuertti", "tuotekehitysassistentti", "vartija", \
        "ohjaaja", "liikkeenharjoittaja", "konstaapeli", "huoltomies", "laitosmies", "kuivaaja", \
        "näytteenottaja"
        )

assert(ero("Jari", "Ilona") == 255+11)
assert(ero("Saari", "Salonen") == 0)

def etaisyydet(nimet):
    pal=[]
    for nimi in nimet:        
        erot=0        
        for vnimi in nimet:
            erot+=ero(nimi, vnimi)
        pal.append(erot)
    return pal




# Poistaa nimet jotka ovat muita kauempana aakkosjärjestyksessä
def poistaErilaiset(nimet):    
    return [x for _, x in sorted(zip(etaisyydet(nimet), nimet))][:4]

for i in range(0, len(results["text"])):
	conf = int(results["conf"][i])
	text = results["text"][i]
	if conf > args["min_conf"] and text in kylanimet:
		kylat.append(i)

PALSTAW=1134
PALSTAH=1620

eprint("kylat",list(map(lambda s: results["text"][s].capitalize(), kylat)))
if len(kylat)==4:
    y1=results["top"][kylat[0]]
    x1=results["left"][kylat[0]]
    x2=results["left"][kylat[1]]

    kallistus=(x2-x1)/PALSTAH
    palstax=x1-kallistus*y1

    eprint("Kallistus: {}".format(kallistus))
    eprint("PalstaX1: {}".format(palstax))
    eprint("PalstaX2: {}".format(palstax+PALSTAW))


pituus=0
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]

	b = results["block_num"][i]
	p = results["par_num"][i]
	l = results["line_num"][i]
	w = results["word_num"][i]

	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])

	korkeusy = results["top"][kylat[0]]-y

    # filter out weak confidence text localizations
	if conf > args["min_conf"] and ((h > 36 and h < 50) or abs(korkeusy-82)<5) and w == 1 and len(text)>1 and text!="Lapset:":
		# display the confidence and text to our terminal
		eprint("Confidence: {}".format(conf))
		eprint("x: {}".format(x))
		eprint("y: {}".format(y))
		eprint("h: {}".format(h))

		eprint("b: {}".format(b))
		eprint("p: {}".format(p))
		eprint("l: {}".format(l))
		eprint("w: {}".format(w))

		eprint("Text: {}".format(text))
		eprint("")


		sukunimet.append(i)
		if(pituus==0):
		    topleft=i
		pituus+=len(text)

eprint(list(map(lambda s: results["text"][s].capitalize(), sukunimet)))
samat=poistaErilaiset(list(map(lambda s: results["text"][s].capitalize(), sukunimet)))
eprint(samat)

paasukunumet=[]

for i in sukunimet:
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]

	b = results["block_num"][i]
	p = results["par_num"][i]
	l = results["line_num"][i]
	w = results["word_num"][i]

	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])

	korkeusy = results["top"][kylat[0]]-y

    # filter out weak confidence text localizations
	if text in samat:
		# display the confidence and text to our terminal
		eprint("Confidence: {}".format(conf))
		eprint("x: {}".format(x))
		eprint("h: {}".format(h))
		eprint("Text: {}".format(text))
		eprint("")
		paasukunumet.append(i)

assert(len(paasukunumet)==4)
paasukunumet.append(len(results["text"])-1)
assert ero(samat[0], samat[3])<5*255, "Sukunimet liian kaukana toisistaan"
eprint(paasukunumet)



lasty=0
for a in range(0,4):
    eprint("\n-------------------")

    rivi=[]
    perhe = dict(sukunimi = results["text"][paasukunumet[0+a]])
    yoffset = results["top"][paasukunumet[0+a]]
    lasty=-1
    
    for i in range(paasukunumet[a], paasukunumet[a+1]+2):

	    if i<=paasukunumet[a+1]:
	        # extract the bounding box coordinates of the text region from
	        # the current result
	        x = results["left"][i]
	        y = results["top"][i] - yoffset
	        w = results["width"][i]
	        h = results["height"][i]

	        b = results["block_num"][i]
	        p = results["par_num"][i]
	        l = results["line_num"][i]
	        w = results["word_num"][i]

	        # extract the OCR text itself along with the confidence of the
	        # text localization
	        text = results["text"][i]
	        conf = int(results["conf"][i])

	    if(i>=paasukunumet[a+1]):
	        text=""

        # filter out weak confidence text localizations
	    if conf > args["min_conf"]:
		    # display the confidence and text to our terminal
		    #eprint("Confidence: {}".format(conf))
		    #eprint("x: {}".format(x))
		    #eprint("y: {}".format(y))
		    #eprint("h: {}".format(h))
		    #eprint("Text: {}".format(text))
		    #eprint("x: {}".format(x))
		    #eprint("y: {}".format(y))
		    #eprint("h: {}".format(h))

		    #eprint("b: {}".format(b))
		    #eprint("p: {}".format(p))
		    #eprint("l: {}".format(l))
		    #eprint("w: {}".format(w))

		    #eprint ('\n' if w==1 else '', end='')
		    #eprint("{} ".format(text), end='')

		    if w==1:
		        if(len(rivi)>0):
		            eprint(lasty, rivi)

		            if(len(rivi)<1600):

		                if(lasty<365 and "asukas1" not in perhe):
		                    if(abs(lasty-48)<4):
		                        if(rivi[0] in kylanimet):
		                            perhe["kyla"]=" ".join(rivi)
		                        else:
		                            perhe["tontti"]=" ".join(rivi)
		                    if(abs(lasty-82)<5):
		                        if(rivi[0] in kylanimet):
		                            if("kyla" in perhe):
		                                perhe["tontti"]=perhe["kyla"]
		                            perhe["kyla"]=" ".join(rivi)
		                    if(rivi[0] == "Pinta-ala:"):
		                        perhe["pinta-ala"]=rivi
		                    if(rivi[0] == "Rakennusmateriaali:"):
		                        perhe["rakennusmateriaali"]=rivi
		                    if(rivi[0] == "Rakennusvuosi:"):
		                        perhe["rakennusvuosi"]=rivi
		                    if(rivi[0] == "Laajennus"):
		                        perhe["laajennus/remontti"]=rivi
                    
		                if lasty>920 and "lapset" not in perhe and "kuvaus" not in perhe:
		                    if(rivi[0] == "avioliitto" or rivi[0] == "avoliitto"):
		                        perhe["liitto"]=rivi
		                    else:
		                        if('s.' in rivi or perhe["sukunimi"] in rivi):
		                            if "asukas1" not in perhe:
		                                perhe["asukas1"]=rivi
		                                assert(lasty>920)
		                            else:
		                                perhe["asukas2"]=rivi
		                                assert(lasty>920)
		                        else:
		                            if "asukas1" in perhe and "ammatti1" not in perhe and "asukas2" not in perhe:
		                                if(rivi[-1].endswith(ammatit)):
		                                    perhe["ammatti1"]=rivi
		                                    assert(lasty>920)
		                                else:
		                                    eprint("!!!!!!!!!!!!!!!!!!")
		                            if "asukas2" in perhe and "ammatti2" not in perhe:
		                                if(rivi[-1].endswith(ammatit)):
		                                    perhe["ammatti2"]=rivi
		                                    assert(lasty>920)
		                                else:
		                                    eprint("!!!!!!!!!!!!!!!!!!")

		                if(lasty>985 and "asukas1" in perhe and "kuvaus" not in perhe):
		                    if(rivi[0] == "Lapset:"):
		                        perhe["lapset"]=rivi
		                    else: 
		                        if "lapset" in perhe and lasty-lastlasty<=50:
		                            perhe["lapset"]+=rivi

		                if(lasty>985 and "asukas1" in perhe and rivi[0] != "Lapset:"):
		                    if(rivi[0] != "Lapset:" and lasty-lastlasty>50 and "kuvaus" not in perhe):
		                        perhe["kuvaus"]=rivi
		                    elif "kuvaus" in perhe:
		                        perhe["kuvaus"]+=rivi


		        rivi=[]
		        lastlasty=lasty
		        lasty=y


		    rivi.append(text)
		    

    eprint()
    eprintdict(perhe)
    assert("asukas1" in perhe)


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

    eprint()
    eprintdict(perhe)

    print(perhe)

exit(0)


if topleft>0:
    topleftx = results["left"][topleft]
    toplefty = results["top"][topleft]
    kallistus=-1

    TOLE=18

    eprint("-------------------")

    # Sukunimet koordinaatin mukaan

    for i in range(0, len(results["text"])):
	    # extract the bounding box coordinates of the text region from
	    # the current result
	    x = results["left"][i]
	    y = results["top"][i]
	    conf = int(results["conf"][i])
	    
	    if conf > args["min_conf"]:
	        if kallistus == -1:
	            if(abs(abs(toplefty-y)-PALSTAH) < TOLE):
	                bottomleft=i
	                kallistus=(x-topleftx)/PALSTAH
	                eprint("Kallistus: {}".format(kallistus))
	        if kallistus != -1:
	            if abs(abs(topleftx-x)-PALSTAW)<TOLE \
                    and abs(toplefty-(y+PALSTAW*kallistus))<TOLE:
	                topright=i
	            #if(abs(math.sqrt((topleftx-x)*(topleftx-x)+(toplefty-y)*(toplefty-y)) - 1976) < TOLE):
	            #    bottomright=i
	            if abs(abs(topleftx-(x-PALSTAH*kallistus))-PALSTAW) < TOLE \
                    and abs(toplefty+PALSTAH-(y+PALSTAW*kallistus)) < TOLE:
	                bottomright=i

    for i in [topleft, bottomleft, topright, bottomright]:
        text = results["text"][i]
        eprint("Text: {}".format(text))

        # filter out weak confidence text localizations
	    #if conf > args["min_conf"] and h > 37 and h < 41 and w == 1:
else:
    sukunimet=poistaErilaiset(sukunimet)
    eprint(poistaErilaiset(sukunimet))
