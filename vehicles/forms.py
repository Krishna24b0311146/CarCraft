import re
from django import forms
from django.utils import timezone

from .models import ServiceBooking, Vehicle


class VehicleListingForm(forms.ModelForm):
	class Meta:
		model = Vehicle
		fields = [
			'name',
			'brand',
			'color',
			'registration_number',
			'kilometers',
			'price',
			'year',
			'fuel_type',
			'image',
			'seller_name',
			'seller_phone',
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	def clean_price(self):
		price = self.cleaned_data.get('price')
		if price is not None and price <= 0:
			raise forms.ValidationError('Price must be greater than zero.')
		return price

	def clean_year(self):
		year = self.cleaned_data.get('year')
		current_year = timezone.localdate().year
		if year is not None and (year < 1900 or year > current_year + 1):
			raise forms.ValidationError(f'Please enter a valid model year between 1900 and {current_year + 1}.')
		return year

	def clean_seller_phone(self):
		phone = self.cleaned_data.get('seller_phone')
		if phone:
			cleaned = re.sub(r'[\s\-\(\)]', '', str(phone))
			if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
				raise forms.ValidationError('Enter a valid 10-15 digit phone number.')
			return cleaned
		return phone


class ServiceBookingForm(forms.ModelForm):
	class Meta:
		model = ServiceBooking
		fields = [
			'customer_name',
			'phone',
			'car_model',
			'registration_number',
			'service_type',
			'preferred_date',
			'preferred_time',
			'notes',
		]
		widgets = {
			'preferred_date': forms.DateInput(attrs={'type': 'date'}),
			'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
			'notes': forms.Textarea(attrs={'rows': 3}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
		self.fields['preferred_date'].widget.attrs['min'] = timezone.localdate().isoformat()

	def clean_preferred_date(self):
		preferred_date = self.cleaned_data['preferred_date']
		if preferred_date < timezone.localdate():
			raise forms.ValidationError('Choose today or a future date.')
		return preferred_date

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if phone:
			cleaned = re.sub(r'[\s\-\(\)]', '', str(phone))
			if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
				raise forms.ValidationError('Enter a valid 10-15 digit phone number.')
			return cleaned
		return phone

