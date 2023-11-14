from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from django.contrib.auth.models import User


User = get_user_model()

    
class Instrument(models.Model):
    name = models.CharField(_("name"), max_length=50)
    type = models.CharField(_("type"), max_length=50)
    damage_text = HTMLField(_("damage_text"), max_length=500, default='', blank=True)
    damage_img = models.ImageField(_("damage_img"), upload_to='damage_img', null=True, blank=True)
    

    class Meta:
        verbose_name = _("instrument")
        verbose_name_plural = _("instruments")

    def __str__(self):
        return f"{self.name} {self.type}"

    def get_absolute_url(self):
        return reverse("instrument_detail", kwargs={"pk": self.pk})


class Doctor(models.Model):
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    specialization = models.CharField(_("specialization"), max_length=100)

    class Meta:
        verbose_name = _("doctor")
        verbose_name_plural = _("doctors")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.specialization}"

    def get_absolute_url(self):
        return reverse("doctor_detail", kwargs={"pk": self.pk})
    

class RegularService(models.Model):
    name = models.CharField(_("name"), max_length=250)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    about = models.TextField(_("about"), max_length=10000, default='', blank=True)

    class Meta:
        verbose_name = _("regular service")
        verbose_name_plural = _("regular services")

    def __str__(self):
        return f"{self.name} {self.price} {self.about}"


class CustomService(models.Model):
    custom_text = models.TextField(_("custom_text"), max_length=500, default='', blank=True)
    custom_img = models.ImageField(_("custom_img"), upload_to='custom_img', null=True, blank=True)
    instrument = models.ForeignKey(
        Instrument, 
        verbose_name=_("instrument"), 
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("custom service")
        verbose_name_plural = _("custom services")

    def __str__(self):
        return f"Custom Service: {self.custom_text}"
    

SERVICEORDER_STATUS = (
    (0, _("Confirmed")),
    (1, _("Completed")),
    (2, _("Cancelled")),
)


class ServiceOrder(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        verbose_name=_("doctor"),
        on_delete=models.CASCADE,
        related_name="jobs",
        null=True,
        blank=True,
    )
    regular_service = models.ForeignKey(
        RegularService,
        verbose_name=_("regular service"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    custom_service = models.ForeignKey(
        CustomService,
        verbose_name=_("custom service"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    instrument = models.ForeignKey(
        Instrument,
        verbose_name=_("instrument"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        User,
        verbose_name=_("customer"),
        on_delete=models.CASCADE,
        related_name="service_orders",
    )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=SERVICEORDER_STATUS,
        default=0,
    )
    created_at = models.DateTimeField(_("created_at"), auto_now=False, auto_now_add=True)


class ServiceReview(models.Model):
    service = models.ForeignKey(
        RegularService, 
        verbose_name=_("service"), 
        on_delete=models.CASCADE,
        related_name="service_reviews",
        blank=True, null=True
    )
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.CASCADE,
        related_name='barber_reviews',
    )
    content = models.TextField(_("content"), max_length=4000, blank=True, null=True)
    created_at = models.DateTimeField(
        _("created at"), 
        auto_now_add=True, 
        db_index=True
    )

    class Meta:
        verbose_name = _("service review")
        verbose_name_plural = _("service reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service} review by {self.reviewer}"

    def get_absolute_url(self):
        return reverse("servicereview_detail", kwargs={"pk": self.pk})


class AboutUs(models.Model):
    content = HTMLField(_("content"), blank=True, null=True)

    class Meta:
        verbose_name = _("about us")
        verbose_name_plural = _("about us")

    def __str__(self):
        return f"{self.content}"

    def get_absolute_url(self):
        return reverse("aboutus_detail", kwargs={"pk": self.pk})
    

class Album(models.Model):
    title = models.CharField(_("title"), max_length=250)
    artist = models.CharField(_("artist"), max_length=250)
    cover = models.ImageField(_("cover"), upload_to='album_covers', null=True, blank=True)

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")

    def __str__(self) -> str:
        return f"{self.artist} - '{self.title}'"
    
    def get_absolute_url(self):
        return reverse("album_detail", kwargs={"pk": self.pk})
    

class AlbumReview(models.Model):
    album = models.ForeignKey(
        Album, 
        verbose_name=_("album"), 
        on_delete=models.CASCADE,
        related_name='album_reviews',
    )
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.CASCADE,
        related_name='album_reviews',
    )
    content = models.TextField(_("content"), max_length=4000, blank=True, null=True)
    created_at = models.DateTimeField(
        _("created at"), 
        auto_now_add=True, 
        db_index=True
    )

    class Meta:
        verbose_name = _("album review")
        verbose_name_plural = _("album reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.album} review by {self.reviewer}"

    def get_absolute_url(self):
        return reverse("albumreview_detail", kwargs={"pk": self.pk})
