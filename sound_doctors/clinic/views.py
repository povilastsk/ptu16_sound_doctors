from django.db.models.query import QuerySet
from django.contrib import messages
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

@login_required
def service_review_create(request, service_pk):
    service = models.Service.objects.get(pk=service_pk)

    if request.method == 'POST':
        form = forms.ServiceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.service = service
            review.save()
            messages.success(request, 'Review posted successfully.')
            return redirect('service_review_create', service_pk=service_pk)
        else:
            messages.error(request, 'Error posting review. Please check your form.')
    else:
        form = forms.ServiceReviewForm()

    return render(request, 'clinic/service_review_create.html', {'form': form, 'service': service})

class ServiceListView(ListView):
    model = models.Service
    template_name = 'clinic/service_list.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = models.Service
    template_name = 'clinic/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reviews'] = models.ServiceReview.objects.filter(service=self.object).order_by('-created_at')

        context['form'] = forms.ServiceReviewForm(initial={'service': self.object.id, 'reviewer': self.request.user.id})

        return context

    def post(self, request, *args, **kwargs):
        form = forms.ServiceReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('service_detail', kwargs={'pk': self.kwargs['pk']}))
        else:
            # Handle form errors if needed
            pass

        # If the form is not valid, render the detail view with errors
        return self.get(request, *args, **kwargs)


class DoctorListView(ListView):
    model = models.Doctor
    template_name = 'clinic/doctor_list.html'
    context_object_name = 'doctors'


class OrderServiceView(View):
    template_name = 'clinic/order_form.html'

    def get(self, request, *args, **kwargs):
        form = forms.ServiceOrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ServiceOrderForm(request.POST)
        if form.is_valid():
            service_order = form.save(commit=False)
            service_order.customer = request.user
            service_order.save()
            return redirect('order_list')  # Redirect to the order list view
        return render(request, self.template_name, {'form': form})


class OrderListView(View):
    template_name = 'clinic/order_list.html'

    def get(self, request, *args, **kwargs):
        service_orders = models.ServiceOrder.objects.filter(customer=request.user)
        return render(request, self.template_name, {'service_orders': service_orders})