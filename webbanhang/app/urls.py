from django.contrib import admin
from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('bookall/',views.bookall, name='bookall'),
    path('detail/',views.detail, name='detail'),
    path('AddBookCart/',views.AddBookCart,name='addbookcart'),
    path('delete',views.deletebookcart,name='deletebookcart'),
    path('update',views.updatebookcart,name='updatebookcart'),
    path('pay',views.Pay,name='pay')
]
