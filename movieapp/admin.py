from django.contrib import admin
from .models import Movie, Showtime, Booking


# Register your models here.


admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(Booking)