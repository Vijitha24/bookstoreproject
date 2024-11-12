from django.urls import path
from . import views

urlpatterns = [
    path('Createbook', views.Createbook, name='createbook'),
    path("author/",views.Createauthor,name='author'),
    path('', views.listbook, name='booklist'),
    path('detailsview/<int:book_id>/',views.detailsview,name='details'),
    path('updateview/<int:book_id>/', views.updatebook, name='update'),
    path('deleteview/<int:book_id>/', views.deleteview ,name='delete'),
    path('index', views.index),
    path('search/', views.search_book,name='search'),


]