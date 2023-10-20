import argparse
from parsefamily import *
from rutiinit import *

fails=0
for p in range(69,135):
    print("parse",p,end="")
    perheet=parseFile(str(p)+".png", 0, 0)
    print(" OK" if len(perheet)==4 else " Fail")
    if len(perheet)!=4:
        fails+=1
print("Total fails ",fails)

exit(0)

perheet=[]
for p in range(69,120):
    print("parse ",p)
    perheet+=parseFile(str(p)+".png", 0, 0)

print("-----------------")

for perhe in perheet:
    #print()
    print(perhe["sukunimi"])
	#eprint(perhe)