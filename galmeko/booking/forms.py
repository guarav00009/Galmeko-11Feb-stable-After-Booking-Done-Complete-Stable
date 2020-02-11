from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from booking.models import Booking,BookingStop,BookingFeature
from setting.models import Features
from user.models import User
from setting.models import Vehicle,VehicleCategory

class BookingCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingCreationForm, self).__init__(*args, **kwargs)
        self.fields['origin_geocode'].widget = forms.HiddenInput()
        self.fields['destination_geocode'].widget = forms.HiddenInput()
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status=1)
        self.fields['category'].queryset = VehicleCategory.objects.filter(status=1)
        if self.is_bound == True:
            if(self.data['booking_type']):
                booking_type = self.data['booking_type']
                Users = User.objects.filter(type = booking_type).filter(status = 1)
                Select = [(i.id, i.first_name) for i in Users]
                self.fields['user'].choices = Select
            else:
                pass
        else:
            self.fields['user'].choices = ''
    class Meta:
        model = Booking
        fields = ('booking_type', 'user','vehicle','category','origin', 'origin_geocode','destination','destination_geocode','booking_msg','round_trip','fare')
        widgets = {
            'booking_msg': forms.Textarea(attrs={'cols': 33, 'rows': 2}),
        }

class BookingChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingChangeForm, self).__init__(*args, **kwargs)
        self.fields['origin_geocode'].widget = forms.HiddenInput()
        self.fields['destination_geocode'].widget = forms.HiddenInput()
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status=1)
        self.fields['category'].queryset = VehicleCategory.objects.filter(status=1)
        if(self.initial.get('booking_type')):
            booking_type = self.initial.get('booking_type')
            Users = User.objects.filter(type = booking_type).filter(status = 1)
            Select = [(i.id, i.first_name + ' ' + i.last_name) for i in Users]
            self.fields['user'].choices = Select
        else:
            pass
    class Meta:
        model = Booking
        fields = ('booking_type', 'user','vehicle','category','origin', 'origin_geocode','destination','destination_geocode','booking_msg','round_trip','fare')
        widgets = {
            'booking_msg': forms.Textarea(attrs={'cols': 33, 'rows': 2}),
        }

class CustomStopCreationForm(forms.ModelForm):
    class Meta:
        model = BookingStop
        fields = ['name', 'phone','address']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 83, 'rows': 1.7}),
        }
        
class CustomBookingFeatureCreationForm(forms.ModelForm):
    def my_choices():
        value = Features.objects.values()
        features = []
        for feature in value:
            features.append([feature['id'], feature['name']])
        return features
    
    feature = forms.MultipleChoiceField(choices=my_choices, widget=forms.SelectMultiple())
    class Meta:
        model = BookingFeature
        fields = ['feature']

class CustomBookingFeatureChangeForm(forms.ModelForm):
    class Meta:
        model = BookingFeature
        fields = ['feature']