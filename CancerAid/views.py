from django.shortcuts import render,redirect, HttpResponse
from .models import *
from datetime import datetime
from .forms import *
from django.forms import inlineformset_factory
from .filters import *
from .decorators import *
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.


@unauthenticated_user
def handleSignUp(request):

          if request.method=="POST":
               # Get the post parameters
               username=request.POST['username']
               email=request.POST['email']
               fname=request.POST['fname']
               lname=request.POST['lname']
               pass1=request.POST['pass1']
               pass2=request.POST['pass2']

               # check for errorneous input
               if len(username)<5:
                    messages.error(request, " Your user name must be under 5 characters")
                    return redirect('homepage')

               if not username.isalnum():
                    messages.error(request, " User name should only contain letters and numbers")
                    return redirect('/')
               if (pass1!= pass2):
                    messages.error(request, " Passwords do not match, try again please")
                    return redirect('/')
               
               # Create the user
               if User.objects.filter(username=username).first():
                         messages.error(request, "This username is already taken, try another for example: username123")
                         return redirect('/')

               myuser = User.objects.create_user(username,email,pass1)
               myuser.first_name= fname
               myuser.last_name= lname
               myuser.save()

               g = Group.objects.get(name='patient')
               users = User.objects.filter(username=username)
               for u in users:
                g.user_set.add(u)

                Patient.objects.create(
				user=myuser,
				name=myuser.username,
				email=myuser.email,
                fname=myuser.first_name,
                lname=myuser.last_name,
				)

               messages.success(request, " Your account has been successfully created")
               return redirect('/')
        
          else:
               return HttpResponse("404 - Not found")

@unauthenticated_user
def handeLogin(request):

          if request.method=="POST":
               # Get the post parameters
               loginusername=request.POST['loginusername']
               loginpassword=request.POST['loginpassword']

               user=authenticate(username= loginusername, password= loginpassword)
               if user is not None:
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return render(request, 'index.html')
               else:
                    messages.error(request, "Invalid credentials! Please try again")
                    return redirect("/")

          return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def homepage(request):
    return render(request,'index.html')

def medicinepage(request):
    
    q = request.GET.get('q') if request.GET.get('q')!= None else ''

    medicine = Medicine.objects.filter(name__icontains=q)

    myFilter = MedicineFilter(request.GET,queryset=medicine)
    medicine = myFilter.qs

    context={'medicine':medicine,'myFilter':myFilter}
    return render(request,'medicine.html',context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def dashboardpage(request):
    order = Order.objects.all()
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()

    t_p = patient.count()
    t_o = order.count()

    req = order.filter(status = 'pending').count()
    acc = order.filter(status = 'delivered').count()

    myFilter = OrderFilter(request.GET,queryset=order)
    order = myFilter.qs

    a = {'order': order, 'patient':patient,'t_p' : t_p, 't_o' : t_o, 'req':req, 'acc':acc,'myFilter':myFilter,'doctor':doctor}
    
    return render(request,'dashboard.html',a)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def patientpage(request,pk):
    patient = Patient.objects.get(id=pk)
    orders = patient.order_set.all()
    order_count = orders.count()
    
    b={'patient':patient,'orders':orders,'order_count':order_count}
    return render(request,"patient.html",b)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','patient','manager'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Patient, Order, fields=('medicine',))
	patient = Patient.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=patient)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=patient)
		if formset.is_valid():
			formset.save()
			return redirect(request.META.get('HTTP_REFERER'))

	context = {'form':formset}
	return render(request, 'order1_form.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')

	context = {'form':form}
	return render(request, 'order_form.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','patient','manager'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'delete.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['patient'])
#This page is for Patient
def userpage(request):

     user = request.user.patient
     form = UserForm(instance=user)

     ord = request.user.patient.ord_set.all()
     orders = request.user.patient.order_set.all()
     total_orders = orders.count()
     delivered = orders.filter(status='delivered').count()
     pending = orders.filter(status='pending').count()

     if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()

     context = {'orders':orders, 'total_orders':total_orders,'delivered':delivered,'pending':pending,'form':form,'ord':ord}
     return render(request, 'user.html', context)

def doctorpage(request):
    doctor = Doctor.objects.all()
    myFilter = DoctorFilter(request.GET,queryset=doctor)
    doctor = myFilter.qs

    context={'doctor':doctor,'myFilter':myFilter}
    return render(request,'doctor.html',context)

def contect(request):
    if request.method == "POST":
     name = request.POST.get('name')
     email = request.POST.get('email')
     phone = request.POST.get('phone')
     desc = request.POST.get('desc')
     contect= Contect(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
     contect.save()
     messages.success(request, 'Your message has been sent')
     
    return render(request, 'contect.html')

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def comments(request):
     c = Contect.objects.all()
     a = Ambudetails.objects.all()
     b = BkashPayment.objects.all()
     f = FS.objects.all()
     context = {'c':c,'a':a,'b':b,'f':f}

     return render(request, 'comments.html',context)

def Lung(request):
    return render(request,'Lungcancer.html')

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def AddMedicine(request):
    if request.method == "POST":
     name = request.POST.get('name')
     price = request.POST.get('price')
     category = request.POST.get('CATEGORY')
     AddMedicine= Medicine(name=name,price=price,category=category)
     AddMedicine.save()
     messages.success(request, 'Medicine successfully added')

    medicine = Medicine.objects.all()
    context={'medicine':medicine}
     
    return render(request, 'addmedicine.html',context)


def discussion_topicpage(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''

    topic = DiscussionTopic.objects.all()
    room = Discussion.objects.filter(topic__name__icontains=q)
    context={'room':room,'topic':topic}
    return render(request, 'discussion_topic.html',context)


def discussion(request,pk):
    room = Discussion.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('discussion', pk=room.id)

    context={'room':room, 'room_messages':room_messages,'participants': participants}
    return render(request, 'discussion.html',context)

@login_required(login_url='homepage')
def createDiscussion(request):
    form = DiscussionForm()
    topics = DiscussionTopic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = DiscussionTopic.objects.get_or_create(name=topic_name)
        Discussion.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            more=request.POST.get('more')
        )
        return redirect('/discussion_topic')

    context = {'form': form,'topics':topics}
    return render(request, 'discussion_form.html', context)

def updateDiscussion(request, pk):
    room = Discussion.objects.get(id=pk)
    form = DiscussionForm(instance=room)
    topics = DiscussionTopic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = DiscussionTopic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.more = request.POST.get('more')
        room.save()
        return redirect('/discussion_topic')

    context = {'form': form,'topics': topics,'room':room}
    return render(request, 'discussion_form.html', context)

def deleteDiscussion(request, pk):
    room = Discussion.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('/discussion_topic')
    return render(request, 'delete1.html', {'obj': room})

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('/discussion_topic')
    return render(request, 'delete1.html', {'obj': message})

def addambu(request):
    a= Ambudetails.objects.all()
    form = AmbuForm()

    if request.method == 'POST':
        form = AmbuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Your information is Recorded")
    else:
        form=AmbuForm()

    context={'form':form,'a':a}
    return render(request, 'ambu.html', context)

def ambuupdate(request, pk):
    ambu = Ambudetails.objects.get(id=pk)
    form = AmbuForm(instance=ambu)
    if request.method == 'POST':
        form = AmbuForm(request.POST, instance=ambu)
        if form.is_valid():
            form.save()
            messages.success(request, " Your information is Updated")
            return redirect('/ambu')
    context = {'form':form}
    return render(request, 'order2_form.html', context)

def load_hospitals(request):
    district_id = request.GET.get('district_id') #It will fetch that address id.It comes from ajax.
    hospitals = Hospital.objects.filter(district_id=district_id) #Filter the hospitals based on the address.
    return render(request, 'hospital_dropdown_list_options.html', {'hospitals': hospitals}) #After Rendering this HTML page, It will send response back to where it is being called 


@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','patient','manager'])
def createOrd(request, pk):
	OrderFormSet = inlineformset_factory(Patient, Ord, fields=('patient','doctor','problem'), extra=1, can_delete=False)
	doctor = Patient.objects.get(id=pk)
	formset = OrderFormSet(queryset=Ord.objects.none(),instance=doctor)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=doctor)
		if formset.is_valid():
			formset.save()
			return redirect(request.META.get('HTTP_REFERER'))

	context = {'form':formset}
	return render(request, 'order2_form.html', context)
 
@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])   
def doctorSignUp(request):

          if request.method=="POST":
               # Get the post parameters
               username=request.POST['username']
               email=request.POST['email']
               pass1=request.POST['pass1']
               pass2=request.POST['pass2']

               # check for errorneous input
               if len(username)<5:
                    messages.error(request, " Your user name must be under 5 characters")
                    return redirect('homepage')

               if not username.isalnum():
                    messages.error(request, " User name should only contain letters and numbers")
                    return redirect('/')
               if (pass1!= pass2):
                    messages.error(request, " Passwords do not match, try again please")
                    return redirect('/')
               
               # Create the user
               if User.objects.filter(username=username).first():
                         messages.error(request, "This username is already taken, try another for example: username123")
                         return redirect('/')

               myuser = User.objects.create_user(username,email,pass1)
               myuser.save()

               b = Group.objects.get(name='doctor')
               users = User.objects.filter(username=username)
               for u in users:
                b.user_set.add(u)

                Doctor.objects.create(
				user=myuser,
				name=myuser.username,
				)

               messages.success(request, " Your account has been successfully created")
               return redirect('/')

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['doctor'])  
def doctoruserpage(request):
     user = request.user.doctor
     form = DrForm(instance=user)

     if request.method == 'POST':
        form = DrForm(request.POST,instance=user)
        if form.is_valid():
            form.save()

     ord = request.user.doctor.ord_set.all()
     context = {'ord':ord,'form':form}
     return render(request, 'doctorsite.html', context)

#doctor can change his message
@login_required(login_url='homepage')
@allowed_users(allowed_roles=['doctor'])  
def updateOrd(request, pk):

	ord = Ord.objects.get(id=pk)
	form = Ord1Form(instance=ord)

	if request.method == 'POST':
		form = Ord1Form(request.POST, instance=ord)
		if form.is_valid():
			form.save()
			return redirect('/doctorsite')

	context = {'form':form,'ord':ord}
	return render(request, 'order3_form.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def addDoctor(request):
    form = DoctorForm()

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor successfully added")
    else:
        form=DoctorForm()

    doctor = Doctor.objects.all()
    myFilter = DoctorFilter(request.GET,queryset=doctor)
    doctor = myFilter.qs

    context={'form':form,'doctor':doctor,'myFilter':myFilter}
    return render(request, 'adddoctor.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['patient'])  
def PatientRecordpage(request):
     ord = request.user.patient.ord_set.all()
     context = {'ord':ord}
     return render(request, 'PatientRecord.html', context)

def payment(request):
    form = BForm()

    if request.method == 'POST':
        form = BForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=BForm()

    context={'form':form,}
    return render(request, 'bkashpayment.html', context)

def Stomach(request):
    return render(request,'Stomach Cancer.html')
    
def Bladder(request):
    return render(request,'Bladder Cancer.html')

def Breast(request):
    return render(request,'Breast Cancer.html')

def Liver(request):
    return render(request,'Liver Cancer.html')

def Ovarian(request):
    return render(request,'Ovarian Cancer.html')

def About(request):
    return render(request,'about.html')

def Videos(request):
    video = Item.objects.all()

    return render(request,'videos.html',{'video':video})

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def manager(request):

    return render(request,'manager.html')

def FSpage(request):
    form = FSForm()

    if request.method == 'POST':
        form = FSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Your information is save, we will notify you later")
    else:
        form=FSForm()

    context={'form':form,}
    return render(request, 'FS.html', context)



@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def updateMedicine(request, pk):

	medicine = Medicine.objects.get(id=pk)
	form = MedicineForm(instance=medicine)

	if request.method == 'POST':
		form = MedicineForm(request.POST, instance=medicine)
		if form.is_valid():
			form.save()
			return redirect('/addmedicine')

	context = {'form':form}
	return render(request, 'order_form.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','patient','manager'])
def deleteMedicine(request, pk):
	medicine = Medicine.objects.get(id=pk) 
	if request.method == "POST":
		medicine.delete()
		return redirect('/addmedicine')

	context = {'item':medicine}
	return render(request, 'delete.html', context)



@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def updateDoctorInfo(request, pk):

	dr = Doctor.objects.get(id=pk)
	form = DrForm(instance=dr)

	if request.method == 'POST':
		form = DrForm(request.POST, instance=dr)
		if form.is_valid():
			form.save()
			return redirect('/adddoctor')

	context = {'form':form}
	return render(request, 'order_form.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','patient','manager'])
def deleteDoctorInfo(request, pk):
	dr = Doctor.objects.get(id=pk) 
	if request.method == "POST":
		dr.delete()
		return redirect('/adddoctor')

	context = {'item':dr}
	return render(request, 'delete.html', context)

@login_required(login_url='homepage')
@allowed_users(allowed_roles=['admin','manager'])
def updatePayStatus(request, pk):

	py = Ord.objects.get(id=pk)
	form = PyForm(instance=py)

	if request.method == 'POST':
		form = PyForm(request.POST, instance=py)
		if form.is_valid():
			form.save()
			return redirect('/comments')

	context = {'form':form}
	return render(request, 'order_form.html', context)
