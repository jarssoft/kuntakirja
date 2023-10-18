import math  
# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import copy
import pickle
import os.path

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())

ocrcachefile="cache/"+args["image"]+".cache"

if not os.path.isfile(ocrcachefile):
    # load the input image, convert it from BGR to RGB channel ordering,
    # and use Tesseract to localize each area of text in the input image
    image = cv2.imread(args["image"])
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='fin')
    print(results)

    with open(ocrcachefile, "wb") as fp:   #Pickling
        pickle.dump(results, fp)

with open(ocrcachefile, "rb") as fp:   # Unpickling
    results = pickle.load(fp)


def poistaTavuviivat(lause):
    return list(map(lambda a : (a+" " if (a=="" or a[-1]!='-') else a[0:-1]) , lause))

def poistaPilkut(lause):
    return list(map(lambda a : (a if (a=="" or a[-1]!=',') else a[0:-1]) , lause))

print(poistaTavuviivat(["Tämä","on","koe-","kutsu."]))
print(poistaTavuviivat(["Tämä","on","kutsu", "kokeilemista", "varten."]))
print(poistaTavuviivat(["Tämä","on","-"]))
print(poistaTavuviivat(["-"]))
print(poistaTavuviivat([]))

def viimeisteleMateriaali(lause):
    lause=poistaPilkut(lause)
    return list(filter(lambda a : a in ["hirsi", "lauta", "puu", "tiili"], lause))

print(viimeisteleMateriaali(['Rakennusmateriaali:', 'hirsi', 'lauta', 'puu', 'tiili']))
print(viimeisteleMateriaali(['Rakennusmateriaali:', 'tiili']))
print(viimeisteleMateriaali(['Rakennusmateriaali:', 'hirsi,', 'lauta']))

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

print(viimeistelePintaala(['Pinta-ala:', '1,2', 'ha']))
print(viimeistelePintaala(['Pinta-ala:', '3000', 'm?']))
print(viimeistelePintaala(['Pinta-ala:', '132', 'ha,', 'josta', 'peltoa', '43', 'ha']))
print(viimeistelePintaala(['Pinta-ala:', 'n.', '2', 'ha']))
print(viimeistelePintaala(['Pinta-ala:', 'peltoa', '26', 'ha,', 'metsää', '24', 'ha']))


def viimeisteleRakennusvuosi(lause):    
    assert(len(lause)>=2)
    if len(lause[1])!=4:
        return None
    try:
        pal = int(lause[1])
        return pal
    except ValueError:
        return None

print(viimeisteleRakennusvuosi(['Rakennusvuosi:', '1800-luvun', 'puoliväli']))
print(viimeisteleRakennusvuosi(['Rakennusvuosi:', '1986']))



def viimeisteleLaajennusTaiRemontti(lause):    
    if len(lause)>3 and lause[0]=='Laajennus' and lause[2]=='remontti:':
        return " ".join(lause[3:])
    else:
        return None


print(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1995']))
print(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1974,', '1990-91']))
print(viimeisteleLaajennusTaiRemontti(['Laajennus', '/', 'remontti:', '1952,', '1993']))

def viimeisteleAsukas(lause, ammattilause, psukunimi):   
    lause=poistaPilkut(lause)
    mode=0
    etunimet=[]
    sukunimi=psukunimi
    osnimi=None
    syntymaaika=None
    syntymapaikka=[]
    for s in lause:
        if s in [psukunimi, "Himanen", 'Alhonmäki-Aalonen', 'Vähä-Jusola', 'Ojala', "Elonen","Kellosalmi"]:
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

print(viimeisteleAsukas(['Anna-Liisa',  'Anttila', '(0.s.', 'Pääkkö),', 's.', '7.10.1934', 'Nivala'], ['maatalouslomittaja,', 'eläkeläinen'], 'Anttila'))

print(viimeisteleAsukas(['Jukka', 'Sakari', 'Anttila,', 's.', '12.1.1961', 'Turku'], ['kuljetusyrittäjä'], 'Anttila'))

print(viimeisteleAsukas(['Aki', 'Aikala,', 's.', '11.4.1960', 'Kurikka'], ['puuseppä'], 'Aikala'))

print(viimeisteleAsukas(['Pasi', 'Markus', 'Aho,', 's.', '21.1.1974', 'Eurajoki'], ['maanviljelijä,', 'käytönhoitaja'], 'Aho'))

print(viimeisteleAsukas(['Tiina', '(o.s.', 'Nieminen),', 's.', '11.3.1965', 'Eurajoki'], ['varastonhoitaja'], 'Anttila'))

print(viimeisteleAsukas(['Aino', 'Helena', '(o.s.', 'Lehtinen),', 's.', '5.3.1932', 'Keuruu'], ['siivooja'], 'Arasmo'))

print(viimeisteleAsukas(['Eeva', 'Esteri', 'Ahlman', '(o.s.', 'Valo),', 's.', '24.12.1922', 'Eurajoki'], ['eläkeläinen'], "Ahlman"))

print(viimeisteleAsukas(['Aku', 'Franz', 'Aro,', 's.', '4.6.1940', 'Eurajoki'], ['maanviljelijä,', 'eläkeläinen'], 'Aro'))

print(viimeisteleAsukas(['Marjatta', 'Ala-Kohtamäki', '(o.s.', 'Karppinen),', 's.', 'Eurajoki'], ['yrittäjä'], 'Ala-Kohtamäki'))

print(viimeisteleAsukas(['Seija', 'Hilma', 'Eufrosyne', '(o.s.', 'Kaukkila),', 's.', '30.12.1941'], [], "Aromaa"))

print(viimeisteleAsukas(['Kaisa', 'Helena', 'Himanen,', 's.', '11.8.1952', 'Sauvo'], ['sihteeri'], "Aro-Heinilä"))

print(viimeisteleAsukas(['Matti', 'Juha,', 's.', '28.12.1959', 'Lappi', 'TI'], ['maanviljelijä'], "Arvela"))

#print(viimeisteleAsukas())



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
            if(s[0].isupper()) and s[-1]!=":":
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

print(viimeisteleLapset(['Lapset:', 'Tommi', 'Tapani', '1980,', 'Laura-Kaisa', '1983,', 'Teemu', 'Juhani', '1990,']))

print(viimeisteleLapset(['Lapset:', 'Tarja', '1961,', 'Kirsi', '1963,', 'Heli', '1967,', 'Merja', '1970,', 'Pasi', '1974']))

print(viimeisteleLapset(['Lapset:', 'Outin:', 'Sanna', '1981', 'sairaanhoitajaopiskelija,', 'Aleksi', '1982', 'mate-', 'matiikanopettajaopiskelija,', 'Ilmari', '1989']))

print(viimeisteleLapset(['Lapset:', 'Leena', 'Mirjami', '1957,', 'Jaana', 'Kristiina', 'ja', 'Jukka', 'Sakari', '1961,', 'Jarmo', 'Kalevi', '1963,', 'Elina', 'Anna-Liisa', '1966,', 'Tuula', 'Katriina', '1970']))

print(viimeisteleLapset(['Lapset:', 'Kari', 'Olavi', '1954,', 'Ari', 'Tapio', '1956', '(k.', '1959),', 'Outi', 'Helena', '1961', '(k.']))

print(viimeisteleLapset(['Lapset:', 'Janica', '1988,', 'Susanne', '1989,', 'Jonathan', 'ja', 'Robin', '1992']))

print(viimeisteleLapset(['Lapset:', 'Kirsi,', 'Riia']))


#print(viimeisteleLapset())

def viimeisteleLiitto(lause):    
    assert(len(lause)>=1)
    liitto = dict(tyyppi=lause[0])
    if(len(lause)>1):
        liitto["alkaen"]=int(lause[1])
    return liitto

print(viimeisteleLiitto(['avioliitto', '2002']))
print(viimeisteleLiitto(['avoliitto']))
print(viimeisteleLiitto(['avoliitto', '1993']))

#exit(0) ######################################################################



# 1. blokki
# ylin,vasemmaisin
# alapuoliskon ylin, oikeapuoliskon vasemmaisin
# sama nimi/alku/peräkkäinen aakkosissa
# tekstin korkeus
# tasaus muihin todennäköisiin (x: 1133-1135, y: 1619-1622)
# ei usein käytetty termi / kylännimi

# loop over each of the individual text localizations

def printdict(cars):
    for value in cars:
        print (value,':',cars[value])

def ero(nimi, vnimi):
    return abs(ord(nimi[0])-ord(vnimi[0]))*255 + abs(ord(nimi[1])-ord(vnimi[1]))

sukunimet=[]
kylat=[]
topleft=-1
kylanimet=["Kirkonkylä", "Kuivalahti", "Verkkokari", "Irjanne", "Lapijoki", "Kainu", "Uusi", \
        "Riiko", "Linnamaa", "Saari", "Sydänmaa", "Orjasaari", "Vuojoki", "Huhta", "Köykkä", \
        "Pappila", "Vaimala"]
    
ammatit=["eläkeläinen", "koneenkuljettaja", "varastomies", "varastonhoitaja", "maanviljelijä", \
        "käytönhoitaja", "tradenomi", "siistijä", "kanslisti", "johtaja", "parturi-kampaaja", "hitsaaja",\
        "kartanpiirtäjä", "merimies", "pituusleikkurinhoitaja", "laitoshuoltaja", "yhteyspäällikkö", \
        "palveluneuvoja", "yrittäjä", "baariapulainen", "myyjä", "leipomotyöntekijä", "merkantti", \
        "projekti-insinööri", "laborantti", "matematiikanopettaja", "käsityönopettaja", "puuseppä", \
        "elektroniikkatyöntekijä", "operaattori" ,"perushoitaja", "emäntä", "katsastusinsinööri", \
        "apulaiskansiisti", "pankkitoimihenkilö", "puutarhayrittäjä", "paperityöntekijä", "kotiäiti", \
        "hoitaja", "insinööri", "sairaanhoitaja", "kauppapuutarhuri", "sairaala-apulainen", "maatalousyrittäjä",\
        "muusikko", "asiakaspalveluhenkilö", "muurari", "työsuunnittelija", "autonasentaja", "kassamyyjä", \
        "kirjanpitäjä", "autonkuljettaja", "pitokokki", "kuljetusyrittäjä", "muovityöntekijä",\
        "asfalttilevittäjänkuljettaja", "sihteeri", "maalari", "siivooja", "ATK-suunnittelija", \
        "satamatyönjohtaja", "tutkimusteknikko", "ylioppilas", "instrumenttiasentaja", "palkanlaskija", \
        "tutkimusinsinööri", "tuotantoinsinööri", "koneahtaaja"]

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

if len(kylat)==4:
    y1=results["top"][kylat[0]]
    x1=results["left"][kylat[0]]
    x2=results["left"][kylat[1]]

    kallistus=(x2-x1)/PALSTAH
    palstax=x1-kallistus*y1

    print("Kallistus: {}".format(kallistus))
    print("PalstaX1: {}".format(palstax))
    print("PalstaX2: {}".format(palstax+PALSTAW))


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
	if conf > args["min_conf"] and ((h > 36 and h < 50) or abs(korkeusy-82)<5) and w == 1 and len(text)>1:
		# display the confidence and text to our terminal
		print("Confidence: {}".format(conf))
		print("x: {}".format(x))
		print("y: {}".format(y))
		print("h: {}".format(h))

		print("b: {}".format(b))
		print("p: {}".format(p))
		print("l: {}".format(l))
		print("w: {}".format(w))

		print("Text: {}".format(text))
		print("")


		sukunimet.append(i)
		if(pituus==0):
		    topleft=i
		pituus+=len(text)

samat=poistaErilaiset(list(map(lambda s: results["text"][s], sukunimet)))
print(samat)

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
		print("Confidence: {}".format(conf))
		print("x: {}".format(x))
		print("Text: {}".format(text))
		print("")
		paasukunumet.append(i)

assert(len(paasukunumet)==4)
paasukunumet.append(len(results["text"])-1)
print(paasukunumet)



lasty=0
for a in range(0,4):
    print("\n-------------------")

    rivi=[]
    perhe = dict(sukunimi = results["text"][paasukunumet[0+a]])
    yoffset = results["top"][paasukunumet[0+a]]
    lasty=-1
    
    for i in range(paasukunumet[a], paasukunumet[a+1]):

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

        # filter out weak confidence text localizations
	    if conf > args["min_conf"]:
		    # display the confidence and text to our terminal
		    #print("Confidence: {}".format(conf))
		    #print("x: {}".format(x))
		    #print("y: {}".format(y))
		    #print("h: {}".format(h))
		    #print("Text: {}".format(text))
		    #print("x: {}".format(x))
		    #print("y: {}".format(y))
		    #print("h: {}".format(h))

		    #print("b: {}".format(b))
		    #print("p: {}".format(p))
		    #print("l: {}".format(l))
		    #print("w: {}".format(w))

		    #print ('\n' if w==1 else '', end='')
		    #print("{} ".format(text), end='')

		    if w==1:
		        if(len(rivi)>0):
		            print(lasty, rivi)

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
		                            if(rivi[-1] in ammatit):
		                                perhe["ammatti1"]=rivi
		                                assert(lasty>920)
		                            else:
		                                print("!!!!!!!!!!!!!!!!!!")
		                        if "asukas2" in perhe and "ammatti2" not in perhe:
		                            if(rivi[-1] in ammatit):
		                                perhe["ammatti2"]=rivi
		                                assert(lasty>920)
		                            else:
		                                print("!!!!!!!!!!!!!!!!!!")

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
		    

    print()
    printdict(perhe)


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

    perhe["rakennusmateriaali"]=list(viimeisteleMateriaali(perhe["rakennusmateriaali"]))
    if("kuvaus" in perhe):
        perhe["kuvaus"]="".join(poistaTavuviivat(perhe["kuvaus"]))

    print()
    printdict(perhe)

exit(0)


if topleft>0:
    topleftx = results["left"][topleft]
    toplefty = results["top"][topleft]
    kallistus=-1

    TOLE=18

    print("-------------------")

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
	                print("Kallistus: {}".format(kallistus))
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
        print("Text: {}".format(text))

        # filter out weak confidence text localizations
	    #if conf > args["min_conf"] and h > 37 and h < 41 and w == 1:
else:
    sukunimet=poistaErilaiset(sukunimet)
    print(poistaErilaiset(sukunimet))
