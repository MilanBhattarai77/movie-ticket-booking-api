from rest_framework import serializers
from .models import Movie, Showtime, Booking



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'duration']



class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'movie_id', 'show_time', 'available_seats']



class BookingSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer(read_only=True)
    showtime_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'showtime', 'showtime_id', 'seat_number']

        

    def validate(self, data):
        showtime_id = data.get('showtime_id')
        seat_number = data.get('seat_number')
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            available_seats = showtime.available_seats.split(',')
            if seat_number not in available_seats:
                raise serializers.ValidationError("Seat is unavailable or invalid.")
        except Showtime.DoesNotExist:
            raise serializers.ValidationError("Invalid showtime ID.")
        return data