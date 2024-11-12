from django.urls import path
from . import views

urlpatterns = [


    path('', views.user_listbook, name='userbooklist'),
    path('detailsview/<int:book_id>/',views.user_detailsview,name='userdetails'),
    path('search/', views.usersearch_book,name='usersearch'),
    path('addtocart/<int:book_id>/', views.add_to_cart,name='addtocart'),
    path('view_cart/', views.view_cart,name='viewcart'),
    path('increase/<int:item_id>/', views.increase_quantity,name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity,name='decrease_quantity'),
    path('removecart/<int:item_id>/', views.remove_cart,name='remove_cart'),
    path('create_checkoutsession/', views.create_checkout_session,name='checkout'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),



]