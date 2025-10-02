from django.contrib import admin
from django.template.response import TemplateResponse

from kinoSamochodowe.models import Screening, Film, Venue, FilmImage, VenueImage, Ticket


class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 1


class VenueAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_at")
    inlines = [VenueImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # nowy obiekt
            obj.user = request.user
        obj.editor = request.user
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excludes = super().get_exclude(request, obj) or []
        return excludes + ["user", "editor"]


class FilmImageInline(admin.TabularInline):
    model = FilmImage
    extra = 1


class FilmAdmin(admin.ModelAdmin):
    inlines = [FilmImageInline]
    readonly_fields = ("user", "created_at")

    def save_model(self, request, obj, form, change): # zapis usera który dokonuje dodania/edycji zamiast domyślnego wyboru
        if not obj.pk:
            obj.user = request.user
        obj.editor = request.user
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excludes = super().get_exclude(request, obj) or []
        return excludes + ["user", "editor"]


class ScreeningAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_at")

    def get_exclude(self, request, obj=None):
        excludes = super().get_exclude(request, obj) or []
        return excludes + ["user", "editor"]

    def save_model(self, request, obj, form, change):
        is_new = not obj.pk
        if is_new:
            obj.user = request.user
        obj.editor = request.user
        super().save_model(request, obj, form, change)
        if is_new:
            parking_spot_count = obj.venue.parking_spot_count
            tickets = [Ticket(screening=obj, parking_spot_number=i) for i in range(1, parking_spot_count + 1)]
            Ticket.objects.bulk_create(tickets)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        screening = Screening.objects.get(id=object_id)
        tickets = Ticket.objects.filter(screening=screening)

        rows = []
        total = len(tickets)
        for i, item in enumerate(tickets, start=1):
            page = (i + 9) // 10
            missing_cells = range((10 - (i % 10)) % 10)
            rows.append({
                "item": item,
                "counter": i,
                "page": page,
                "is_last": i == total,
                "missing_cells": missing_cells,
            })

        extra_context["screening"] = screening
        extra_context["tickets"] = tickets
        extra_context["rows"] = rows
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Venue, VenueAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Screening, ScreeningAdmin)
