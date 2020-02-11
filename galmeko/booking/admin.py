from django.contrib import admin
from .forms import BookingCreationForm
from booking.forms import CustomStopCreationForm,CustomBookingFeatureCreationForm,CustomBookingFeatureChangeForm,BookingChangeForm
from django.utils.html import format_html
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site
from booking.models import Booking,BookingStop,BookingFeature
from django.template.defaultfilters import truncatechars  # or truncatewords
from setting.models import Vehicle,VehicleCategory

class StopInline(admin.TabularInline):
    extra = 1
    model = BookingStop
    form = CustomStopCreationForm

class BookingFeatureInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular_booking_feature.html'
    extra = 1
    max_num=1
    model = BookingFeature
    form = CustomBookingFeatureChangeForm
    add_form = CustomBookingFeatureCreationForm

class BookingAdmin(admin.ModelAdmin):
    inlines = [
        StopInline,BookingFeatureInline
    ]
    js = ("booking/js/booking.js",)
    form = BookingCreationForm
    form = BookingChangeForm
    add_form = BookingCreationForm
    model = Booking
    list_display = ('booking_type', 'source', 'destination','fare','round_trip','vehicle_id')
    list_filter = ('round_trip',)
    list_per_page = 5
    search_fields = ('booking_type',)
    ordering = ('-id',)

    def source(self, obj):
        return truncatechars(obj.origin,30)
    source.short_description = "Source"

    def destination(self, obj):
        return truncatechars(obj.origin,30)
    source.short_description = "Destination"

    def vehicle_id(self, obj):
        vehicleDetail = Vehicle.objects.get(id=obj.vehicle_id)
        return vehicleDetail.vehicle_no
    vehicle_id.short_description = "Vehicle_Number"

admin_site.register(Booking, BookingAdmin)
