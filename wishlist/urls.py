from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_wishlist, name='wishlist'),
    # path('wishlist/', views.view_wishlist, name='wishlist'),
    path('remove/<item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
