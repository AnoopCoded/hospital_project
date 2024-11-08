from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from my_app.models import *
from my_app.forms import DateInput
from doctor_app.models import *



#for admin signup
class AdminSigupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields to display in the form

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = doctorDetails
        fields = ['doc_spec', 'dept_name', 'dep_image', 'availability']

class Appointment_Form(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'reason']

        widgets = {
            'date' : DateInput(),
        }

#payment form**
class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Amount to Pay"
    )

    def clean_amount(self):
        # You can validate here if necessary (e.g., amount must be less than or equal to the amount_due)
        amount_due = self.initial.get('amount_due', 0)
        amount = self.cleaned_data['amount']
        if amount > amount_due:
            raise forms.ValidationError(f"Payment cannot exceed the amount due: {amount_due}")
        return amount

#------------


class PatientBillForm(forms.ModelForm):
    class Meta:
        model = PatientBill
        fields = ['doctor_name', 'roomCharge', 'medicineCost', 'doctorFee', 'OtherCharge']
