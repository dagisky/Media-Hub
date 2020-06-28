from django.core.management.base import BaseCommand, CommandError
from Movies.models import Movie

from django.core.files.base import ContentFile
import shelve
import urllib
import os


class Command(BaseCommand):

    def handle(self,*arg,**options):
        print('populate stuff.......')
        SFile=shelve.open('MovieData')
        Shelf=shelve.open('Path')
        for (movie,path) in zip(SFile['Movies'],Shelf['Paths']):
            mov=Movie()
            if not Movie.objects.filter(Name=movie['title']).exists():                
                try:
                    mov.Name=movie['title']
                except:
                    mov.Name="Not Available"
                try:
                    mov.Year=movie['year']
                except:
                    mov.Year="Not Available"
                try:
                    mov.Plot=''.join(movie['plot'])
                    mov.Plot_outline=''.join(movie['plot outline'])
                except:
                    mov.Plot="Not Available"
                    mov.Plot_outline="Not Available"
                try:
                    mov.Genre=' '.join(movie['genres'])
                except:
                    mov.Genre="Not Available"
                try:
                    mov.Imdb_rating=movie['rating']
                except:
                    mov.Imbd_rating=1.0
                d=''
                try:
                    for name in movie['director']:
                        d+=','+str(name)
                        mov.Director=d.strip(',')
                except:
                    mov.Director="Not Available"
                try:  
                    base_dir = 'media/'                 
                    url=movie['full-size cover url']
                    if not os.path.exists(base_dir):
                        os.mkdir(base_dir)
                    with urllib.request.urlopen(url) as resource:        
                        print('-------- poster saving -----')      
                        output = open(base_dir+movie['title']+'.jpg',"wb+")
                        output.write(resource.read())
                        output.close()
                        mov.Poster = movie['title']+'.jpg'
                except:
                    mov.Poster=None

                if mov.Name =="Not Available" or 'TV' in mov.Genre or 'Show' in mov.Genre:
                    SFile['Movies'].remove(movie)
                else:
                    mov.Path=path
                    mov.save()
                    self.stdout.write(mov.Name)
            self.stdout.write(movie['title'])


        Shelf.close()
        SFile.close()
