import sys

def eprint(*args, **kwargs):
	#print(*args, file=sys.stderr, **kwargs)
	pass

def poistaTavuviivat(lause):
	return list(map(lambda a : (a+" " if (a=="" or a[-1]!='-') else a[0:-1]) , lause))

def poistaPilkut(lause):
	return list(map(lambda a : (a if (a=="" or a[-1]!=',') else a[0:-1]) , lause))