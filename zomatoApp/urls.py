from django.urls import path

from . import views


urlpatterns = [
    path('login/generateOTP/', views.GenerateOTP,name='generateOTP'),
    path('login/', views.VerifyOTP,name='verifyOTP'),
    path('cities_list/', views.GetCity, name='getCity'),
    path('city/<int:city_id>/restaurants', views.GetRestByCity, name='getRestByCity'),
    path('restaurant/<int:rest_id>/reservations', views.GetReservations, name='getReservations'),
    path('restaurant/<int:rest_id>/items', views.GetItemsByRestaurant,name='getItemsByRestaurant'),
    path('add_to_cart', views.AddToCart,name='addToCart'),
    path('create_booking', 
        views.CreateBooking,name='createBooking'),
    path('cart/<int:cart_id>/create_order', views.CreateOrder, name='createOrder'),
    path('order/<int:order_id>/delivery_success', views.DeliverOrder, name='deliverOrder')
]