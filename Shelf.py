import urllib
import urllib.parse
from urllib.request import Request, urlopen, URLError
import os
import requests
from lxml import html
import imdb
import re
import shelve
import sys
import itertools
if os.name=='nt':
    import win32api

VIDEO_FORMATS=('.mp4','.avi','.mkv','.flv')

access = imdb.IMDb()

shelffile1=shelve.open('MovieData')
shelffile2=shelve.open('Path')
shelffile3=shelve.open('File')

if 'Movies' not in shelffile1.keys():
    shelffile1['Movies']=list()
if 'Paths' not in shelffile2.keys():
    shelffile2['Paths']=list()
if 'Files' not in shelffile3.keys():
    shelffile3['Files']=list()

if shelffile1['Movies']:
    Movies=shelffile1['Movies']
else:
    Movies=list()

if shelffile3['Files']:
    Files=shelffile3['Files']
else:
    Files=list()

if shelffile2['Paths']:
    Paths=shelffile2['Paths']
else:
    Paths=list()

def get_imdb_id(input):
    """Function to get imdb id from input file name"""
    query = urllib.parse.quote_plus(input)
    url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="+query+"&s=all"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    if"No results" in (tree.xpath('//h1[@class="findHeader"]/text()')[0]):
        imdb_id = "tt00000"
    else:
        imdb_id=(tree.xpath('//td[@class="result_text"]//a')[0].get('href'))
        imdb_id = imdb_id.replace('/title/','')
        imdb_id = imdb_id.replace('/?ref_=fn_al_tt_1','')
    return (imdb_id)

def clean_name(fil,fromat):
    l=('xvid','Extended','Cut','pancake','HD','hd','Hd','EXTENDED','extended',"UNRATED",'Unrated','BRRIP','BRRip','DVDRip','com','BrRip','YIFY','Yify','CD','Ganool')
    fil=re.findall('(.*)'+fromat,fil)
    fil=fil[0]
    fil=fil.replace('.'," ")
    fil=fil.replace('_'," ")
    fil=re.sub('1080(.*)',"",fil)
    fil=re.sub('720(.*)',"",fil)
    fil=re.sub('480(.*)',"",fil)
    fil=re.sub('\W'," ",fil)
    fil=re.sub('(\s){2,10}'," ",fil)
    for c in l:
        fil=fil.replace(c,"")
    fil=re.sub('(\d\d\d\d)(.*)',"",fil)
    return fil.strip()

def populate(path): # automatic or not.... (prformance issue..)
    for path,dirr,files in os.walk(path):
        for fil in files:
            for form in VIDEO_FORMATS:
                if fil.endswith(form) and os.stat(os.path.join(path,fil)).st_size > 419430400:
                    filee=fil
                    fil=clean_name(fil,form)
                    if fil and fil not in Files:
                        print(fil)
                        Files.append(fil)
                        if re.findall('([0-9]+)',get_imdb_id(fil))[0]!='00000':
                            movie=access.get_movie(re.findall('([0-9]+)', get_imdb_id(fil))[0])
                            Movies.append(movie)
                            Paths.append(os.path.join(path,filee))
                            print(movie) # chewata yalew Movie Obj lay.....
                            break

    shelffile1['Movies']=Movies
    shelffile3['Files']=Files
    shelffile2['Paths']=Paths
    shelffile1.close()
    shelffile2.close()
    shelffile3.close()

if len(sys.argv) < 2:
    print ("USAGE: python Shelf.py 'Drive Path'")
    print ("NOTE: If no path is given the whole hard drive would be scanned(Take a Lot Of Time) suggested: Specify path ")
    print ("1.Exit and start again with Path specified")
    print ("2.Scan the whole hard drive")
    choice=raw_input()
    if(choice=='1'):
        sys.exit()
    elif(choice=='2'):
        if(os.name=='posix'):
            populate('/')
        elif(os.name=='nt'):
            for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                populate(drive)
else:
    path=" ".join(sys.argv[1:])
    if not os.path.exists(path):
        print ("Path Does Not Exist")
        sys.exit()
    if(os.name=='posix'):
        populate(path)
    elif(os.name=='nt'):
        populate(path)
