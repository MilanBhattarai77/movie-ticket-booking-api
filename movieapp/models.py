from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    duration = models.IntegerField()

    def __str__(self):
        return self.title
    


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    show_time = models.DateTimeField()
    available_seats = models.TextField()  
    def __str__(self):
        return f"{self.movie.title} at {self.show_time}"
    
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.CharField(max_length=3)

    def __str__(self):
        return f"Booking {self.id} for {self.showtime} - Seat {self.seat_number}"
