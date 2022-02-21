from datetime import datetime, timedelta
import pytz
import json
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
import string
import random

from zomatoApp.models import *

# Create your views here.
def GenerateOTP(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_ph = body['user_ph']
    user_id = User.objects.get(user_ph = user_ph).id
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))    
    try:
        obj = Otp.objects.get(user_id=user_id)
        setattr(obj, 'otp_val', ran)
        setattr(obj, 'created_at', datetime.now())
        obj.save()
    except Otp.DoesNotExist:
        obj = Otp(otp_val=ran, created_at = datetime.now(), user_id=user_id,)
        obj.save()
    return HttpResponse("OTP Generated: "+ran)

def VerifyOTP(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_ph = body['user_ph']
    user_id = User.objects.get(user_ph = user_ph).id
    otp_val = body['otp']
    otp= Otp.objects.get(user_id=user_id)
    if otp_val == otp.otp_val and pytz.utc.localize(datetime.now()) <= otp.created_at + timedelta(minutes=1):
        return HttpResponse("User Verified!")
    return HttpResponse("Failed to Login!")

def GetCity(request):
    city_queryset = list(City.objects.all())
    city_list = []
    for city in city_queryset:
        city_list.append(city.city_name)
    res = {}
    res['city_list'] = city_list
    return JsonResponse(res)

def GetRestByCity(request, city_id):
    rest_queryset = Restaurant.objects.filter(city_id = city_id)
    rest_list = []
    for rest in rest_queryset:
        rest_list.append(rest.rest_name)
    res = {}
    res['rest_list'] = rest_list
    return JsonResponse(res)

def GetReservations(request, rest_id):
    seat_set = Seat.objects.filter(rest_id = rest_id) 
    seat_list = []
    for seat in seat_set:
        seat_list.append(seat.id)
    total_seats = len(seat_list)
    reserved_seats_count = Booking.objects.filter(seatbookingmap__seat_id__in=seat_list,
     from_time__lte=pytz.utc.localize(datetime.datetime.now()),
     to_time__gte=pytz.utc.localize(datetime.datetime.now()),
     status = 1,).count()
    res = {}
    res['Reserved Seats'] = reserved_seats_count
    res['Unreserved Seats'] = total_seats - reserved_seats_count
    return JsonResponse(res)

def GetItemsByRestaurant(request, rest_id):
    item_set = Item.objects.filter(rest_id = rest_id)
    item_list = []
    for item in item_set:
        item_list.append({'name':item.item_name, 'price': item.price,})
    res = {}
    res['items'] = item_list
    return JsonResponse(res)


def CreateBooking (request):
    # POST
    # body = {
    #     seat_list: [1,2],
    #     from_timme: '',
    #     to_time: ''
    # }
    user_id = request.META['HTTP_X_USERID']
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    seat_list = body['seat_list']
    from_time = body['from_time']
    to_time = body['to_time']
    for seat in seat_list:
        try:
            seat_booking = Booking.objects.filter(seatbookingmap_seat_id = seat.id).last
        except Booking.DoesNotExist:
            continue
        if from_time <= seat_booking.from_time <= to_time or from_time <= seat_booking.to_time <= to_time:
             return Http404("Seat id: "+str(seat.id)+" is not available for the booking time slot.")   

    booking = Booking.objects.create(from_time = from_time, to_time=to_time, user_id=user_id)
    booking.save()
    booking_id = booking.id
    for seat in seat_list:
        seatBookingMapEntry = SeatBookingMap.objects.create(seat_id = seat, booking_id = booking_id)
        seatBookingMapEntry.save()
    res={}
    res['booking_id'] = booking_id
    return JsonResponse(res)

def AddToCart(request):
    user_id = request.META['HTTP_X_USERID']
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    items = body['items']
    # POST
    # body = {
    #     items: [
    #         {
    #             'item_id': '',
    #             'qty': 'qty',
    #         }
    #     ]
    # }
    add_cart_price = 0

    try:
        cart = Cart.objects.get(user_id=user_id)
        

    except Cart.DoesNotExist:
        cart = Cart(cart_price=0, user_id=user_id,)
        cart.save()  

    for item in items:
        
        try:
            cartItem = CartItem.objects.get(cart_id = cart.id,item_id = item["item_id"])
        except CartItem.DoesNotExist: 
            cartItem = CartItem(item_id = item["item_id"], qty = 0, cart_id = cart.id)
            cartItem.save()
        curr_qty = cartItem.qty + item['qty']
        setattr(cartItem, 'qty', curr_qty)
        cartItem.save()
        item_price = Item.objects.get(pk = item["item_id"]).price
        add_cart_price += item_price*item['qty']
    
    cart_curr_price = cart.cart_price + add_cart_price
    setattr(cart, 'cart_price', cart_curr_price)
    cart.save()

    res = {}
    res['cart_id'] = cart.id
    res['cart_price'] = cart.cart_price
    
    return JsonResponse(res)

def CreateOrder(request, cart_id):
    try:
        cart = Cart.objects.get(id = cart_id)
    except Cart.DoesNotExist:
        return Http404("No cart is present!")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    conv_fee = body['conv_fee']
    del_fee = body['del_fee']
    discount_val = body['discount_val']
    payment_id = body['payment_id']
    order_price = cart.cart_price + conv_fee + del_fee - discount_val
    if order_price < 0 :
        return Http404("Error calculating Order price")
    order = Order(status = 0, created_at = datetime.datetime.now(), convinience_fee = conv_fee,
    delivery_fee = del_fee, discount_val = discount_val, order_price = order_price,
    cart_id = cart_id, payment_id = payment_id);

    order.save()
    cartItems = CartItem.objects.filter(cart_id = cart.id)
    for cartItem in cartItems:
        item_price = Item.objects.get(id = cartItem.item_id).price
        order_item = OrderItem(item_id =  cartItem.item_id,
        item_price = item_price, order_id = order.id, qty=cartItem.qty)
        order_item.save()
        cartItem.delete()
    
    setattr(cart, 'cart_price', 0)
    cart.save()
    res={}
    res['order_id'] = order.id
    return JsonResponse(res)

def DeliverOrder(request, order_id):
    print(order_id)
    order = Order.objects.get(pk = order_id)
    setattr(order,'status', 1)
    order.save()
    return HttpResponse("Order id: "+str(order.id)+" delivered successfully!")








    


    

    
