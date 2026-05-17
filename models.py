from django.db import models

class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=100, blank=True)
    poster_url = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WatchlistMovie(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('watching', 'Watching'),
        ('completed', 'Completed'),
    ]
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    rating = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)