from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('album_detail/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('regular_order/', views.RegularServiceOrderView.as_view(), name='regular_service_order'),
    path('custom_order/', views.CustomServiceOrderView.as_view(), name='custom_service_order'),
    path('cancel_order/<int:order_id>/', views.CancelOrderView.as_view(), name='cancel_order'),
]
