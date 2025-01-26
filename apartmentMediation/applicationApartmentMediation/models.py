from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Status(models.TextChoices):
        BUYER = "BUYER", _("Buyer")
        SELLER = "SELLER", _("Seller")
        BUYER_AND_SELLER = "BUYER_AND_SELLER", _("Buyer_and_seller")
        MEDIATOR = "MEDIATOR", _("Mediator")
    phone = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=17, choices=Status, default=Status.BUYER)

    # def __str__(self):
    #     return f"{self.id}:{self.firstName} {self.lastName}"


class Address(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    city = models.CharField(max_length=15)
    street = models.CharField(max_length=20)
    buildingNumber = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.city} {self.street} {self.buildingNumber}"


class Apartment(models.Model):
    class Status(models.TextChoices):
       SOLD = "SOLD", _("Sold")
       FOR_SALE = "FOR_SALE", _("For_sale")
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    seller= models.ForeignKey(User, on_delete=models.DO_NOTHING,)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    numberRooms = models.IntegerField()
    size = models.FloatField()
    floor = models.IntegerField()
    isMediator = models.BooleanField()
    price = models.IntegerField()
    charge = models.FloatField()
    status = models.CharField(max_length=8, choices=Status, default=Status.FOR_SALE)

    def __str__(self):
        return f" {self.id}: apartment of {self.numberRooms} rooms"


class Interested(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    def createInterested(self,buyer,apartment):
        self.buyer = buyer
        self.apartment = apartment
        return self


class Image(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

