from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Movie, Room, Session


class MovieTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Duna: Parte Dois',
            description='A jornada épica de Paul Atreides continua.',
            duration_minutes=166,
            genre='Ficção Científica',
            rating='14'
        )
        self.room = Room.objects.create(name='Sala 1', rows=8, cols=10)
        self.session = Session.objects.create(
            movie=self.movie,
            room=self.room,
            datetime=timezone.now() + timedelta(days=1),
            language='Dublado',
            format='2D'
        )

    def test_list_movies(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_movie_detail(self):
        response = self.client.get(reverse('movie-detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Duna: Parte Dois')

    def test_movie_not_found(self):
        response = self.client.get(reverse('movie-detail', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_movies(self):
        Movie.objects.create(
            title='Deadpool & Wolverine',
            description='Dois anti-heróis.',
            duration_minutes=128,
            genre='Ação',
            rating='16'
        )
        response = self.client.get(reverse('movie-list'), {'search': 'Duna'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_sessions(self):
        response = self.client.get(reverse('session-list', args=[self.movie.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_movie_pagination(self):
        for i in range(15):
            Movie.objects.create(
                title=f'Filme {i}',
                description='Descrição',
                duration_minutes=100,
                genre='Ação',
                rating='L'
            )
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertEqual(len(response.data['results']), 10)