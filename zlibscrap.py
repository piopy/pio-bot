import requests,time,random
from bs4 import BeautifulSoup

from base64 import b64decode as ops

dec=ops('aHR0cHM6Ly9pdC4xbGliLmV1').decode("utf-8")

def scrapedeep(url):
    req=requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')
    i=soup.find('a', class_="btn btn-primary dlButton addDownloadedBook")
    i=dec+i.get('href')
    return i

def scrapeResults(url):
    #prende l'url e vede i vari risultati, li apre e prende i collegamenti diretti
    #div id searchResultBox
    req=requests.get(url).text
    results=[]
    soup = BeautifulSoup(req, 'html.parser')
    for i in soup.find_all("div", class_="resItemBox resItemBoxBooks exactMatch"):
        r=random.randint(1,13)/10
        time.sleep(r)
        try:
            it=i.find('h3')
            it=it.find('a')
            link=dec+it.get('href')
            nome=it.get_text()
            aut=''
            author=i.find('div',class_='authors')
            author=author.find_all('a')
            for a in author:
                a=a.get_text()
                aut+=a+'_'
            link=scrapedeep(link)
            stringa=nome+' ('+aut+')'+' - '+link
            results.append(stringa)
            print(len(results))
        except: results+=['Troppe richieste dal tuo IP. Riprova più tardi.']
    return results

def scraperz(author, international=False):
    if international == True: url=dec+'/s/'+author+'/?e=1&language=italian'
    else: url=dec+'/s/'+author+'/?e=1'
    results=scrapeResults(url)
    for i in results: print(i)
    return results
    
    

if __name__ == '__main__':
    scraperz(input("Inserisci un libro o un autore: "))
    #except: print("qualcosa è andato terribilmente storto")