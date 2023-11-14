from . import models, forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.generic import ListView, DetailView
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
    model = models.RegularService
    template_name = 'clinic/service_list.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = models.RegularService
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
            pass
        return self.get(request, *args, **kwargs)


class DoctorListView(ListView):
    model = models.Doctor
    template_name = 'clinic/doctor_list.html'
    context_object_name = 'doctors'


@method_decorator(login_required, name='dispatch')
class OrderServiceView(View):
    template_name = 'clinic/order_form.html'

    def get(self, request, *args, **kwargs):
        regular_service_form = forms.RegularServiceOrderForm()
        custom_service_form = forms.CustomServiceOrderForm()

        return render(request, self.template_name, {
            'regular_service_form': regular_service_form,
            'custom_service_form': custom_service_form,
        })

    def post(self, request, *args, **kwargs):
        order_type = request.POST.get('order_type')
        regular_service_form = forms.RegularServiceOrderForm(request.POST)
        custom_service_form = forms.CustomServiceOrderForm(request.POST)

        if order_type == 'regular' and regular_service_form.is_valid():
            regular_service_form.instance.customer = request.user
            regular_service_form.save()
            return redirect('order_list')

        elif order_type == 'custom' and custom_service_form.is_valid():
            custom_service_form.instance.customer = request.user
            custom_service_form.save()
            return redirect('order_list')

        return render(request, self.template_name, {
            'regular_service_form': regular_service_form,
            'custom_service_form': custom_service_form,
        })


@method_decorator(login_required, name='dispatch')
class OrderListView(View):
    template_name = 'clinic/order_list.html'

    def get(self, request, *args, **kwargs):
        service_orders_regular = models.ServiceOrder.objects.filter(customer=request.user, custom_service__isnull=True)
        service_orders_custom = models.ServiceOrder.objects.filter(customer=request.user, regular_service__isnull=True)

        return render(request, self.template_name, {
            'service_orders_regular': service_orders_regular,
            'service_orders_custom': service_orders_custom,
        })
    
    
class AlbumListView(ListView):
    model = models.Album
    template_name = 'clinic/album_list.html'
    context_object_name = 'albums'


class AlbumDetailView(View):
    template_name = 'clinic/album_detail.html'

    def get(self, request, *args, **kwargs):
        album = get_object_or_404(models.Album, pk=kwargs['pk'])
        reviews = models.AlbumReview.objects.filter(album=album).order_by('-created_at')
        form = forms.AlbumReviewForm(initial={'album': album.id, 'reviewer': request.user.id}) if request.user.is_authenticated else None

        return render(request, self.template_name, {'album': album, 'reviews': reviews, 'form': form})

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(models.Album, pk=kwargs['pk'])
        form = forms.AlbumReviewForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('album_detail', pk=album.id)
        
        reviews = models.AlbumReview.objects.filter(album=album).order_by('-created_at')
        return render(request, self.template_name, {'album': album, 'reviews': reviews, 'form': form})