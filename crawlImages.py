#!/usr/bin/python

import requests,sys
from bs4 import BeautifulSoup

def countImage(url, page):
    
    if url.startswith('http'):
        r = requests.get(url)
        uri = r.url
        length = r.headers['content-length']
    elif url.startswith('//'):
        r = requests.get('http:'+url)
        uri = r.url
        length = r.headers['content-length']
    elif url.startswith('/'):
        r = requests.get(page + url)
        uri = r.url
        length = r.headers['content-length']
    else:
        try:
           r = requests.get(page + '/'+url)
           uri = r.url
           length = r.headers['content-length']
        except:
           print url 

    mapImg[uri] = int(length)
    print uri, length

def crawlPages(url):
    imgLinks = []
    try:
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')

        for i in soup.find_all('img'):
            if i.get('src') is not None: 
                imgLinks.append(i.get('src'))
        for i in soup.find_all('img'):
            if i.get('data-src') is not None: 
                imgLinks.append(i.get('data-src'))
    except:
        print 'Url error'
        sys.exit(0)

    return imgLinks

pages = crawlPages(sys.argv[1])
mapImg = {}

for i in pages:
   try:
      countImage(i,sys.argv[1])
   except:
      print i

print 'Total ' + str(sum(mapImg.values()) / 1024 ) + 'K' 
