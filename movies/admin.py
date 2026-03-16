from django.contrib import admin
from .models import Movie, Room, Session

admin.site.register(Movie)
admin.site.register(Room)
admin.site.register(Session)