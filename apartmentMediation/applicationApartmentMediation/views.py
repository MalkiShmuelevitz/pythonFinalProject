from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth import get_user_model
from .forms import RegisterForm, ApartmentForm, AddressForm, ImagesForm, ApartmentMediatorForm
from .models import User, Apartment, Address, Image, Interested
from django.http import JsonResponse
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
                        images = request.FILES.getlist('image')
                        apartment.seller = request.user
                        if request.user.status != 'MEDIATOR':
                            apartment.isMediator = False
                            apartment.charge = 0
                        else:
                            apartment.isMediator = True
                        apartment.address = address
                        apartment.save()
                        for img in images:
                            Image.objects.create(apartment=apartment, image=img)
                        # לאחר שמירת הדירה, מפנים לעמוד של ההצלחה
                        return render(request, 'apartment_saved.html')  # עמוד חדש שמציג את ההודעה המוצלחת
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
    # אם המשתמש שלח את הטופס
    if request.method == 'POST':
        selected_item = request.POST.get('filterSelect')
        filterField = request.POST.get('filterInput')
        apartments = Apartment.objects.all()
        # סינון דירות לפי קריטריונים
        if selected_item == 'numberOfrooms' and filterField:
            apartments = apartments.filter(numberRooms=filterField)
        if selected_item == 'city' and filterField:
            apartments = apartments.filter(address__city=filterField)
    else:
        apartments = Apartment.objects.all()  # אם לא נבחרו פילטרים, הצגת כל הדירות

    # בדיקה אם המשתמש הוא קונה או מוכר
    if request.user.status == 'BUYER':
        all_apartments = apartments.filter(status='FOR_SALE')
        data = {
            'apartments': all_apartments,
            'images': Image.objects.filter(apartment__in=apartments),
            'seller': "null"
        }
    else:
        all_apartments = apartments.filter(seller=request.user)
        data = {
            'apartments': all_apartments,
            'images': Image.objects.filter(apartment__in=apartments),
            'seller': request.user
        }

    return render(request, 'view_apartment.html', data)


@login_required(login_url='login')
def add_request(request, id):
    if request.method == 'POST':  # בדוק שהבקשה היא מסוג POST
        interested = Interested()
        interested.createInterested(request.user, Apartment.objects.get(id=id))
        interested.save()
        return JsonResponse({"message": "פניתך התקבלה בהצלחה"})
    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required(login_url='login')
def sale(request, id):
    apartment = Apartment.objects.get(id=id)
    apartment.status = "SOLD"
    apartment.save()
    next_url = request.GET.get('next', 'apartments')
    return redirect(next_url)


@login_required(login_url='login')
def requests(request, id):
    requests_all = Interested.objects.all()
    all_requests = list(filter(lambda x: x.apartment.id == id, requests_all))
    data = {
        'requests': all_requests
    }
    return render(request, 'requests.html', data)

@login_required(login_url='login')
def personal(request):
    apartments_all = Apartment.objects.all()
    apartments = filter(lambda x: x.seller == request.user and x.status == 'SOLD',apartments_all)
    total_price = 0
    for i in apartments:
        total_price = total_price + i.charge / 100 * i.price
    return render(request, 'personal.html', {'total_price': total_price})


