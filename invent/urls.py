from django.urls import path
from .views import *

urlpatterns = [
    path('home/', invent_home, name='home'),
    path('floor/', floor, name='floor'),
    path('update/', update_inv, name='update_inv'),
    path('delete/', delete_inv, name='delete_inv'),
    path('', auth, name='auth'),
    path('logout/', log_out, name='logout'),
    path('repair/', repair, name='repair'),
    path('delete_rep/', delete_repair, name='delete_repair'),
    path('update_rep/', update_repair, name='update_repair'),
    path('dep/', department, name='department'),
    path('delete_dep/', delete_dep, name='delete_dep'),
    path('update_dep/', update_dep, name='update_dep'),
    path('location/', location, name='location'),
    path('delete_loc/', delete_loc, name='delete_loc'),
    path('update_loc/', update_loc, name='update_loc')
]