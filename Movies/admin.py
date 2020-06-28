from django.contrib import admin
from .models import Movie
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Year', 'Genre','Director','Imdb_rating']
	list_editable = ['Genre']
	search_fields=['Name','Genre']
	list_filter = ['Imdb_rating']

admin.site.register(Movie, MovieAdmin)
