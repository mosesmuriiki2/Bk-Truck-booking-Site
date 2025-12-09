from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Truck, Extra, Driver
from bookings.models import Booking


def home(request):
    # Landing page (hero) instead of redirect
    return render(request, 'home.html')


def truck_list(request):
    trucks_qs = Truck.objects.filter(is_active=True).order_by('name')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start = end = None
    if start_date and end_date:
        from datetime import datetime
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            start = end = None

    trucks = list(trucks_qs)
    # Default: hide trucks currently booked today if no filter is provided
    today = timezone.now().date()
    if not start and not end:
        trucks = [t for t in trucks if t.is_available_for(today, today)]
    elif start and end and end >= start:
        # Filter out trucks that are not available for given dates
        available = []
        for t in trucks:
            if t.is_available_for(start, end):
                available.append(t)
        trucks = available

    return render(request, 'trucks/list.html', {
        "trucks": trucks,
        "start_date": start_date or '',
        "end_date": end_date or '',
        "today": today,
    })


def truck_detail(request, slug):
    truck = get_object_or_404(Truck, slug=slug, is_active=True)
    extras = Extra.objects.filter(active=True)

    if request.method == 'POST':
        # Extract booking fields from POST
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        route_start = request.POST.get('route_start')
        route_end = request.POST.get('route_end')
        route_notes = request.POST.get('route_notes') or ''
        purpose = request.POST.get('purpose') or ''
        extras_ids = request.POST.getlist('extras')

        if not all([customer_name, email, start_date, end_date, route_start, route_end]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            from datetime import datetime
            try:
                sd = datetime.strptime(start_date, '%Y-%m-%d').date()
                ed = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                sd = ed = None
            if not sd or not ed or ed < sd:
                messages.error(request, 'Please provide valid start and end dates.')
            elif not truck.is_available_for(sd, ed):
                messages.error(request, 'This truck is not available for the selected dates.')
            else:
                booking = Booking(
                    user=request.user if request.user.is_authenticated else None,
                    customer_name=customer_name,
                    email=email,
                    phone=phone or '',
                    truck=truck,
                    start_date=sd,
                    end_date=ed,
                    route_start=route_start,
                    route_end=route_end,
                    route_notes=route_notes,
                    purpose=purpose,
                    status='reserved',
                )
                booking.save()
                # Attach extras and compute pricing
                selected_extras = Extra.objects.filter(id__in=extras_ids)
                if selected_exras := list(selected_extras):
                    booking.extras.set(selected_exras)
                days = booking.days
                extras_total = sum([float(e.price_per_day) for e in selected_exras]) * days if selected_exras else 0
                total = float(truck.daily_price) * days + extras_total
                booking.total_price = total
                booking.save()
                messages.success(request, 'Your booking has been created and reserved. Admin will review and approve.')
                return redirect('bookings:my_bookings') if request.user.is_authenticated else redirect('trucks:detail', slug=truck.slug)

    return render(request, 'trucks/detail.html', {"truck": truck, "extras": extras})


def driver_list(request):
    drivers = Driver.objects.filter(active=True).order_by('name')
    return render(request, 'trucks/driver_list.html', {"drivers": drivers})


def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk, active=True)
    trucks = Truck.objects.filter(driver=driver, is_active=True)
    return render(request, 'trucks/driver_detail.html', {"driver": driver, "trucks": trucks})
