from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/', views.view_wishlist, name='wishlist_link'),
    # path('wishlist/', views.view_wishlist, name='wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
