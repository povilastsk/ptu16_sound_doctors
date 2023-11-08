from django.contrib import admin
from . import models


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "damage_text", "damage_img")
    search_fields = ("name", "type")
    list_filter = ("name", )


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "specialization")
    search_fields = ("last_name", "specialization")
    list_filter = ("specialization", )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "about")
    search_fields = ("name", )
    list_filter = ("name", )


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("doctor", "service", "customer", "status", "created_at")
    search_fields = ("doctor__last_name", "service__name", "customer__username")
    list_filter = ("doctor__specialization", "status")
    readonly_fields = ("id", )


@admin.register(models.ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("doctor", "reviewer", "created_at")
    list_display_links = ("created_at", )


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("content", )



admin.site.register(models.Instrument, InstrumentAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.AboutUs, AboutUsAdmin)