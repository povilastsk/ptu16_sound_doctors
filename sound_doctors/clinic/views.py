from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from . import models, forms
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic import View

def index(request):
    return render(request, "clinic/index.html")

def about_us(request):
    about_us_content = models.AboutUs.objects.first()
    return render(
        request,
        "clinic/about_us.html",
        {"about_us_content": about_us_content}
    )


class ServiceListView(ListView):
    model = models.Service
    template_name = 'clinic/service_list.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = models.Service
    template_name = 'clinic/service_detail.html'
    context_object_name = 'service'


class DoctorListView(ListView):
    model = models.Doctor
    template_name = 'clinic/doctor_list.html'
    context_object_name = 'doctors'