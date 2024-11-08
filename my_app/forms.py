from django import forms
from django.contrib.auth.models import User

from doctor_app.models import *
from .models import *

#date picker function
class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['gender','date_of_birth','phone_number','doctor','medical_history']
        widgets = {
            'date_of_birth' : DateInput(),
        }

#appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'reason']

        widgets = {
            'date' : DateInput(),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'doctor_notes']
        
    medication_name = forms.CharField(label='Medication Name', max_length=200, required=True)
    dosage = forms.CharField(label='Dosage', max_length=100, required=True)
    doctor_notes = forms.CharField(label='Doctor Notes', widget=forms.Textarea, required=False)

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['condition', 'date_diagnosed', 'notes']

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ['treatment_description', 'start_date', 'end_date', 'doctor_notes']

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


#  form for health educational resources for admin

class HealthTipForm(forms.ModelForm):
    class Meta:
        model = HealthTip
        fields = ['title', 'content']

class EducationalMaterialForm(forms.ModelForm):
    class Meta:
        model = EducationalMaterial
        fields = ['title', 'description','material_type','file']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'link']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dep_name', 'dep_description']