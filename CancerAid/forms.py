from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django import forms

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['status','discount']

class MedicineForm(ModelForm):
	class Meta:
		model = Medicine
		fields = ['name','price','category']


class PyForm(ModelForm):
	class Meta:
		model = Ord
		fields = ['status']

class CreateForm(ModelForm):
	class Meta:
		model = Order
		fields = ['medicine']

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ['topic','name','description','more']

class UserForm(ModelForm):
	class Meta:
		model = Patient
		fields = ['name','fname','lname','email']

class DrForm(ModelForm):
	class Meta:
		model = Doctor
		fields = ['name','title','specialist','office','available']

		widgets = {
		   'name' : forms.TextInput(attrs ={'class': 'form-control'}),
           'title' : forms.TextInput(attrs ={'class': 'form-control'}),
		   'specialist' : forms.TextInput(attrs ={'class': 'form-control' }),
		   'office' : forms.TextInput(attrs ={'class': 'form-control'}),
		   'available' : forms.TextInput(attrs ={'class': 'form-control'}),
		}

class DoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = '__all__'

		widgets = {
           'user' : forms.Select(attrs ={'class': 'form-control' }),
		   'name' : forms.TextInput(attrs ={'class': 'form-control' }),
		   'title' : forms.TextInput(attrs ={'class': 'form-control' }),
		   'specialist' : forms.Select(attrs ={'class': 'form-control' }),
		   'office' : forms.TextInput(attrs ={'class': 'form-control' }),
		   'available' : forms.TextInput(attrs ={'class': 'form-control' }),
		}

class BForm(forms.ModelForm):
	class Meta:
		model = BkashPayment
		fields = ['name','address','option','medicine_name_and_quentity','bkashNumber','bkashTransaction','financial_support']

		widgets = {
		   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name here' }),
		   'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your current address here' }),
		   'option': forms.Select(attrs={'class': 'form-control' }),
		   'medicine_name_and_quentity': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your medicine name and quentity here or leave it blank' }),
		   'bkashNumber' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your bkash number here' }),
		   'bkashTransaction' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your transaction ID here' }),
		   'financial_support': forms.Select(attrs={'class': 'form-control' }),
		}

class FSForm(forms.ModelForm):
	class Meta:
		model = FS
		fields = ['name','phone','reason_why_you_need_this']

		widgets = {
		   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name here' }),
		   'phone' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your phone number here' }),
		   'reason_why_you_need_this' : forms.Textarea(attrs ={'class': 'form-control', 'placeholder':'Write proper reason here' }),
		}

class Ord1Form(ModelForm):
	class Meta:
		model = Ord
		fields = ['reply']

		widgets = {
           'reply' : forms.Textarea(attrs ={'class': 'form-control', 'placeholder':'Write your answer here'}),
		}


class AmbuForm(ModelForm):
	class Meta:
		model = Ambudetails
		fields = ['current_address','district','hospital','contact_no']

		widgets = {
		   'current_address' : forms.TextInput(attrs ={'class': 'form-control'}),
           'district' : forms.Select(attrs ={'class': 'form-control'}),
		   'hospital' : forms.Select(attrs ={'class': 'form-control' }),
		   'contact_no' : forms.TextInput(attrs ={'class': 'form-control','placeholder':'Write your contect number here'}),
		}

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['hospital'].queryset = Hospital.objects.none()

			if 'district' in self.data:  #If address is request.POST
				try:
					district_id = int(self.data.get('district')) #Fetch Address ID
					self.fields['hospital'].queryset = Hospital.objects.filter(district_id=district_id).order_by('name')
				except (ValueError, TypeError):
					pass  # invalid input from the client; ignore and fallback to empty City queryset
			elif self.instance.pk:
				self.fields['hospital'].queryset = self.instance.district.hospital_set.all()

	

