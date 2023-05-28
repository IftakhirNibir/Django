import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):

	class Meta:
		model = Order
		fields = ['patient','medicine','status']

class MedicineFilter(django_filters.FilterSet):

	class Meta:
		model = Medicine
		fields = ['category']

class DoctorFilter(django_filters.FilterSet):

	class Meta:
		model = Doctor
		fields = ['specialist']
	