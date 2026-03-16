from django.db import models
from django.conf import settings


class Seat(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponível'
        RESERVED = 'reserved', 'Reservado temporariamente'
        PURCHASED = 'purchased', 'Comprado'

    session = models.ForeignKey(
        'movies.Session',
        on_delete=models.CASCADE,
        related_name='seats'
    )
    row = models.CharField(max_length=5)    # Ex: "A", "B", "C"
    col = models.PositiveIntegerField()     # Ex: 1, 2, 3
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reserved_seats'
    )
    reserved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('session', 'row', 'col')

    def __str__(self):
        return f"{self.session} - {self.row}{self.col} ({self.status})"


class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    seat = models.OneToOneField(
        Seat,
        on_delete=models.CASCADE,
        related_name='ticket'
    )
    ticket_code = models.CharField(max_length=20, unique=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_code} - {self.user.email}"