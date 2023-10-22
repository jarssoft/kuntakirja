import argparse
from parsefamily import *
from rutiinit import *


fails=0
for p in range(69,170):
    print("parse",p,end="")
    perheet=parseFile(str(p)+".png", 0, 0)
    print(" OK" if len(perheet)==4 else " Fail " + perheet[0])
    if len(perheet)!=4:
        fails+=1
print("Total fails ",fails)

exit(0)

perheet=[]
for p in range(69,170):
    print("parse ",p)
    perheet+=parseFile(str(p)+".png", 0, 0)

print("-----------------")

for perhe in perheet:
    #print()
    if("sukunimi" in perhe):
        print(perhe["sukunimi"])
    else:
        print(perhe)
	#eprint(perhe)