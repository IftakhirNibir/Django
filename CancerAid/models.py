from django.db import models
from django.contrib.auth.models import  User
from django.db.models.fields import DateTimeField
from embed_video.fields import EmbedVideoField
# Create your models here.


class Patient(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	fname = models.CharField(max_length=200, null=True)
	lname = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)


	def __str__(self):
		return str(self.name) if self.name else ''

class Medicine(models.Model):
	CATEGORY = (
			('Foreign', 'Foreign'),
			('Local', 'Local'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)


	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('pending', 'pending'),
			('delivered', 'delivered'),
			)

	Discount = (
		('You will get 30 percent discount' ,'You will get 30 percent discount'),
		('You will get 50 percent discount', 'You will get 50 percent discount'),
		('You will get 70 percent discount', 'You will get 70 percent discount'),
		('Sorry there is no discount for you', 'Sorry there is no discount for you')
	)

	patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
	medicine = models.ForeignKey(Medicine, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	discount = models.CharField(max_length=200, null=True, choices=Discount)
	
	def __str__(self):
		return str(self.medicine.name) if self.medicine.name else ''
		
class Doctor(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	SPECIALIST = (
			('Lung_Cancer_specialist', 'Lung_Cancer_specialist'),
			('Stomach_Cancer_specialist', 'Stomach_Cancer_specialist'),
			('Liver_Cancer_specialist', 'Liver_Cancer_specialist'),
			) 

	name = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	specialist = models.CharField(max_length=200, null=True, choices=SPECIALIST)
	office = models.CharField(max_length=200, null=True)
	available= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Contect(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name

class DiscussionTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Discussion(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    more = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    participants =models.ManyToManyField(User, related_name="participants", blank=True)

    def __str__(self):
        return self.name

    class Meta:
       ordering = ['-updated', '-created']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


class District(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name)

class Hospital(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name)

class Ambudetails(models.Model):
	current_address = models.CharField(max_length=200, null=True,auto_created=True)
	district = models.ForeignKey(District, null=True, on_delete= models.SET_NULL)
	hospital = models.ForeignKey(Hospital, null=True, on_delete= models.SET_NULL)
	contact_no = models.CharField(max_length=200)

class Ord(models.Model):
	STATUS = (
			('paid', 'paid'),
			('unpaid', 'unpaid'),
			)

	patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
	doctor = models.ForeignKey(Doctor, null=True, on_delete= models.SET_NULL)
	problem = models.TextField()
	reply = models.TextField(null=True)
	posting_time = models.DateTimeField(auto_now_add=True,null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

class BkashPayment(models.Model):
	OPTION = (
			('Donation', 'Donation'),
			('Doctor Visit Cost', 'Doctor Visit Cost'),
			('Medicine Bill', 'Medicine Bill'),
			('Ambulance Cost', 'Ambulance Cost'),
			)

	FH = (
		('Yes I Have','Yes I have'),
		('No I dont need','No I dont need'),
	)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, blank=True)
	option = models.CharField(max_length=200, choices=OPTION)
	medicine_name_and_quentity = models.CharField(max_length=100, null=True, blank=True)
	bkashNumber = models.CharField(max_length=20)
	bkashTransaction = models.CharField(max_length=512)
	financial_support = models.CharField(max_length=200, choices=FH)
	created_time = models.DateTimeField(auto_now_add=True,null=True)


class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()

class FS(models.Model):
    name = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    reason_why_you_need_this = models.TextField()

    def __str__(self) -> str:
        return self.name
