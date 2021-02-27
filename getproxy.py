import requests, urllib, re,time, random
from bs4 import BeautifulSoup
from base64 import b64decode as ops

# url='https://proxyscrape.com/free-proxy-list'

def getproxies(tipo='http',nazione='IT'):
    url='https://api.proxyscrape.com/?request=getproxies&proxytype={tipo}&timeout=10000&ssl=yes&country={nazione}&anonymity=anonymous'.format(tipo=tipo,nazione=nazione) #&country=US&anonymity=elite
    req=''
    while req=='':
        req=requests.get(url).text
        res=req.splitlines()
    return res

def getproxy(tipo='http',nazione='IT'):
    return random.choice(getproxies(tipo,nazione))

def getproxys2():###prova anche con socks4, vai sul sito e prendi
    url='https://www.sslproxies.org/'
    s=requests.Session()
    soup=BeautifulSoup(s.get(url).text,'html.parser')
    soup=soup.find('tbody')
    soup=soup.find_all('tr')
    anons=list(str(i) for i in soup if 'anonymous' in str(i))
    soup=BeautifulSoup(anons[0],'html.parser')
    res=soup.find_all('td')
    res[0]=res[0].get_text()
    res[1]=res[1].get_text()
    return res[0]+':'+res[1]

# getproxys2()
print("Proxy loaded.")