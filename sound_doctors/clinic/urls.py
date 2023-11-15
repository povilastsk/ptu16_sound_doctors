from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('regular_order/', views.RegularServiceOrderView.as_view(), name='regular_service_order'),
    path('custom_order/', views.CustomServiceOrderView.as_view(), name='custom_service_order'),
    path('cancel_order/<int:order_id>/', views.CancelOrderView.as_view(), name='cancel_order'),
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('album_detail/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('album_sale/<int:pk>/', views.AlbumSaleView.as_view(), name='album_sale'),
    path('album_order_list/', views.AlbumOrderListView.as_view(), name='album_order_list'),
    path('cancel_album_purchase/<int:album_sale_id>/', views.CancelAlbumPurchaseView.as_view(), name='cancel_album_purchase'),
]
