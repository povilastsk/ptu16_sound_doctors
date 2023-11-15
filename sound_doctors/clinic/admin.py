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

class RegularServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "about")
    search_fields = ("name", )
    list_filter = ("name", )

class CustomServiceAdmin(admin.ModelAdmin):
    list_display = ("custom_text", )

class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("doctor", "regular_service", "customer", "status", "created_at")
    search_fields = ("doctor__last_name", "service__name", "customer__username")
    list_filter = ("doctor__specialization", "status")
    readonly_fields = ("id", )


@admin.register(models.ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("service", "reviewer", "created_at")
    list_display_links = ("created_at", )


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("content", )

class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")
    search_fields = ("title", "artist")
    list_filter = ("title", "artist")

class AlbumSaleAdmin(admin.ModelAdmin):
    list_display = ("get_album_title", "get_album_artist", "status")
    search_fields = ("album__title", "album__artist")
    list_filter = ("album__title", "album__artist")

    def get_album_title(self, obj):
        return obj.album.title

    def get_album_artist(self, obj):
        return obj.album.artist

    get_album_title.short_description = 'Album Title'
    get_album_artist.short_description = 'Album Artist'


admin.site.register(models.Instrument, InstrumentAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.RegularService, RegularServiceAdmin)
admin.site.register(models.CustomService, CustomServiceAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.AboutUs, AboutUsAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.AlbumSale, AlbumSaleAdmin)