from django.urls import path
from . import views

urlpatterns = [
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('send_message/<int:receiver_id>/<int:item_id>/', views.send_message, name='send_message_about_item'),
    path('chat/<int:receiver_id>/', views.send_message, name='send_message'),
    path('chat/<int:receiver_id>/item/<int:item_id>/', views.send_message, name='send_message_with_item'),
]