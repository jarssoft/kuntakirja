import re

def parsi(lause, tontti="###"):
    
    vuonna="((kesällä |talvella |keväällä |syksyllä |[a-z]+kuussa |vuonna )?([0-9]{4}))"    
    talo='('+tontti+'n )?('+tontti+'|paritalo|asunto|tontti|rantatontti|kesämökki|mökki|talo|omakotitalo|kesäpaikka|paikka|tila|osake|rivitalo-osake|kiinteistö)'
    talon='('+tontti+'n )?('+tontti+'|paritalo|asunno|tonti|rantatonti|kesämöki|möki|talo|omakotitalo|kiinteistö|kesäpaika|paika|tila|osakkee|rivitalo-osakkee|rakennukse)n'

    #print(lause)

    m = re.search('(ostivat|osti|hankki|hankkivat) '+talon+'(sa)? ([A-ZÅÄÖ][ A-ZÅÄÖa-zåäö]+lt[aä] )*(itselleen |omistukseensa )?'+vuonna, lause)
    if m!=None:
        #print("1")
        return int(m.group(9))

    m = re.search(talon+'(sa)? (hän|he) (ostivat|osti|hankki|hankkivat) ([A-ZÅÄÖ][ A-ZÅÄÖa-zåäö]+lt[aä] )*(itselleen |omistukseensa )?'+vuonna, lause, re.I)
    if m!=None:
        return int(m.group(10))


    m = re.search(vuonna+' '+talo+' siirtyi ([A-ZÅÄÖ][A-ZÅÄÖ a-zåäö]+n) omistukseen', lause)        
    if m!=None:
        return int(m.group(3))
    
    m = re.search('omistukseen '+talo+' siirtyi '+vuonna, lause)        
    if m!=None:
        return int(m.group(5))
    
    m = re.search(talo+' siirtyi '+vuonna+' ([A-ZÅÄÖ][A-ZÅÄÖ a-zåäö]+n) omistukseen', lause, re.I )        
    if m!=None:
        return int(m.group(5))
    
    m = re.search(talo+' siirtyi ([A-ZÅÄÖ][A-ZÅÄÖ a-zåäö]+n) omistukseen '+vuonna, lause, re.I )        
    if m!=None:
        return int(m.group(6))
    
    return None

#assert parsi("Veikko ja Olga ostivat tyttärensä perheen kanssa paritalon Riikon asuinalueelta 1988.") == 1988


assert parsi("ostivat talon 1974") == 1974
assert parsi("Reijo muutti taloon 1981 ja osti tilan itselleen 1990.") == 1990
assert parsi("Orvokki ja Harry-Pekka ostivat talon 1997 loma-asunnokseen.") == 1997
assert parsi("Walleniukset ostivat osakkeen 1981.") == 1981
assert parsi("Kimmo osti osakkeen vuonna 1999.") == 1999
assert parsi("Henry ja Tiina ostivat paikan helmikuussa 1993.") == 1993
assert parsi("He ostivat talon Niemisiltä vuonna 2000.") == 2000
assert parsi("Heidi ja Marko ostivat talon Heidin äidiltä vuonna 2001.") == 2001
assert parsi("Pentti ja Terttu ostivat rantatontin 1978") == 1978
assert parsi("Pia osti talon Kuivalahdelta 1990 maaseudulta") == 1990
assert parsi("Juha ja Jaana ostivat tontin 1996 ja ") == 1996
assert parsi("Timo osti Polttilan paikan 1995.", "Polttila") == 1995
assert parsi("Teemu ja Riikka-Liisa ostivat talonsa 1999.") == 1999
assert parsi("Veli-Matti ja Sirpa ostivat talon Liipolan perikunnalta kesällä 1999.") == 1999
assert parsi("Parjaset ostivat rivitalo-osakkeen Lapijoelta 1975.") == 1975
assert parsi("Aromaat ostivat rakennuksen 1976 Gustavsonin perikunnalta.") == 1976

assert parsi("Airin täti Salli Knuutila ja hänen miehensä Aali hankkivat talon 1932.") == 1932
assert parsi("Nordblomit hankkivat tontin 1967.") == 1967
assert parsi("Gunnarit hankkivat mökin omistukseensa 1970-80-luvun taitteessa.")==1970
assert parsi("Jaakko ja Eila hankkivat talon omistukseensa 1991.")==1991

assert parsi("Vuonna 1976 talo siirtyi Antin ja Airin omistukseen.") == 1976
assert parsi("1982 tila siirtyi Pertin ja Airan omistukseen") == 1982
assert parsi("Vuonna 1993 talo siirtyi Mikon omistukseen.") == 1993
assert parsi("Toivon ja Katrin omistukseen tila siirtyi 1962.") == 1962
assert parsi("Tila siirtyi Laurin vanhempien Esa ja Leena Linnalan omistukseen 1995.") == 1995
assert parsi("1990 Rantanotko siirtyi Jarmon omistukseen.", "Rantanotko") == 1990
assert parsi("Tila siirtyi 1998 Junniloiden omistukseen") == 1998
assert parsi("hänen omistukseen tila siirtyi 1995.") == 1995

#assert parsi("Urpo ja Toini ostivat oman talon Koivusen perikunnalta Kuivalahdelta 1983.") == 1983

assert parsi("Paikalla sijaitsi 1900-luvun alussa mökki, jonka Kivi-niminen mies laajensi nykymuotoonsa 1930-40-luvuilla. Tuomet ostivat talon 1967 Eino ja Helmi Nummelta. He myivät talon 1974 Sakari Leirimaalle. Talo siirtyi uudelleen Tuomien omistukseen 1990. Sen jälkeen talossa on ollut vuokralaisia, mutta nykyään talo on lähinnä omassa käytössä.") == 1967
assert parsi("Kesäasunnon omistavat veljekset Hemmo, Sakari ja Mika Laine. Sen ovat rakentaneet heidän vanhempansa Matti ja Irja Laine. Poikien omistukseen paikka siirtyi vuonna 2000.")==2000
assert parsi("Aimo ja Seija etsivät kesämökkiä monta vuotta ja tämä löytyi Kuivalahdelta Aimon synnyinkunnasta. He ostivat mökin Terhosen perikunnalta 1988. Tontille rakennettiin uusi mökki 1990. ")==1988

assert parsi("Eija muutti Satakuntaan 1976. Talon hän osti kesällä 1999 ja on sen jälkeen kunnostanut sitä pikku hiljaa. ")==1999
assert parsi("Asser ja Sinikka ostivat kesämökin 1976. 421 ") == 1976


assert parsi("Paikka siirtyi Toivon omistukseen 1997.") == 1997
assert parsi("Paikka siirtyi Toiv.on omistukseen 1997.") == None
