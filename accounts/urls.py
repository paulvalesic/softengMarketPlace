from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
     path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('post_item/', views.post_item, name='post_item'),
    path('place_order/<int:item_id>/', views.place_order, name='place_order'),
    path('review_user/<int:user_id>/', views.review_user, name='review_user'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
     #path('rate_order/<int:order_id>/', views.rate_order, name='rate_order'),
      path('submit_review/<int:order_id>/', views.submit_review, name='submit_review'),
]