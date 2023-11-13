from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('order/', views.OrderServiceView.as_view(), name='order_service'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('album_detail/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
]
