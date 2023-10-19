import argparse
from parsefamily import *
from rutiinit import *

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

perheet = parseFile(args["image"], args["refresh"], args["min_conf"])
          
print("-----------------")

for perhe in perheet:
	print()
	eprintdict(perhe)