from django.urls import path
from . import views

app_name = 'dormitory'

urlpatterns = [
    # Asosiy sahifa - ariza formasi
    path('', views.home_view, name='home'),
    
    # Ariza yuborilgandan keyin
    path('ariza-yuborildi/<str:ariza_raqami>/', views.success_view, name='success'),
    
    # Ariza holatini tekshirish
    path('ariza-holati/', views.ariza_status_view, name='status'),
    
    # Ma'lumot sahifasi
    path('malumot/', views.info_view, name='info'),
]