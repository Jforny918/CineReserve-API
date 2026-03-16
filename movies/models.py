from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)  # Ex: "L", "10", "14", "18"
    poster_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=50)  # Ex: "Sala 1"
    rows = models.PositiveIntegerField()     # Ex: 8 fileiras
    cols = models.PositiveIntegerField()     # Ex: 10 colunas = 80 assentos

    def __str__(self):
        return self.name


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='sessions')
    datetime = models.DateTimeField()
    language = models.CharField(max_length=20, default='Dublado')  # Dublado / Legendado
    format = models.CharField(max_length=10, default='2D')         # 2D / 3D / IMAX

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return f"{self.movie.title} - {self.datetime}"