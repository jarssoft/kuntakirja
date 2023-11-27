import sys

def eprint(*args, **kwargs):
	#print(*args, file=sys.stderr, **kwargs)
	pass

def poistaTavuviivat(lause):
	return list(map(lambda a : (a+" " if (a=="" or a[-1]!='-') else a[0:-1]) , lause))

eprint(poistaTavuviivat(["Tämä","on","koe-","kutsu."]))
eprint(poistaTavuviivat(["Tämä","on","kutsu", "kokeilemista", "varten."]))
eprint(poistaTavuviivat(["Tämä","on","-"]))
eprint(poistaTavuviivat(["-"]))
eprint(poistaTavuviivat([]))

def poistaPilkut(lause):
	return list(map(lambda a : (a if (a=="" or a[-1]!=',') else a[0:-1]) , lause))

kirjaimet="ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
pienet="abcdefghijklmnopqrstuvwxyzåäö"

def ford(c):
	return  kirjaimet.index(c)  if c in kirjaimet else pienet.index(c)

def fstr(str):
	#print (str)
	#print("0:", ford(str[0]))
	#print("1:", ford(str[1]))
	return ford(str[0])*len(kirjaimet)+ford(str[1])

def ero(nimi, vnimi):
	#return abs(ord(nimi[0])-ord(vnimi[0]))*255 + abs(ord(nimi[1])-ord(vnimi[1]))
	#strord = ford(nimi[0])*len(kirjaimet)+ford(nimi[1])
	#vstrord = ford(vnimi[0])*len(kirjaimet)+ford(vnimi[1])
	return abs(fstr(vnimi)-fstr(nimi))

assert(ero("Jari", "Ilona") == abs(-29+11))
assert(ero("Saari", "Salonen") == 0)
assert(ero("Söderman", "Tahkoniemi")==1)

def etaisyydet(nimet):
	pal=[]
	for nimi in nimet:        
		erot=0        
		for vnimi in nimet:
			erot+=ero(nimi, vnimi)
		pal.append(erot)
	return pal

# Järjestää nimet aloittamalla niistä, jotka ovat toisiian lähellä aakkosissa
def yleisemmatEnsin(nimet):    
	return [x for _, x in sorted(zip(etaisyydet(nimet), nimet))]

def eprintdict(cars):
	for value in cars:
		eprint (value,':',cars[value])
		
        
