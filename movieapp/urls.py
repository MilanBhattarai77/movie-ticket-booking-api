from django.urls import path
from .views import MovieListView, MovieDetailView, ShowtimeListView, BookingView, CancelBookingView

# from .views import MovieListCreateView, MovieDeleteView, ShowtimeListCreateView, BookingCreateView, BookingCancelView,movie_list_create, movie_delete, showtime_list_create,booking_create, booking_cancel



urlpatterns = [

    path('movies/', MovieListView.as_view(), name='movie-list'),

    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),

    path('movies/<int:movie_id>/showtimes/', ShowtimeListView.as_view(), name='showtime-list'),

    path('bookings/', BookingView.as_view(), name='booking-create'),

    path('bookings/<int:booking_id>/', CancelBookingView.as_view(), name='booking-cancel'),

]





# This is for both Class-Based Views URLs and Function-Based Views URLs


# urlpatterns = [
#     path('movies/', movie_list_create, name='movie-list'),
#     path('movies/<int:pk>/', movie_delete, name='movie-detail'),
#     path('movies/<int:movie_id>/showtimes/', showtime_list_create, name='showtime-list'),
#     path('bookings/', booking_create, name='booking-create'),
#     path('bookings/<int:booking_id>/', booking_cancel, name='booking-cancel'),
# ]