from . import models, forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


class RegularServiceOrderView(LoginRequiredMixin, View):
    template_name = 'clinic/regular_service_order.html'
    login_url = 'user_profile/login'

    def get(self, request, *args, **kwargs):
        form = forms.RegularServiceOrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.RegularServiceOrderForm(request.POST)
        if form.is_valid():
            regular_service_order = form.save(commit=False)
            regular_service_order.customer = request.user
            regular_service_order.save()
            return redirect('order_list')

        return render(request, self.template_name, {'form': form})

class CustomServiceOrderView(LoginRequiredMixin, View):
    template_name = 'clinic/custom_service_order.html'
    login_url = 'user_profile/login'

    def get(self, request, *args, **kwargs):
        form = forms.CustomServiceOrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.CustomServiceOrderForm(request.POST)
        if form.is_valid():
            custom_service_order = form.save(commit=False)
            custom_service_order.customer = request.user
            custom_service_order.save()
            return redirect('order_list')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class OrderListView(View):
    template_name = 'clinic/order_list.html'

    def get(self, request, *args, **kwargs):
        service_orders = models.ServiceOrder.objects.filter(customer=request.user)
        return render(request, self.template_name, {
            'service_orders': service_orders,
        })
    
@method_decorator(login_required, name='dispatch')
class CancelOrderView(View):

    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(models.ServiceOrder, id=order_id, customer=request.user)
        if order.status == 0:
            order.status = 2  
            order.save()
        return redirect('order_list')
    
    
class AlbumListView(ListView):
    model = models.Album
    template_name = 'clinic/album_list.html'
    context_object_name = 'albums'


class AlbumDetailView(View):
    template_name = 'clinic/album_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        album = get_object_or_404(models.Album, pk=kwargs['pk'])
        reviews = models.AlbumReview.objects.filter(album=album).order_by('-created_at')
        review_form = forms.AlbumReviewForm(initial={'album': album.id, 'reviewer': request.user.id}) if request.user.is_authenticated else None
        return render(request, self.template_name, {'album': album, 'reviews': reviews, 'review_form': review_form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        album = get_object_or_404(models.Album, pk=kwargs['pk'])
        review_form = forms.AlbumReviewForm(request.POST)

        if 'review_submit' in request.POST:
            if review_form.is_valid():
                review_form.save()

        elif 'buy_now' in request.POST:
            album_sale = models.AlbumSale.objects.create(customer=request.user, album=album)
            return redirect('album_order_list')

        return redirect('album_detail', pk=album.id)
    

@method_decorator(login_required, name='dispatch')
class AlbumOrderListView(View):
    template_name = 'clinic/album_order_list.html'

    def get(self, request, *args, **kwargs):
        album_sales = models.AlbumSale.objects.filter(customer=request.user)
        return render(request, self.template_name, {'album_sales': album_sales})

    def post(self, request, *args, **kwargs):
        form = forms.AlbumSaleForm(request.POST)
        album = get_object_or_404(models.Album, pk=kwargs.get('pk'))

        if form.is_valid():
            album_sale = form.save(commit=False)
            album_sale.customer = request.user
            album_sale.album = album
            album_sale.save()
            return redirect('album_order_list')

        album_sales = models.AlbumSale.objects.filter(customer=request.user)
        return render(request, self.template_name, {'album_sales': album_sales})
    
class AlbumSaleView(View):
    template_name = 'clinic/album_detail.html'

    def get(self, request, *args, **kwargs):
        album_id = kwargs.get('pk')
        album = get_object_or_404(models.Album, pk=album_id)
        album_sale_form = forms.AlbumSaleForm(initial={'album': album})
        return render(request, self.template_name, {'album': album, 'album_sale_form': album_sale_form})

    def post(self, request, *args, **kwargs):
        album_id = kwargs.get('pk')
        album = get_object_or_404(models.Album, pk=album_id)
        album_sale_form = forms.AlbumSaleForm(request.POST)

        if album_sale_form.is_valid():
            album_sale = album_sale_form.save(commit=False)
            album_sale.customer = request.user
            album_sale.album = album
            album_sale.save()

            return redirect('album_order_list')
        else:
            return render(request, self.template_name, {'album': album, 'album_sale_form': album_sale_form})
        

@method_decorator(login_required, name='dispatch')
class CancelAlbumPurchaseView(View):
    def get(self, request, *args, **kwargs):
        album_sale_id = kwargs.get('album_sale_id')
        try:
            album_sale = models.AlbumSale.objects.get(id=album_sale_id, customer=request.user)
            if album_sale.status == 0:
                album_sale.status = 2
                album_sale.save()
        except models.AlbumSale.DoesNotExist:
            pass
        return redirect('album_order_list')
    
    def post(self, request, *args, **kwargs):
        album_sale_id = kwargs.get('album_sale_id')
        try:
            album_sale = models.AlbumSale.objects.get(id=album_sale_id, customer=request.user)
            if album_sale.status == 0:
                album_sale.status = 2
                album_sale.save()
        except models.AlbumSale.DoesNotExist:
            pass
        return redirect('album_order_list')