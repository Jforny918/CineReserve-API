import os
import django
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / '.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinereserve.settings')
django.setup()

from movies.models import Movie, Room, Session
from django.utils import timezone
from datetime import timedelta

sala1 = Room.objects.get_or_create(name='Sala 1', rows=8, cols=10)[0]
sala2 = Room.objects.get_or_create(name='Sala 2', rows=6, cols=8)[0]

filmes = [
    {'title': 'Duna: Parte Dois', 'description': 'A jornada épica de Paul Atreides continua.', 'duration_minutes': 166, 'genre': 'Ficção Científica', 'rating': '14'},
    {'title': 'Deadpool & Wolverine', 'description': 'Dois anti-heróis se unem em uma missão improvável.', 'duration_minutes': 128, 'genre': 'Ação', 'rating': '16'},
    {'title': 'O Leão e a Bruxa', 'description': 'Uma aventura épica em terras mágicas.', 'duration_minutes': 110, 'genre': 'Fantasia', 'rating': 'L'},
]

for f in filmes:
    movie, created = Movie.objects.get_or_create(title=f['title'], defaults=f)
    if created:
        now = timezone.now()
        Session.objects.get_or_create(movie=movie, room=sala1, datetime=now + timedelta(days=1, hours=14), language='Dublado', format='2D')
        Session.objects.get_or_create(movie=movie, room=sala2, datetime=now + timedelta(days=1, hours=18), language='Legendado', format='3D')
        print(f'✅ Criado: {movie.title}')
    else:
        print(f'⏭️  Já existe: {movie.title}')

print('\n🎬 Banco populado com sucesso!')