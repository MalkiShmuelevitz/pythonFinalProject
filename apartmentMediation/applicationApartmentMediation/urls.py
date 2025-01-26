from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_request

urlpatterns = [
    path("", views.get_home_page,name='home'),
    path("register/", views.Register, name='register'),
    path("login/", views.Login, name='login'),
    path("add_apartment/", views.AddApartment, name='add_apartment'),
    path("apartments/", views.Apartments, name='apartments'),
    path('add_request/<int:id>', views.add_request, name='add_request'),
    path("sale/<int:id>", views.sale, name='sale'),
    path("requests/<int:id>", views.requests, name='requests'),
    path("personal/", views.personal, name='personal'),
    path("filters/", views.filterByData),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)