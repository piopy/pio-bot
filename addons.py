import datetime, re, random, os, urllib.request, time, json, requests, scraper, framescrap
from google_trans_new import google_translator
from urllib.request import urlopen
from bs4 import BeautifulSoup
import zlibscrap, taybook, dieti

from base64 import b64decode as ops
#######################################
#           /bus command              #
#######################################

def query_hellobus(fermata, linea=0):
    SATELLITE_EMOJI = "\U0001F4E1"
    CLOCK_EMOJI = "\U0001F550"
    
    time_now = datetime.datetime.now().strftime('%H%M')
    
    if linea != 0:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + linea + "&oraHHMM=" #+ str(time_now)
    else:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + "&oraHHMM=" #+ str(time_now)

    root = urlopen(url).read()
    result = re.findall('.asmx">([^<]*)', str(root))
    print(result)
    return_value = ""
    for res in result:
        result = res.replace(", ", "_").strip()
        result1, result2 = result.split("_")
        if "Previsto" in result1:
            return_value += CLOCK_EMOJI + "" + result1.replace("TperHellobus:" , "").replace("Previsto", "da orario") + "\n"
        else:
            return_value += SATELLITE_EMOJI + "" + result1.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"

        if "Previsto" in result2:
            return_value += CLOCK_EMOJI + " " + result2.replace("TperHellobus:" , "").replace("Previsto", "da orario") + "\n"
        else:
            return_value += SATELLITE_EMOJI + " " + result2.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"
    return str(return_value)

#######################################
#              dieta                  #
#######################################
def dieta_p():
    print("Genero una dieta...")
    dieta=''
    uovo=False
    legumi=False
    r=random.randint(0,9)
    if r%2==0:uovo=True
    with open('diet.txt','r',encoding='utf-8') as f:
        dieta=f.read()
    dieti.update(uovo)
    pasti=dieta.split('#')
    final=''+'Kcal: 1250 circa\nUova a colazione: '+str(uovo)+'\n'
    if uovo:pasti.pop(1)
    else: pasti.pop(0)
    for p in pasti:
        p=p.split(':')
        nome=p[0]
        componenti=p[1]
        scelta=dieti.scegli(nome,componenti)
        final+=scelta+'\n'
    return  final

#######################################
#          /book command              #
#######################################

def get_all_authors():
    return taybook.get_all_authors()

def search_author(user_input):
    return taybook.search_author(user_input)

def retrive_books(authors, bformat="pdf"):
    return taybook.retrive_books(authors, bformat)

def wrapper_retrive_books(authors):
    return retrive_books(authors)

def try_author(authors):
    return taybook.testpage(authors)

def clean_book_cache(file_list):
    for f in file_list:
        os.remove(f)

def zsearch(usersays):
    if '/international' in usersays: return zlibscrap.scraperz(usersays, True)
    return zlibscrap.scraperz(usersays,False)

###########################trad ##############
def traduttore_albano_romina(text):
    src='it'
    tgt='sq'
    ALB_EMOJI = "\U0001F1E6\U0001F1F1"
    IT_EMOJI = "\U0001F1EE\U0001F1F9"
    t=google_translator()
    res1=IT_EMOJI+': '+t.translate(text,lang_tgt=src,lang_src=tgt)
    res2=ALB_EMOJI+': '+t.translate(text,lang_src=src,lang_tgt=tgt)
    return res1,res2
############################ b64 #############

def encodecode(stringa):
    dec=ops(stringa).decode("utf-8")
    enc=ops(stringa).encode()
    return 'E: '+enc+'\n\nD: '+dec

############################calcio ###########
def updategmt(url):
    regex=r'\d\d:\d\d'
    orario="".join(re.findall(regex,url)) ## es 20:00
    ora=orario.split(':')
    
    if(ora[0]=='23'): ora[0]='00'
    else: ora[0]=str(int(""+ora[0])+1)
    if len(ora[0])==1: ora[0]='0'+ora[0]
    orarionuovo=""+ora[0]+':'+ora[1]
    res=url.replace(orario,orarionuovo)
    return res

def calcio():
    
    url2=ops('aHR0cDovLzE3Mi42Ny4xODguMTc1L3Byb2cudHh0').decode("utf-8")
    headers={
                                    'Host': ops('c3BvcnR6b25saW5lLnRv').decode("utf-8"),
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
                                }
    html=requests.get(url2,headers=headers).text
    html=html.splitlines()
    links=[]
    lan=[]
    for line in html:
        if 'HD' in line or 'BR' in line:
            lan+=[line]
        if 'http' in line:
            if not '24/7 CHANNELS' in line: line=updategmt(line)
            links+=[line]
    return links, lan

def calcio2():
    ##return a list of links
    url2=ops('aHR0cDovLzE3Mi42Ny4yMDkuMjM1Lw==').decode("utf-8")
    links=[]
    headers={
                                    'Host': ops('ZGFkZHlsaXZlLmNsdWI=').decode("utf-8"),
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
                                }
    req=requests.get(url2,headers=headers).text
    soup = BeautifulSoup(req, 'html.parser') ##div class="col-lg-3 col-md-4 col-xs-4 mb-30"
    for i in soup.findAll("article", class_="col-xs-12"):
        ##links
        link=str((i.findAll('p'))[0]) ##only soccer
        regex=r'>(.*?)\<\/span\>'
        link=re.findall(regex,link)
        for i in link: 
            i=i.replace('<br/>','')
            i=re.findall('^(.*?)>',i)
            i=str(i)
            i=i.replace('<a href=',': ').replace('"','').replace('[\'','').replace('\']','')
            i=i.replace('/stream/','/embed/')
            links.append(i)
    
    return links

####################################
#############taste##################
def taste(something):
    tipi=['music', 'movies', 'shows', 'podcasts', 'books', 'authors', 'games']
    intro='Hai cercato: '+something.capitalize()+'.\n Ecco la lista di cose che potrebbero piacerti:\n'
    res=''
    for i in tipi:
        print("Processing "+i)
        temp=taste_core(something,i)
        print(temp) 
        if "Rate limit exceeded, try again later" in temp: return "Rate limit exceeded, try again later"
        if not temp == '' and not temp == '\n':
            res+=temp+'\n'
    if res == '': res="Non ho trovato nulla! Sicuro di aver scritto tutto giusto?"
    else: res=intro+res
    return res

def taste_core(something, tipo):
    url="https://tastedive.com/api/similar?q="+something.replace(' ','+')+"&type="+tipo
    req=requests.get(url).text
    regex=r'(?<=\{)(.*?)(?=\})'
    regex_2=r'(?<=\"Name": ")(.*?)(?=\")'
    list=re.findall(regex,req)
    if "Rate limit exceeded, try again later" in list[0]:
        return "Rate limit exceeded, try again later"
    list[0]=list[0].replace('"Similar": {"Info": [{','')
    #tipocercato=re.findall(r'(?<=\"Type": ")(.*?)(?="$)',list[0])
    testo=''
    for i in list:
        testo+='\n'+i
    list=re.findall(regex_2,testo)

    testo='\t    '+tipo.upper()+'\n'
    nome=list[0]
    for i in list:
        if not nome==i: testo+=i+'\n'
    if testo == '\t    '+tipo.upper()+'\n': return ''
    else: return testo

########## pioflix ############
def pioflix(termsrc):
    listurls=scraper.preparaurl(termsrc)
    l,i,t=scraper.globalsearch(listurls)
    new_l=[]
    for link in l:
        test=framescrap.sframestring(link)
        if len(link)>0: new_l.append(test)
    
    return scraper.globallist(t,new_l)
    #return scraper.globallist(t,l)


