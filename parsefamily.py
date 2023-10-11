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
# tasaus muihin todennäköisiin
# ei usein käytetty termi / kylännimi

# loop over each of the individual text localizations

def ero(nimi, vnimi):
    return abs(ord(nimi[0])-ord(vnimi[0]))*255 + abs(ord(nimi[1])-ord(vnimi[1]))

nimet=[]

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



# filter out weak confidence text localizations
	if conf > args["min_conf"] and h > 37 and h < 41 and w == 1:
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
        
		nimet.append(text)

print(poistaErilaiset(nimet))

