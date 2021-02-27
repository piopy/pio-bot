#### deprecated

import re, os, urllib.request, time, urllib.error
from urllib.request import urlopen
from base64 import b64decode as ops

def get_all_authors():
    with open('./authors.txt', 'r') as authors_file: 
        return authors_file.readlines() 

def search_author(user_input):
    authors = get_all_authors()
    user_input = user_input.replace(" ", "-").lower()
    match = []
    for author in authors:
        if user_input in author: 
            match.append(author)
            break
    if match: return match
    else: return False

def testpage(author):
    author=author.replace(' ','-').lower()
    base_url = "aHR0cHM6Ly9kd25sZy50ZWwvYm9vay1uLw=="
    author = author.rstrip()
    try:
        new_url = ops(base_url).decode("utf-8") + author + "/"
        a=urllib.request.urlopen(new_url)
        a.getcode()
        return True
    except urllib.error.HTTPError as e:
        return False


def retrive_books(authors, bformat="pdf"):
    reg_ex_interno = r'a href="\/book-n[^>]+>([^<]+)'
    if bformat == "mobi": reg_ex_books = r'>([^\.]+\.mobi)<\/a>'
    elif bformat == "pdf": reg_ex_books = r'>([^\.]+\.pdf)<\/a>'
    else: reg_ex_books = r'>([^\.]+\.epub)<\/a>'
    base_url = "aHR0cHM6Ly9kd25sZy50ZWwvYm9vay1uLw==" #b64 to evoid being triggered by target searches
    downloaded_titles = []
    for author in authors: 
        if 1:
            author = author.rstrip()
            new_url = ops(base_url).decode("utf-8") + author + "/"
            print("\nWorking on " + author)
            req = urllib.request.Request(new_url)
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            
            books = re.findall(reg_ex_interno, str(respData))
            responso=[]
            for book in books:
                if "Directory" not in book:
                    print("Processing book " + book)
                    url_download_book = new_url + book + "/"
                    req = urllib.request.Request(url_download_book)
                    resp = urllib.request.urlopen(req)
                    respData = resp.read()
                    titles = re.findall(reg_ex_books, str(respData))
                    for title in titles:
                        download_url = url_download_book + title
                        filename = author.replace("-", " ") + " - " + title.replace("-", " ")
                        if 1:
                            filename = author.replace("-", " ") + " - " + title.replace("-", " ").replace(".pdf",'')
                            #strin="Download "+filename+": "+url_download_book
                            strin="Download "+filename+": \n"+download_url+"\n\n"+download_url.replace(".pdf",".epub")+"\n\n"+download_url.replace(".pdf",".mobi")
                            responso.append(strin)
                        else:
                            print("Something bad happened :/")
    return responso