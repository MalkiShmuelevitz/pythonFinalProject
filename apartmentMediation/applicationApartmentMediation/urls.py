from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.get_home_page,name='home'),
    path("register/", views.Register, name='register'),
    path("login/", views.Login, name='login'),
    path("add_apartment/", views.AddApartment, name='add_apartment'),
    path("apartments/", views.Apartments, name='apartments'),
    # path("add_buyer/", views.add_buyer),
    # path("/", views.get_home_page),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)