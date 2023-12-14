import re

# ihminen viljelee, viljeli, kasvattaa, pitää, tuottaa, hoitaa
# tilalla/pelloilla viljellään/viljeltiin,
# päätuotantosuunta
# vuoteem xxxx saakka

def parsiTuotanto(lause, tontti="###"):
    
    pal=[]
    start=0

    paikka="(tilalla)"    
    verbi="(viljellään|viljelee|viljeltiin|viljelevät|viljelivät|viljelty|"
    verbi+="tuotetaan|tuottavat|tuotti|tuotettiin|tuottavat|tuotettu|"        
    verbi+="kasvatetaan|kasvatettiin|kasvattivat|kasvatti|kasvatettiin|kasvattavat|kasvatettu|"
    verbi+="pidetään|pidettiin|pitivät|pidetty|piti|pitää|"
    verbi+="oli|on ollut|munitettu)"
    aikamuoto="( nykyisin| aikaisemmin| edelleenkin)"
    painotus="( sivutoimisesti| pelkästään| pääasiassa| pääasiallisesti| pienellä alalla| myös| sopimustuotantona| vain| muun muassa| vielä| esimerkiksi)"
    objekti="(porkkanaa|eläimiä|vihanneksia|hevosia|muutama lehmä|lihotussikoja|lehmiä|perunaa|tärkkelysperunaa|porsaita|salaattia|ruokaperunaa|vehnää|viljaa|ohraa|rehua|rehua eläimille|leipäviljaa|kauraa|tomaattia|erikoiskasveja|rypsiä|mallasohraa|avomaankurkkuja|avomaankurkkua|siemenviljaa|kurkkua|sokerijuurikasta|heinää|vihanneksia|maitoa|lampaita|kanoja|lihakarjaa|naudanlihaa|lypsykarjaa|minkkejä|karjaa|nutriaa|mansikkaa|kesäkurpitsaa|sikoja|ruokahernettä|rehuviljaa|kananmunia|sipulia)"    
    kokoobjekti=aikamuoto+'?'+painotus+'? '+objekti
    

    while True:
        m = re.search(verbi+kokoobjekti+'(,'+kokoobjekti+')?'+'(,'+kokoobjekti+')?'+'( (ja|sekä)'+kokoobjekti+')?', lause[start:], re.I)

        if m==None:
            #print(pal)
            return pal
        
        pal.append(m.group(4))
        if m.group(8) is not None:
            pal.append(m.group(8))
        if m.group(12) is not None:
            pal.append(m.group(12))     
        if m.group(17) is not None:
            pal.append(m.group(17))                        

        start += m.end()

assert parsiTuotanto("Tilalla pidettiin lypsykarjaa ja sikoja vielä 1980-luvulla. Nykyään tilalla viljellään viljaa. Pasi on Satakunnan Keskustanuorten puheenjohtaja. Hän kuuluu myös kirkkovaltuustoon.") == ["lypsykarjaa", "sikoja", "viljaa"]
assert parsiTuotanto("Päätuotteena on sokerijuurikas, lisäksi viljellään ohraa ja kauraa.") == ["ohraa", "kauraa"]
assert parsiTuotanto("Tuovi ja Tarmo asuvat myös edelleen tilalla. Tilalla viljellään tomaattia ja kurkkua.") == ["tomaattia", "kurkkua"]
assert parsiTuotanto("Tilalla viljellään sivutoimisesti viljaa.") == ["viljaa"]
assert parsiTuotanto("Nykyisin tilalla viljellään pelkästään sokerijuurikasta.") == ["sokerijuurikasta"]
assert parsiTuotanto("Pelloilla viljellään nykyisin pääasiassa sokerijuurikasta ja heinää.") == ["sokerijuurikasta","heinää"]
assert parsiTuotanto("kesällä 2002. Nyt viljellään vihanneksia. Timo on maataloustuottajain johtokunnassa.") == ["vihanneksia"]
assert parsiTuotanto("Mäkelä on Markun kotitila. Tilalla tuotetaan maitoa. Asuinrakennus ") == ["maitoa"]
assert parsiTuotanto("Tilalla viljeltiin viljaa ja kasvatettiin kanoja vuoteen 1995.") == ["viljaa", "kanoja"]
assert parsiTuotanto("Tilalla on kasvatettu karjaa, minkkejä ja nutriaa") == ["karjaa", "minkkejä", "nutriaa"]
assert parsiTuotanto("Tilalla on kasvatettu viljaa ja mansikkaa.") == ["viljaa", "mansikkaa"]
assert parsiTuotanto("kasvatetaan viljaa ja pienellä alalla kesäkurpitsaa. ") == ["viljaa", "kesäkurpitsaa"]
assert parsiTuotanto("Tila on viljanviljelytila, vuoteen 1985 kasvatettiin myös sikoja.") == ["sikoja"]
assert parsiTuotanto("Tällä hetkellä viljellään avomaankurkkuja, mansikkaa, sokerijuurikasta viljaa. Hannu.") == ["avomaankurkkuja","mansikkaa", "sokerijuurikasta"]
assert parsiTuotanto("asuntoa. Tilalla viljellään viljaa ja tuotetaan kananmunia, vuonna 1993 ") == ["viljaa","kananmunia"]
assert parsiTuotanto("aaikan 1972. He viljelevät viljaa ja kasvattivat aikaisemmin myös sipulia. Viljan") == ["viljaa","sipulia"]
assert parsiTuotanto("tukseen. Tilalla tuotetaan perunaa, sokerijuurikasta, avomaankurkkua sekä viljaa.  ") == ["perunaa","sokerijuurikasta", "avomaankurkkua", "viljaa"]