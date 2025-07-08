
# Movie Ticket Booking System API

A RESTful API built with Django and Django REST Framework (DRF) for a Movie Ticket Booking System. Users can browse movies, view showtimes, book seats, and cancel bookings. Admins can add/remove movies and manage showtimes. The API uses JSON Web Token (JWT) authentication for secure access.



## Setup and Installation

1. **Prerequisites**:
   - Python 3.8 or higher (tested with 3.12; 3.13 may work but is not officially supported by Django 4.2.11).
   - Git.
   - Virtual environment (recommended).



2. **Clone the Repository**:
   ```bash
   git clone https://github.com/MilanBhattarai77/movie-ticket-booking-api.git
   cd MovieTicketBookingSystem


3. **Set Up Virtual Environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  


4. **Install Dependencies**:
   Ensure `requirements.txt` exists in the project root with:



5. **Set Up Environment Variables**:
   Create a `.env` file in the project root (as of 10:23 PM +0545, July 08, 2025):
   ```bash
   echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
   echo "DEBUG=True" >> .env




6. **Apply Database Migrations**:
   ```bash
   python manage.py migrate



7. **Create a Superuser (for Admin Access)**:
   ```bash
   python manage.py createsuperuser



Steps to Run the Application


1. Activate the virtual environment:

source myenv/bin/activate


2. Start the Django development server:

python manage.py runserver


3. Access the API at http://127.0.0.1:8000/api/.


4. Obtain a JWT token:

Send a POST request to http://127.0.0.1:8000/api/token/ with:

{"username": "your_username", "password": "your_password"}

Use the returned access token in the Authorization header (Bearer <token>).


5. Test endpoints using Postman, curl, or a frontend:

List movies: GET /api/movies/

Add a movie (admin): POST /api/movies/ with {"title": "Inception", "genre": "Sci-Fi", "duration": 148}

Book a seat: POST /api/bookings/ with {"showtime_id": 1, "seat_number": "1A"}