from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def my_bookings(request):
    qs = Booking.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'bookings/my_bookings.html', {"bookings": qs})
