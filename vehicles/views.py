from decimal import Decimal, InvalidOperation

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .forms import ServiceBookingForm, VehicleListingForm
from .models import Vehicle


def vehicle_list(request):
    search = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    fuel = request.GET.get('fuel', '')
    price = request.GET.get('price', '')
    year = request.GET.get('year', '')
    sort = request.GET.get('sort', '')

    vehicles = Vehicle.objects.all()

    # Search
    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) | Q(brand__icontains=search)
        )

    # Brand filter
    if brand:
        vehicles = vehicles.filter(brand=brand)

    # Fuel filter
    if fuel:
        vehicles = vehicles.filter(fuel_type=fuel)

    # Maximum price filter
    if price:
        try:
            maximum_price = Decimal(price)
            if maximum_price >= 0:
                vehicles = vehicles.filter(price__lte=maximum_price)
        except (InvalidOperation, ValueError):
            price = ''

    # Year filter
    if year:
        try:
            vehicles = vehicles.filter(year=int(year))
        except ValueError:
            year = ''

    if sort == 'low':
        vehicles = vehicles.order_by('price')

    elif sort == 'high':
        vehicles = vehicles.order_by('-price')

    elif sort == 'newest':
        vehicles = vehicles.order_by('-year')


    # Filter options
    brands = Vehicle.objects.values_list(
        'brand', flat=True
    ).distinct()

    fuels = Vehicle.objects.values_list(
        'fuel_type', flat=True
    ).distinct()

    years = Vehicle.objects.values_list(
        'year', flat=True
    ).distinct().order_by('-year')

    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles,
        'search': search,
        'brands': brands,
        'fuels': fuels,
        'years': years,
        'selected_brand': brand,
        'selected_fuel': fuel,
        'price': price,
        'year': year,
        'sort': sort,
    })


def service_booking(request):
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(
                request,
                f"Service booking received for {booking.car_model} on {booking.preferred_date:%d %b %Y}.",
            )
            return redirect('service_booking')
    else:
        form = ServiceBookingForm()

    return render(request, 'vehicles/service_booking.html', {'form': form})


def vehicle_detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)

    return render(request, 'vehicles/vehicle_detail.html', {
        'vehicle': vehicle
    })


@login_required(login_url='login')
def sell_vehicle(request):
    if request.method == 'POST':
        form = VehicleListingForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'{vehicle.name} has been listed for sale.')
            return redirect('sell_vehicle')
    else:
        form = VehicleListingForm()

    return render(request, 'vehicles/sell_vehicle.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('vehicle_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'vehicles/signup.html', {
                'error': 'Username and password are required.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'vehicles/signup.html', {
                'error': 'Username already exists.'
            })

        try:
            validate_password(password)
        except ValidationError as error:
            return render(request, 'vehicles/signup.html', {
                'error': ' '.join(error.messages)
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('vehicle_list')

    return render(request, 'vehicles/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('vehicle_list')

    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('vehicle_list')

        return render(request, 'vehicles/login.html', {
            'error': 'Invalid username or password.',
            'next': next_url,
        })

    return render(request, 'vehicles/login.html', {'next': next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('vehicle_list')