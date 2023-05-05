from django.urls import path
from . import views

app_name = 'hotel_reservation'

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/reservations/', views.reservation_list, name='reservation_list'),
    path('hotel/<int:hotel_id>/new_reservation/', views.new_reservation, name='new_reservation'),
    path('hotel/<int:hotel_id>/reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
]
