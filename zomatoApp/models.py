import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
    user_ph = models.CharField(max_length=10)
    def __str__(self):
        return self.user_ph

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_val = models.CharField(max_length=6)
    created_at = models.DateTimeField('created_at')

class City(models.Model):
    city_name = models.CharField(max_length=50)
    def __str__(self):
        return self.city_name

class Restaurant(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rest_name = models.CharField(max_length=100)
    rest_addr = models.CharField(max_length=100)
    rest_rating = models.IntegerField()

class Seat(models.Model):
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Booking(models.Model):
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

class SeatBookingMap(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.FloatField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_price = models.FloatField(default=0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)

class Payment(models.Model):
    payment_name = models.CharField(max_length=100)
    payment_charges = models.FloatField(default=0)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    convinience_fee = models.FloatField(default = 0)
    delivery_fee = models.FloatField(default = 0)
    discount_val = models.FloatField(default = 0)
    #order price = cart_price + conv_fee + del_fee + payment_charges - discount_val
    order_price = models.FloatField(default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_price = models.FloatField()
    qty = models.IntegerField()










# Create your models here.
