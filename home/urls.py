# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('seller/<int:user_id>/', views.seller_profile, name='seller_profile'),
]