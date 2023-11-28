import math  
from pytesseract import Output #version 0.3.10
import pytesseract
import cv2
import pickle
import os.path

from vakiot import ammatit, kylanimet, PALSTAH, PALSTAW
from viimeistely import * 
import inspect

def errorline():
    """Returns the current line number in our program."""
    return "Error in line "+str(inspect.currentframe().f_back.f_lineno)+": "

# 1. blokki
# ylin,vasemmaisin
# alapuoliskon ylin, oikeapuoliskon vasemmaisin
# sama nimi/alku/peräkkäinen aakkosissa
# tekstin korkeus
# tasaus muihin todennäköisiin (x: 1133-1135, y: 1619-1622)
# ei usein käytetty termi / kylännimi

# loop over each of the individual text localizations

def korjaasukunimi(text):
	if text=="Aijälä":
		text="Äijälä"
	if text=="Arnfors":
		text="Ärnfors"
	if text[0].startswith(('i','l')):
		text="I"+text[1:]
	return text

def parsiResults(results, minconf):

	sukunimet=[]
	kylat=[]
	topleft=-1

	for i in range(0, len(results["text"])):
		conf = int(results["conf"][i])
		text = results["text"][i]
		if conf > minconf and text in kylanimet:
			kylat.append(i)

	kylatstr=str(list(map(lambda s: results["text"][s].capitalize(), kylat)))

	if(len(kylat)<3):
		return [errorline()+"len(kylat)<4, " + kylatstr]

	eprint("kylat", kylatstr)

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
	samat=[]

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
		#assert(text!="Aijälä"),text
		
		conf = int(results["conf"][i])

		korkeusy = results["top"][kylat[0]]-y

		# filter out weak confidence text localizations
		if(len(text)>1):			
			text=korjaasukunimi(text)
			if conf > minconf and ((h > 36 and h < 55) or abs(korkeusy-82)<5) and w == 1 and text!="Lapset:" and text[0].isupper() and y < 2000: #poistettu abs(korkeusy-82)<5
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

				if(text[0].islower()):
					return [errorline()+"nimi "+text+" alkaa pienellä alkukirjaimella."]

				sukunimet.append(i)
				samat.append(text)

				if(pituus==0):
					topleft=i
				
				pituus+=len(text)

	#eprint(list(map(lambda s: results["text"][s], sukunimet)))
	samat=yleisemmatEnsin(samat)[:4]
	eprint(samat)

	if(len(samat)!=4):
		return [errorline()+"len(samat)!=4 "+str(samat)]
	
	if(ero(samat[0], samat[-1])>4*255):
		return [errorline()+"Sukunimet liian kaukana toisistaan"+str(samat)]

	paasukunimet=[]
	kuvat=[]

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
		if(len(text)>1):
			text=korjaasukunimi(text)
			if text in samat and y < 2000:
				# display the confidence and text to our terminal
				eprint("Confidence: {}".format(conf))
				eprint("x: {}".format(x))
				eprint("h: {}".format(h))
				eprint("Text: {}".format(text))
				eprint("")
				paasukunimet.append(i)
				kuvat.append((x,y))				

	assert((len(paasukunimet)==4))
	if(len(paasukunimet)!=4):
		return [errorline()+"len(paasukunimet)!=4, "+str(list(map(lambda s: results["text"][s], paasukunimet)))+str(samat)]
	
	assert(len(paasukunimet)==4)
	paasukunimet.append(len(results["text"])-1)
	assert ero(samat[0], samat[3])<5*255, "Sukunimet liian kaukana toisistaan"
	eprint(paasukunimet)

	lasty=0
	perheet=[]

	for a in range(0,4):
		eprint("\n-------------------")

		rivi=[]
		perhe = dict(sukunimi = korjaasukunimi(results["text"][paasukunimet[0+a]]))
		yoffset = results["top"][paasukunimet[0+a]]
		lasty=-1
		
		for i in range(paasukunimet[a], paasukunimet[a+1]+2):

			if i<=paasukunimet[a+1]:
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

			if(i>=paasukunimet[a+1]):
				text=""

			# filter out weak confidence text localizations
			if conf > minconf:
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

						if rivi==['MTT', 'RUOKA', 'Marjukka', 'Paavola,', 's.', '14.3.1978', 'Eurajoki']:
							rivi=['Mari-Sanna', 'Marjukka', 'Paavola,', 's.', '14.3.1978', 'Eurajoki']

						if rivi==['amäki', '(o.s.', 'Jussila),', 's.', '25.11.1946']:
							rivi=['Liisa', 'Kaarina', 'Kukkamäki', '(o.s.', 'Jussila),', 's.', '25.11.1946']							

						if rivi==['Jannen', 'isoisovanhemmat', 'Fredrik', 'ja', 'Aleksandra', 'Salonen', 'ostivat']:
							rivi=['Jannen', 'isoisovanhemmat', 'Fredrik', 'ja', 'Aleksandra', 'ostivat']

						if rivi==['rd', 'Eeva', 'Kaarina', '1968,', 'Tuula', 'Kristiina', '1973,', 'Mirja', 'Susanna']:
							rivi=['1965', 'Eeva', 'Kaarina', '1968,', 'Tuula', 'Kristiina', '1973,', 'Mirja', 'Susanna']

						#if rivi==['Aijälä']:
						#	rivi=['Äijälä']

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
						
							if lasty>910 and "lapset" not in perhe and "kuvaus" not in perhe:
								if(rivi[0] == "avioliitto" or rivi[0] == "avoliitto"):
									perhe["liitto"]=rivi
								else:
									if('perikunta' in rivi or 's.' in rivi or '(o.s.' in rivi or (perhe["sukunimi"] in rivi and rivi.index(perhe["sukunimi"])>0)):
										if "asukas1" not in perhe:
											perhe["asukas1"]=rivi
											assert(lasty>910)
										elif "asukas2" not in perhe:
											perhe["asukas2"]=rivi
											assert(lasty>910)
										else:
											perhe["asukas2"]+=rivi
									else:
										if "asukas1" in perhe and "ammatti1" not in perhe and "asukas2" not in perhe:
											if(rivi[-1].endswith(ammatit)):
												perhe["ammatti1"]=rivi
												assert(lasty>910)
											else:
												eprint("!!!!!!!!!!!!!!!!!!")
										if "asukas2" in perhe and "ammatti2" not in perhe:
											if(rivi[-1].endswith(ammatit)):
												perhe["ammatti2"]=rivi
												assert(lasty>910)
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
		if(not "asukas1" in perhe):
			print(perhe)
			return ["Perheessä pitää olla vähintään yksi asukas."]

		perheet.append(viimeistelePerhe(perhe))
		
		eprint()
		#eprintdict(perhe)

	perheet[2], perheet[1] = perheet[1], perheet[2]
	return perheet, kuvat

def cropFile(imagefile, piste, i):
	image = cv2.imread("images/"+imagefile)
	cropped_image = image[(piste[1]+370):(piste[1]+900), (piste[0]):(piste[0]+950)]
	cv2.imwrite("photos/"+imagefile+"-"+str(i)+".jpg", cropped_image)

def parseFile(imagefile, useCache, minconf):

	ocrcachefile="cache/"+imagefile+".cache"
	cfg_filename = 'userwords.txt'

	if not os.path.isfile(ocrcachefile) or useCache:
		# load the input image, convert it from BGR to RGB channel ordering,
		# and use Tesseract to localize each area of text in the input image
		image = cv2.imread("images/"+imagefile)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='fin', config="--user-words userwords.txt")
		eprint(results)

		with open(ocrcachefile, "wb") as fp:   #Pickling
			pickle.dump(results, fp)

	with open(ocrcachefile, "rb") as fp:   # Unpickling
		results = pickle.load(fp)

	pal = parsiResults(results, minconf)
	#for i in range(0,4):
	#	cropFile(imagefile, pal[1][i], i)

	return pal[0]

"""
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
	sukunimet=yleisemmatEnsin(sukunimet)[:4]
	eprint(yleisemmatEnsin(sukunimet))
"""