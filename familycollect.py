import argparse
from parsefamily import *
from rutiinit import *


perheet=[]
for p in range(96,120):
    print("parse ",p)
    perheet+=parseFile(str(p)+".png", 0, 0)

print("-----------------")

for perhe in perheet:
    print()
    print(perhe)
	#eprint(perhe)