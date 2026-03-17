from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from users.models import User
from movies.models import Movie, Room, Session
from .models import Seat, Ticket


class ReservationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@cinepolis.com',
            password='Senha@123'
        )
        self.movie = Movie.objects.create(
            title='Duna: Parte Dois',
            description='Descrição',
            duration_minutes=166,
            genre='Ficção Científica',
            rating='14'
        )
        self.room = Room.objects.create(name='Sala 1', rows=4, cols=5)
        self.session = Session.objects.create(
            movie=self.movie,
            room=self.room,
            datetime=timezone.now() + timedelta(days=1),
            language='Dublado',
            format='2D'
        )
        self.seat = Seat.objects.create(
            session=self.session,
            row='A',
            col=1,
            status=Seat.Status.AVAILABLE
        )

    def test_seat_map(self):
        response = self.client.get(
            reverse('seat-map', args=[self.session.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie'], 'Duna: Parte Dois')

    def test_reserve_seat_unauthenticated(self):
        response = self.client.post(
            reverse('reserve-seat', args=[self.session.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reserve_seat_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('reserve-seat', args=[self.session.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, Seat.Status.RESERVED)

    def test_reserve_already_reserved_seat(self):
        self.seat.status = Seat.Status.RESERVED
        self.seat.reserved_by = self.user
        self.seat.reserved_at = timezone.now()
        self.seat.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('reserve-seat', args=[self.session.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_success(self):
        self.seat.status = Seat.Status.RESERVED
        self.seat.reserved_by = self.user
        self.seat.reserved_at = timezone.now()
        self.seat.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('checkout', args=[self.session.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('ticket', response.data)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, Seat.Status.PURCHASED)

    def test_checkout_expired_reservation(self):
        self.seat.status = Seat.Status.RESERVED
        self.seat.reserved_by = self.user
        self.seat.reserved_at = timezone.now() - timedelta(minutes=15)
        self.seat.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('checkout', args=[self.session.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('expirada', response.data['error'])

    def test_my_tickets(self):
        Ticket.objects.create(
            user=self.user,
            seat=self.seat,
            ticket_code='CNP-TEST001'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('my-tickets'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['ticket_code'], 'CNP-TEST001')

    def test_my_tickets_unauthenticated(self):
        response = self.client.get(reverse('my-tickets'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)