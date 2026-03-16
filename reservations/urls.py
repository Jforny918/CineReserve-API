from django.urls import path
from .views import SeatMapView, ReserveSeatView, CheckoutView, MyTicketsView

urlpatterns = [
    path('sessions/<int:session_id>/seats/', SeatMapView.as_view(), name='seat-map'),
    path('sessions/<int:session_id>/reserve/', ReserveSeatView.as_view(), name='reserve-seat'),
    path('sessions/<int:session_id>/checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
]