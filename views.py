from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, Watchlist, WatchlistMovie
import requests
import json

# Search movies from OMDB
def search_movies(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No search query'}, status=400)
    
    response = requests.get('http://www.omdbapi.com/', params={
        'apikey': settings.OMDB_API_KEY,
        's': query
    })
    data = response.json()
    movies = data.get('Search', [])
    return JsonResponse({'results': movies})

# Get all watchlists
def get_watchlists(request):
    watchlists = Watchlist.objects.all().values('id', 'name', 'created_at')
    return JsonResponse({'watchlists': list(watchlists)})

# Create a watchlist
@csrf_exempt
def create_watchlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wl = Watchlist.objects.create(name=data['name'])
        return JsonResponse({'id': wl.id, 'name': wl.name})

# Watchlist detail, update name, delete watchlist
@csrf_exempt
def watchlist_detail(request, watchlist_id):
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id)
    except Watchlist.DoesNotExist:
        return JsonResponse({'error': 'Watchlist not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': watchlist.id, 'name': watchlist.name})
    elif request.method in ('PUT', 'PATCH'):
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            watchlist.name = name
            watchlist.save()
        return JsonResponse({'id': watchlist.id, 'name': watchlist.name})
    elif request.method == 'DELETE':
        watchlist.delete()
        return JsonResponse({'message': 'Watchlist deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Add movie to watchlist
@csrf_exempt
def add_movie(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Save movie to DB if it doesn't exist
        movie, _ = Movie.objects.get_or_create(
            imdb_id=data['imdb_id'],
            defaults={
                'title': data['title'],
                'year': data.get('year', ''),
                'poster_url': data.get('poster_url', ''),
            }
        )
        
        watchlist = Watchlist.objects.get(id=data['watchlist_id'])
        entry = WatchlistMovie.objects.create(
            watchlist=watchlist,
            movie=movie,
            status='planned'
        )
        return JsonResponse({'message': 'Movie added!', 'entry_id': entry.id})

# Get movies in a watchlist
def get_watchlist_movies(request, watchlist_id):
    entries = WatchlistMovie.objects.filter(
        watchlist_id=watchlist_id
    ).select_related('movie')
    
    movies = [{
        'title': e.movie.title,
        'imdb_id': e.movie.imdb_id,
        'poster': e.movie.poster_url,
        'status': e.status,
        'rating': e.rating,
    } for e in entries]
    
    return JsonResponse({'movies': movies})

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Register a new user
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return JsonResponse({'message': 'Account created!', 'user_id': user.id})

# Login
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful!', 'user_id': user.id, 'username': user.username})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)