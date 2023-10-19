import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	#pass

def poistaTavuviivat(lause):
	return list(map(lambda a : (a+" " if (a=="" or a[-1]!='-') else a[0:-1]) , lause))

eprint(poistaTavuviivat(["Tämä","on","koe-","kutsu."]))
eprint(poistaTavuviivat(["Tämä","on","kutsu", "kokeilemista", "varten."]))
eprint(poistaTavuviivat(["Tämä","on","-"]))
eprint(poistaTavuviivat(["-"]))
eprint(poistaTavuviivat([]))

def poistaPilkut(lause):
	return list(map(lambda a : (a if (a=="" or a[-1]!=',') else a[0:-1]) , lause))

def ero(nimi, vnimi):
	return abs(ord(nimi[0])-ord(vnimi[0]))*255 + abs(ord(nimi[1])-ord(vnimi[1]))

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

def eprintdict(cars):
	for value in cars:
		eprint (value,':',cars[value])