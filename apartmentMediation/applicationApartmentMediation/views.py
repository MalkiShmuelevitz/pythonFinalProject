from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth import get_user_model
from .forms import RegisterForm, ApartmentForm, AddressForm, ImagesForm,ApartmentMediatorForm
from .models import User, Apartment, Address, Image

# Create your views here.


def get_home_page(request):
	return render(request, 'home.html')


def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                return redirect('register/')
        else:
            return HttpResponse("form.is_not_valid")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def AddApartment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.status != 'BUYER':
                if request.user.status == 'MEDIATOR':
                    apa = ApartmentMediatorForm(request.POST)
                else:
                    apa = ApartmentForm(request.POST)
                ad = AddressForm(request.POST)
                ima = ImagesForm(request.POST, request.FILES)
                if apa.is_valid() and ad.is_valid() and ima.is_valid():
                    with transaction.atomic():
                        address = ad.save()
                        apartment = apa.save(commit=False)
                        images = ima.save(commit=False)
                        apartment.seller = request.user
                        if request.user.status != 'MEDIATOR':
                            apartment.isMediator = False
                            apartment.charge = 0
                        else:
                            apartment.isMediator = True
                        apartment.address = address
                        images.apartment = apartment
                        apartment.save()
                        images.save()
                        return HttpResponse("Apartment SAVED")
            else:
                return HttpResponse("UnAthoriezed")
        if request.user.status == 'MEDIATOR':
            apartment_form = ApartmentMediatorForm()
        else:
            apartment_form = ApartmentForm()
        address_form = AddressForm()
        images_form = ImagesForm()
        return render(request, 'add_apartment.html', {
            'apartment_form': apartment_form,
            'address_form': address_form,
            'images_form': images_form})
    else:
        return redirect('login/')


@login_required(login_url='login')
def Apartments(request):
    apartments = Apartment.objects.all()
    if request.user.status == 'BUYER':
        all_apartments = filter(lambda x: x.status == 'FOR_SALE', apartments)
    else:
        all_apartments = filter(lambda x: x.seller == request.user, apartments)
    data = {
        'apartments': all_apartments,
        'images': Image.objects.all()
    }
    return render(request, 'view_apartment.html', data)

