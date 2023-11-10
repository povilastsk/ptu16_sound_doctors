from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
]
