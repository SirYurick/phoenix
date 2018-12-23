from django.urls import path
from phoenix import views

urlpatterns = [
    path('', views.index, name='index'),
    path('how_to_buy/', views.how_to_buy, name='how_to_buy'),
    #path('<slug:category_url>/<slug:product_url>/', views.product, name='product'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('get_bonus/', views.get_bonus, name='get_bonus'),
    path('category/<slug:category_url>/', views.category, name='category'),
]
