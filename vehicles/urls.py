from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('services/', views.service_booking, name='service_booking'),
    path('vehicle/<int:id>/', views.vehicle_detail, name='vehicle_detail'),
    path('sell/', views.sell_vehicle, name='sell_vehicle'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]