from django.http import HttpResponseRedirect
import django.utils.timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from doctor_app.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import PatientRegistrationForm, UserRegistrationForm, AppointmentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from my_app.forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView



#register
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        patient_form = PatientRegistrationForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        patient_form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'user_form': user_form, 'patient_form': patient_form})
#patientlogin
def login_view(request):
    if request.method == 'POST' :
            username =  request.POST.get('username')
            password= request.POST.get('password')
            user= authenticate(username=username, password=password)
            if user is not None:
                login (request, user)

                try:
                    patient = Patient.objects.get(user=user)
                    return redirect('patient_profile')
                except Patient.DoesNotExist:
                # If no doctor profile is found for the user
                    messages.error(request, 'No patient profile found for this user.')
                    return redirect('login')
            else:
                messages.info(request, 'please provide correct details !')
                return redirect('login')
    
    return render(request,'patient/login.html')

#profile
@login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    patientbill = PatientBill.objects.all()
    return render(request, 'patient/patient_view.html', {'patient': patient,"patientbill": patientbill})

#logout
def logout_view(request):
    logout(request)
    return redirect('login')

#appointment
@login_required
def schedule_appointment(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = get_object_or_404(Patient, user=request.user)
            appointment.save()
            return redirect('patient_profile')  # Redirect to profile or another page
    else:
        form = AppointmentForm()
    return render(request, 'schedule_appointment.html', {'form': form, "patient":patient})

#reschedule_appointment
@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('patient_profile')  # Redirect to patient profile or another page
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'reschedule_appointment.html', {'form': form, 'appointment': appointment})

#cancel_appointment
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('patient_profile')  # Redirect to patient profile or another page
    
    return render(request, 'cancel_appointment.html', {'appointment': appointment})




def home_view(request):
   
    return render(request,'index.html')
    
def about(request):
    return render(request,'about.html')

def doctors(request):
    dict_docs={
        "docs": doctorDetails.objects.all()
    }
    return render(request, 'doctors.html', dict_docs)
def contact(request):
    sub = ContactusForm()
    if request.method == 'POST':
        sub = ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    
    return render(request, 'contact.html',{'form':sub})

def department(request):
    dict_dept={
        "dept":Department.objects.all()
    }
    return render(request, 'department.html', dict_dept)

#---------Health Resources----------

def health_tips(request):
    tips = HealthTip.objects.all()
    return render(request, 'health/health_tips.html', {'tips': tips})

def educational_materials(request):
    materials = EducationalMaterial.objects.all()
    return render(request, 'health/educational_materials.html', {'materials': materials})

def resources(request):
    resources_list = Resource.objects.all()
    return render(request, 'health/resources.html', {'resources': resources_list})


#admin crud operation for health educational resources 
def ehrView(request):
    return render(request,'ehrmaterial/ehrview.html')

class HealthTipListView(ListView):
    model = HealthTip
    template_name = 'ehrmaterial/healthtip_list.html'
    context_object_name = 'health_tips'

class HealthTipCreateView(CreateView):
    model = HealthTip
    form_class = HealthTipForm
    template_name = 'ehrmaterial/healthtip_form.html'
    success_url = reverse_lazy('healthtip_list')

class HealthTipUpdateView(UpdateView):
    model = HealthTip
    form_class = HealthTipForm
    template_name = 'ehrmaterial/healthtip_form.html'
    success_url = reverse_lazy('healthtip_list')

class HealthTipDeleteView(DeleteView):
    model = HealthTip
    template_name = 'ehrmaterial/healthtip_confirm_delete.html'
    success_url = reverse_lazy('healthtip_list')

# EducationalMaterial Views
class EducationalMaterialListView(ListView):
    model = EducationalMaterial
    template_name = 'ehrmaterial/educationalmaterial_list.html'
    context_object_name = 'materials'

class EducationalMaterialCreateView(CreateView):
    model = EducationalMaterial
    form_class = EducationalMaterialForm
    template_name = 'ehrmaterial/educationalmaterial_form.html'
    success_url = reverse_lazy('educationalmaterial_list')

class EducationalMaterialUpdateView(UpdateView):
    model = EducationalMaterial
    form_class = EducationalMaterialForm
    template_name = 'ehrmaterial/educationalmaterial_form.html'
    success_url = reverse_lazy('educationalmaterial_list')

class EducationalMaterialDeleteView(DeleteView):
    model = EducationalMaterial
    template_name = 'ehrmaterial/educationalmaterial_confirm_delete.html'
    success_url = reverse_lazy('educationalmaterial_list')

# Resource Views
class ResourceListView(ListView):
    model = Resource
    template_name = 'ehrmaterial/resource_list.html'
    context_object_name = 'resources'

class ResourceCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'ehrmaterial/resource_form.html'
    success_url = reverse_lazy('resource_list')

class ResourceUpdateView(UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'ehrmaterial/resource_form.html'
    success_url = reverse_lazy('resource_list')

class ResourceDeleteView(DeleteView):
    model = Resource
    template_name = 'ehrmaterial/resource_confirm_delete.html'
    success_url = reverse_lazy('resource_list')


#--------admin department--------

def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully!")
            return redirect('department_list')  # Redirect to the list view
    else:
        form = DepartmentForm()
    return render(request, 'department/department_form.html', {'form': form})

# List Departments
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})

# Update Department
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')  # Redirect to the list view
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department/department_form.html', {'form': form})

# Delete Department
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')
    return render(request, 'department/department_confirm_delete.html', {'department': department})