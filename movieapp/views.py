from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Movie, Showtime, Booking
from .serializers import MovieSerializer, ShowtimeSerializer, BookingSerializer


# Create your views here.




class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class MovieDetailView(APIView):
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        
        


class ShowtimeListView(APIView):
    def get(self, request, movie_id):
        showtimes = Showtime.objects.filter(movie_id=movie_id)
        serializer = ShowtimeSerializer(showtimes, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        if not request.user.is_staff:
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
        try:
            Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['movie_id'] = movie_id
        data['available_seats'] = ','.join([f"{row}{col}" for row in range(1, 6) for col in range(1, 6)])  # 5x5 grid
        serializer = ShowtimeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            showtime = Showtime.objects.get(id=data['showtime_id'])
            available_seats = showtime.available_seats.split(',')
            seat_number = data['seat_number']
            if seat_number in available_seats:
                available_seats.remove(seat_number)
                showtime.available_seats = ','.join(available_seats)
                showtime.save()
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Seat is unavailable"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            showtime = booking.showtime
            available_seats = showtime.available_seats.split(',')
            available_seats.append(booking.seat_number)
            showtime.available_seats = ','.join(sorted(available_seats))
            showtime.save()
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
        









# This is Class-Based Views (GenericAPIView with Mixins)




# class MovieListCreateView(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
#         return super().create(request, *args, **kwargs)
    


# class MovieDeleteView(generics.DestroyAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     permission_classes = [IsAdminUser]

#     def destroy(self, request, *args, **kwargs):
#         try:
#             movie = self.get_object()
#             movie.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        


# class ShowtimeListCreateView(generics.ListCreateAPIView):
#     serializer_class = ShowtimeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         movie_id = self.kwargs.get('movie_id')
#         return Showtime.objects.filter(movie_id=movie_id)

#     def create(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
#         movie_id = self.kwargs.get('movie_id')
#         try:
#             Movie.objects.get(pk=movie_id)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         data = request.data.copy()
#         data['movie_id'] = movie_id
#         data['available_seats'] = ','.join([f"{row}{chr(64+col)}" for row in range(1, 6) for col in range(1, 6)])  # 5x5 grid (1A-5E)
#         serializer = ShowtimeSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class BookingCreateView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data['user_id'] = request.user.id
#         serializer = BookingSerializer(data=data)
#         if serializer.is_valid():
#             try:
#                 showtime = Showtime.objects.get(id=data['showtime_id'])
#                 available_seats = showtime.available_seats.split(',')
#                 seat_number = data['seat_number']
#                 if seat_number in available_seats:
#                     available_seats.remove(seat_number)
#                     showtime.available_seats = ','.join(available_seats)
#                     showtime.save()
#                     serializer.save(user=request.user)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response({"error": "Seat is unavailable"}, status=status.HTTP_400_BAD_REQUEST)
#             except Showtime.DoesNotExist:
#                 return Response({"error": "Showtime not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class BookingCancelView(generics.DestroyAPIView):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def destroy(self, request, *args, **kwargs):
#         try:
#             booking = Booking.objects.get(id=self.kwargs['pk'], user=request.user)
#             showtime = booking.showtime
#             available_seats = showtime.available_seats.split(',')
#             available_seats.append(booking.seat_number)
#             showtime.available_seats = ','.join(sorted(available_seats))
#             showtime.save()
#             booking.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Booking.DoesNotExist:
#             return Response({"error": "Booking not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
        






# # This is Function-Based Views 



# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def movie_list_create(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         if not request.user.is_staff:
#             return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def movie_delete(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except Movie.DoesNotExist:
#         return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    




# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def showtime_list_create(request, movie_id):
#     if request.method == 'GET':
#         showtimes = Showtime.objects.filter(movie_id=movie_id)
#         serializer = ShowtimeSerializer(showtimes, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         if not request.user.is_staff:
#             return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
#         try:
#             Movie.objects.get(pk=movie_id)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         data = request.data.copy()
#         data['movie_id'] = movie_id
#         data['available_seats'] = ','.join([f"{row}{chr(64+col)}" for row in range(1, 6) for col in range(1, 6)])  # 5x5 grid (1A-5E)
#         serializer = ShowtimeSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def booking_create(request):
#     data = request.data.copy()
#     data['user_id'] = request.user.id
#     serializer = BookingSerializer(data=data)
#     if serializer.is_valid():
#         try:
#             showtime = Showtime.objects.get(id=data['showtime_id'])
#             available_seats = showtime.available_seats.split(',')
#             seat_number = data['seat_number']
#             if seat_number in available_seats:
#                 available_seats.remove(seat_number)
#                 showtime.available_seats = ','.join(available_seats)
#                 showtime.save()
#                 serializer.save(user=request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response({"error": "Seat is unavailable"}, status=status.HTTP_400_BAD_REQUEST)
#         except Showtime.DoesNotExist:
#             return Response({"error": "Showtime not found"}, status=status.HTTP_404_NOT_FOUND)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def booking_cancel(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=booking_id, user=request.user)
#         showtime = booking.showtime
#         available_seats = showtime.available_seats.split(',')
#         available_seats.append(booking.seat_number)
#         showtime.available_seats = ','.join(sorted(available_seats))
#         showtime.save()
#         booking.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
