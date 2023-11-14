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
            pass
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
        form = forms.ServiceOrderForm(request.POST, request.FILES)

        if form.is_valid():
            order_type = request.POST.get('order_type')
            custom_text = form.cleaned_data['custom_text']
            custom_img = form.cleaned_data['custom_img']
            doctor = form.cleaned_data['doctor']

            if order_type == 'custom':
                custom_order = models.CustomServiceOrder(
                    custom_text=custom_text,
                    custom_img=custom_img,
                    doctor=doctor,
                    customer=request.user
                )
                custom_order.save()
            else:
                # Regular order, include the service field only if it's present in the form data
                regular_order = models.ServiceOrder(
                    doctor=doctor,
                    customer=request.user
                )
                if 'service' in form.cleaned_data:
                    regular_order.service = form.cleaned_data['service']
                regular_order.save()

            return redirect('order_list')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class OrderListView(View):
    template_name = 'clinic/order_list.html'

    def get(self, request, *args, **kwargs):
        # Fetch regular and custom service orders
        service_orders_regular = models.ServiceOrder.objects.filter(customer=request.user)
        service_orders_custom = models.CustomServiceOrder.objects.filter(customer=request.user)

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