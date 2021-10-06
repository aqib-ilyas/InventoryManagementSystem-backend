from django.urls import path, include
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('add_products/', views.add_products, name='add_products'),
    path('update_products/', views.update_products, name='update_products'),
    path('get_products/', views.get_products, name='get_products'),
    path('get_sellers/', views.get_sellers, name='get_sellers'),
    path('delete_products/', views.delete_products, name='delete_products'),
    path('update_products/', views.update_products, name='update_products')
]
