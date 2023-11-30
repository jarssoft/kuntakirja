import argparse
from parsefamily import *
from rutiinit import *
import itertools
import copy

fails=0
last="Aaaa"
for p in range(69,464):
    print("parse",p,end="")
    perheet=parseFile(str(p)+".png", 0, 0)
    print(" OK" if len(perheet)==4 else " Fail " + perheet[0])
    if len(perheet)!=4:
        fails+=1
    else:
        for perhe in perheet:
            #print (perhe["sukunimi"])
            assert perhe["sukunimi"]>=last
            last=perhe["sukunimi"]
            
print("Total fails ",fails)

#exit(0)

perheet=[]
pid=0
for p in range(69,464):
    print("parse ",p)
    uudet=parseFile(str(p)+".png", 0, 0)
    #for kuva in range(0,4):
    #    uudet[kuva]["kirjassa"]={"sivu": p, "kuva": kuva}
    for perhe in uudet:
        del perhe ['sukunimi']
        del perhe ['asukkaat']
        if "liitto" in perhe:
            del perhe ['liitto']
        if "lapset" in perhe:
            del perhe ['lapset']
        if "kuvaus" in perhe:
            del perhe ['kuvaus']
        perhe["id"]=pid
        if "tontti" in perhe:
            perheet.append(perhe)        
        pid=pid+1
    #perheet+=uudet

print("-----------------")
"""
for perhe in perheet:
    #print()
    if("sukunimi" in perhe):
        print(perhe["sukunimi"])
    else:
        print(perhe)
	#eprint(perhe)

print("-----------------")

for perhe in perheet:
    #print()
    print(perhe["sukunimi"])
    for asukas in perhe["asukkaat"]:
        if "syntymäaika" in asukas and asukas["syntymäaika"]==1981:
            print(asukas)
    if "lapset" in perhe:
        for lapsi in perhe["lapset"]:
            if "syntymäaika" in lapsi and lapsi["syntymäaika"]==1981:                   
                print(lapsi)

#exit(0)
print("Etsi samat:")

for vuosi in range (1900,2004):
    print("Vuosi:",vuosi)
    
    henkilot=[]    
    for (pn, perhe) in enumerate(perheet):
        for (n, asukas) in enumerate(perhe["asukkaat"]):
            if "syntymäaika" in asukas and asukas["syntymäaika"]==vuosi:
                henkilo=asukas #copy.copy(asukas)
                #henkilo["kirjassa"]=perhe["kirjassa"]
                henkilo["perhe"]=pn
                #henkilo["rooli"]={"tyyppi":"omistaja", "numero":n}
                henkilot.append(henkilo)
        if "lapset" in perhe:
            for (n, lapsi) in enumerate(perhe["lapset"]):
                if "syntymäaika" in lapsi and lapsi["syntymäaika"]==vuosi:
                    henkilo=lapsi #copy.copy(lapsi)
                    henkilo["sukunimi"]=perhe["sukunimi"]
                    #henkilo["kirjassa"]=perhe["kirjassa"]
                    henkilo["perhe"]=pn
                    #henkilo["rooli"]={"tyyppi":"lapsi", "numero":n}
                    henkilot.append(henkilo)

    for (id1, henkilo1), (id2, henkilo2) in itertools.combinations(enumerate(henkilot), 2):
        if(henkilo1["etunimet"][0]==henkilo2["etunimet"][0]):        
            if(len(henkilo1["etunimet"])>1 and len(henkilo2["etunimet"])>1) and henkilo1["etunimet"]!=henkilo2["etunimet"]:
                continue
            samasukunimi=False
            if "sukunimi" in henkilo1 and "sukunimi" in henkilo2 and henkilo1["sukunimi"]==henkilo2["sukunimi"]:
                samasukunimi=True
            if "osnimi" in henkilo1 and "sukunimi" in henkilo2 and henkilo1["osnimi"]==henkilo2["sukunimi"]:
                samasukunimi=True
            if "sukunimi" in henkilo1 and "osnimi" in henkilo2 and henkilo1["sukunimi"]==henkilo2["osnimi"]:
                samasukunimi=True
            if "osnimi" in henkilo1 and "osnimi" in henkilo2 and henkilo1["osnimi"]==henkilo2["osnimi"]:
                samasukunimi=True
            if(samasukunimi):
                print(henkilo1, "-", henkilo2)
                if "kaksoiskappaleet" not in henkilo1:
                    henkilo1["kaksoiskappaleet"]=[]
                henkilo1["kaksoiskappaleet"].append(henkilo2["perhe"])
                if "kaksoiskappaleet" not in henkilo2:
                    henkilo2["kaksoiskappaleet"]=[]
                henkilo2["kaksoiskappaleet"].append(henkilo1["perhe"])                
"""
i1=690
i2=692

print(perheet[i1])
print(perheet[i2])

y = json.dumps(perheet)
#print(y)
with open("kaios-app/src/data/eurajoki.json", "w") as text_file:
    text_file.write(y)