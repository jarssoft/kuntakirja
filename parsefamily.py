import math  
# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())


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

#exit(0)


# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to localize each area of text in the input image
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='fin')

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
