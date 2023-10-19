import math  
from pytesseract import Output
import pytesseract
import argparse
import cv2
import pickle
import os.path

from vakiot import ammatit, kylanimet
from rutiinit import *
from viimeistely import * 

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




eprint(poistaTavuviivat(["Tämä","on","koe-","kutsu."]))
eprint(poistaTavuviivat(["Tämä","on","kutsu", "kokeilemista", "varten."]))
eprint(poistaTavuviivat(["Tämä","on","-"]))
eprint(poistaTavuviivat(["-"]))
eprint(poistaTavuviivat([]))


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
