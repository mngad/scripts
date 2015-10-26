#!python3
#fraun

import requests, os, bs4, random, hashlib
import os
import sys, getopt
from os import listdir
from os.path import isfile, join

def getDir():
    biblioDir = input('Input the biblio.bib dir: ')
    os.chdir(biblioDir)

def genHeader():
    rand_str = str(random.random()).encode('utf8')
    google_id = hashlib.md5(rand_str).hexdigest()[:16]
    header = {'User-Agent': 'Mozilla/5.0','Cookie': 'GSP=ID=%s:CF=4' % google_id}
    return header



def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hmo:")
    except getopt.GetoptError:
        print('getBib.py -m -o')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('getBib.py -m -o\n -m: Multiple Searches \n -o Change dir of biblio.bib')
            sys.exit()
        if opt == '-m':
            multbibs =True
        if opt == '-o':
            os.chdir(arg)
            
    while multbibs:
        bibFile = open('biblio.bib', 'a')
        # fake google id (looks like it is a 16 elements hex)
        header=genHeader()
        scholUrl = 'https://scholar.google.co.uk/scholar?hl=en&q='
        paperToSearch = input('Enter the paper to seach for: ')
        if paperToSearch == 'q':break
        url = scholUrl + paperToSearch
        res = requests.get(url, headers=header)
        res.raise_for_status
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        numBibs = 0
        for a in soup.find_all('a', href=True):
            if ".bib" in a['href']:
                numBibs = numBibs +1
        if numBibs == 1:
            for a in soup.find_all('a', href=True):
                if ".bib" in a['href']:
                    bibURL = 'https://scholar.google.co.uk' + a['href']
                    print(bibURL)
                    resbib = requests.get(bibURL, headers=header)
                    soupbib = bs4.BeautifulSoup(resbib.text, "html.parser")
                    [s.extract() for s in soupbib(['style', 'script', '[document]', 'head', 'title'])]
                    visible_text = soupbib.getText()
                    print(visible_text)
                    bibFile.write(visible_text)
        else:
            print('More than one paper...')
        bibFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])
