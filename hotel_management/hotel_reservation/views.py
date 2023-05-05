from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Hotel, Reservation
from .forms import ReservationForm
from django.db.models import Q
from django.contrib import messages


def hotel_list(request):
    if not Hotel.objects.exists():
        Hotel.objects.create(name = "Isla", location = "Beit Sahour")
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})

# def reservation_list(request, hotel_id):
#     hotel = Hotel.objects.get(id=hotel_id)
#     reservations = Reservation.objects.filter(hotel=hotel)
#     return render(request, 'reservation_list.html', {'reservations': reservations, 'hotel': hotel})
def reservation_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    reservations = Reservation.objects.filter(hotel=hotel).order_by('check_in', 'floor_number', 'room_number')
    return render(request, 'reservation_list.html', {'hotel': hotel, 'reservations': reservations})

# def new_reservation(request, hotel_id):
#     hotel = Hotel.objects.get(id=hotel_id)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.hotel = hotel
#             reservation.save()
#             return redirect('reservation_list', hotel_id=hotel.id)
#     else:
#         form = ReservationForm()
#     return render(request, 'new_reservation.html', {'form': form, 'hotel': hotel})
def new_reservation(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    show_error_modal = False
    # hotel = Hotel.objects.get(id=hotel_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.hotel = hotel

            # Checking for existing and non-overlapping rooms
            overlapping_reservations = Reservation.objects.filter(
                Q(hotel=hotel) &
                Q(floor_number=reservation.floor_number) &
                Q(room_number=reservation.room_number) &
                (
                    (Q(check_in__lte=reservation.check_in) & Q(check_out__gt=reservation.check_in)) |
                    (Q(check_in__lt=reservation.check_out) & Q(check_out__gte=reservation.check_out)) |
                    (Q(check_in__gte=reservation.check_in) & Q(check_out__lte=reservation.check_out))
                )
            )

            if overlapping_reservations.exists():
                show_error_modal = True
                # messages.error(request, 'This room is already booked during the selected date range.')
            else:
                reservation.save()
                return HttpResponseRedirect(reverse('hotel_reservation:reservation_list', args=(hotel.id,)))
    else:
        form = ReservationForm()

    return render(request, 'new_reservation.html', {'form': form, 'hotel': hotel, 'show_error_modal': show_error_modal})


from django.shortcuts import get_object_or_404

# def cancel_reservation(request, hotel_id, reservation_id):
#     reservation = get_object_or_404(Reservation, pk=reservation_id)
#     reservation.delete()
#     return HttpResponseRedirect(reverse('hotel_reservation:reservation_list', args=(hotel_id,)))
def cancel_reservation(request, hotel_id, reservation_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    return redirect('hotel_reservation:reservation_list', hotel_id=hotel.id)