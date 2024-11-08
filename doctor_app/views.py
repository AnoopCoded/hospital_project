from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from my_app.models import *
from doctor_app.forms import *
from my_app.forms import *
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import date
from django.db import transaction


#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_doctor(request.user):
        accountapproval= doctorDetails.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor_dashboard')
        else:
           pass
    elif is_patient(request.user):
        
            return redirect('patient_profile')



@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = patient.medical_histories.all()
    treatment_plans = patient.treatment_plans.all()
    
    return render(request, 'doctors/patient_detail.html', {
        'patient': patient,
        'medical_histories': medical_histories,
        'treatment_plans': treatment_plans,
    })

@login_required
def add_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        condition = request.POST['condition']
        date_diagnosed = request.POST['date_diagnosed']
        notes = request.POST.get('notes', '')
        MedicalHistory.objects.create(patient=patient, condition=condition, date_diagnosed=date_diagnosed, notes=notes)
        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'doctors/add_medical_history.html', {'patient': patient})

@login_required
def add_treatment_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        treatment_description = request.POST['treatment_description']
        start_date = request.POST['start_date']
        end_date = request.POST.get('end_date', None)
        doctor_notes = request.POST.get('doctor_notes', '')
        TreatmentPlan.objects.create(patient=patient, treatment_description=treatment_description, start_date=start_date, end_date=end_date, doctor_notes=doctor_notes)
        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'doctors/add_treatment_plan.html', {'patient': patient})

#doctors Registration
def register_doctor(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        doctor_form = DoctorRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Hash the password
            user.save()
            
            doctor = doctor_form.save(commit=False)
            doctor.user = user  # Associate doctor with the user
            doctor.save()
            
            login(request, user)  # Log in the user after registration
            return redirect('loginDoc')  # Change to your doctor dashboard URL
    else:
        user_form = UserRegistrationForm()
        doctor_form = DoctorRegistrationForm()

    return render(request, 'doctors/register_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                # Try to get the doctor profile associated with the user
                doctor = doctorDetails.objects.get(user=user)

                # If a doctor profile exists for the user, redirect to the doctor dashboard
                return redirect('doctor_dashboard')
            except doctorDetails.DoesNotExist:
                # If no doctor profile is found for the user
                messages.error(request, 'No doctor profile found for this user.')
                return redirect('loginDoc')
        else:
            messages.info(request, 'Please provide correct details!')
            return redirect('loginDoc')

    return render(request, "doctors/Doctorslogin.html")
    
     
@login_required
def doctor_dashboard(request):
    
    
    doctor = get_object_or_404(doctorDetails, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
    appointcount= Appointment.objects.all().filter(doctor=doctor).count()
    patientcount= Patient.objects.all().filter(doctor=doctor).count()
    mydict={
        'doctor': doctor,
        'appointments':appointments,
        'appointcount':appointcount,
        'patientcount': patientcount,
    }
    return render(request, 'doctors/doctor_dashboard.html', mydict)

#------Doctors Patient view----------------


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    prescriptions = patient.prescriptions.all()
    treatment_plans = patient.treatment_plans.all()
    medical_histories = patient.medical_histories.all()
    
    return render(request, 'doctors/patientfulldetail.html', {
        'patient': patient,
        'prescriptions': prescriptions,
        'treatment_plans': treatment_plans,
        'medical_histories': medical_histories,
    })

def create_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST, prefix='prescription')
        medical_history_form = MedicalHistoryForm(request.POST, prefix='medical_history')
        treatment_plan_form = TreatmentPlanForm(request.POST, prefix='treatment_plan')

        if prescription_form.is_valid() and medical_history_form.is_valid() and treatment_plan_form.is_valid():
            # Save Prescription
            prescription = prescription_form.save(commit=False)
            prescription.patient = patient
            prescription.prescribed_date = date.today()
            prescription.save()

            # Save Medical History
            medical_history = medical_history_form.save(commit=False)
            medical_history.patient = patient
            medical_history.save()

            # Save Treatment Plan
            treatment_plan = treatment_plan_form.save(commit=False)
            treatment_plan.patient = patient
            treatment_plan.save()

            return redirect('patient_detail', patient_id=patient.id)
    else:
        prescription_form = PrescriptionForm(prefix='prescription')
        medical_history_form = MedicalHistoryForm(prefix='medical_history')
        treatment_plan_form = TreatmentPlanForm(prefix='treatment_plan')

    context = {
        'patient': patient,
        'prescription_form': prescription_form,
        'medical_history_form': medical_history_form,
        'treatment_plan_form': treatment_plan_form,
    }

    return render(request, 'doctors/create_prescription.html', context)
    

def doctor_patient_view(request):
    doctor = get_object_or_404(doctorDetails, user=request.user)
    patients = Patient.objects.filter(doctor=doctor)  # Retrieve patients linked to the doctor
    
    context = {
        'doctor': doctor,
        'patients': patients  # Updated to use 'patients'
    }
    return render(request, 'doctors/doctor_view_patient.html', context)
    
def doctor_view_patient_view(request):
    return render(request,'doctors/doctor_view_patient.html')

def doctor_appointment_view(request):
    doctor = get_object_or_404(doctorDetails, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date')
    mydict={
        'doctor': doctor,
        'appointments':appointments
    }
    return render(request,'doctors/doctor_view_appointment.html',mydict)



class doctor_AppointmentDeleteView(View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, 'doctors/doctor_delete_appointment.html', {'appointment': appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect('doctor-appointment')

def delete_appointment_view(request):
    return render(request,'doctors/delete_appointment.html')






#-------------------------------------------------
# --------------Admin Module----------------------
#-------------------------------------------------

def admin_signup_view(request):
    form = AdminSigupForm()
    if request.method == 'POST':
        form = AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)  # Set the password hash (important for security)
            user.save()

            # Create or get the 'ADMIN' group
            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')

            # Add the user to the ADMIN group
            my_admin_group.user_set.add(user)

            # Optionally, you can assign more permissions to the group
            # my_admin_group.permissions.add(some_permission)

            # Redirect to login page after successful signup
            return redirect('adminlogin')  # Change 'adminlogin' to the name of your admin login URL

    return render(request, 'admin/adminsignup.html', {'form': form})

def adminLogin(request):
    if request.method == 'POST' :
            username =  request.POST.get('username')
            password= request.POST.get('password')
            user= authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff: 
                    login (request, user)
                    return redirect('admin_dashboard')
                else:
                    messages.info(request, 'You are not authorized to access this page.')
                    return redirect('adminLogin')
            else:
                messages.info(request, 'please provide correct details !')
                return redirect('adminLogin')
    return render(request,"admin/adminlogin.html")

def adminDashboard(request):
    doctors= doctorDetails.objects.all().order_by('-id')
    patients= Patient.objects.all().order_by('-id')

    doctorcount=doctorDetails.objects.all().count()
    patientcount=Patient.objects.all().count()
    appointcount= Appointment.objects.all().count()

    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount' : doctorcount,
    'patientcount':patientcount,
    'appointcount':appointcount,
    }
    return render(request,"admin/adminDashboard.html", mydict)


#------------admin appoinment------------

def appoinmentDetails(request):
    appointcount= Appointment.objects.all().count()
    return render(request, "admin/appoinmentDetails.html",{"appointcount":appointcount})
class AppointmentListView(View):
    def get(self, request):
        appointments = Appointment.objects.all().order_by('date')
        return render(request, 'admin/appointment_list.html', {'appointments': appointments})

class AppointmentCreateView(View):
    def get(self, request):
        form = Appointment_Form()
        return render(request, 'admin/appointment_form.html', {'form': form})

    def post(self, request):
        form = Appointment_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        return render(request, 'admin/appointment_form.html', {'form': form})

class AppointmentUpdateView(View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = Appointment_Form(instance=appointment)
        return render(request, 'admin/appointment_form.html', {'form': form})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = Appointment_Form(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        return render(request, 'admin/appointment_form.html', {'form': form})

class AppointmentDeleteView(View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, 'admin/appointment_confirm_delete.html', {'appointment': appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect('appointment_list')
    
    #--------------------end appointment-------------


def patientManagement(request):
    patientcount=Patient.objects.all().count()
    return render(request,'admin/admin_patient.html',{'patientcount':patientcount} )

#-----admin-doctor--------
def doctorManagement(request):
    return render(request,'admin/admin_doctor.html')

def doctor_record(request):
    doctor= doctorDetails.objects.all()
    return render(request,'admin/doctor_record.html', {'doctor':doctor})

def doctor_update(request, doctor_id, username):
    # Retrieve the User instance or raise a 404 error if not found
    user_instance = get_object_or_404(User, username=username)
    # Retrieve the DoctorDetails instance or raise a 404 error if not found
    doctor = get_object_or_404(doctorDetails, id=doctor_id)

    if request.method == 'POST':
        # Get form data from the POST request
        doc_spec = request.POST.get('doc_spec')
        dept_name = request.POST.get('dept_name')  
        dep_image = request.POST.get('dep_image')  
        availability = request.POST.get('availability')

        # Update the doctorDetails instance
        doctor.user = user_instance
        doctor.doc_spec = doc_spec
        doctor.dept_name = dept_name
        doctor.dep_image = dep_image
        doctor.availability = availability

        # Save the updated instance
        doctor.save()

        return redirect("doctor_record")  # Adjust redirect as needed

    return render(request, 'admin/doctor_update.html', {"doctor": doctor})

def doctor_delete(request):
    return render(request, 'admin/doctor_delete.html')


#----------------admin patient--------------
def patient_record(request):
    patient= Patient.objects.all()
    patientbill=PatientBill.objects.all()
    return render(request,'doctors/patient_record.html', {'patient':patient, "patientbill":patientbill})

def patient_update(request, patient_id, username):
    # Retrieve the User instance or raise a 404 error if not found
    user_instance = get_object_or_404(User, username=username)
    # Retrieve the Patient instance or raise a 404 error if not found
    patient = get_object_or_404(Patient, id=patient_id)
    doctors = doctorDetails.objects.all()  # Fetch all doctors
    if request.method == 'POST':
        # Get form data from the POST request
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        doctor_id = request.POST.get('doctor')  # Assuming this is the doctor's ID
        medical_history = request.POST.get('medical_history')

        # Update the patient instance
        patient.user = user_instance
        patient.date_of_birth = date_of_birth
        patient.phone_number = phone_number
        patient.address = address
        patient.medical_history = medical_history

        # Update the doctor field if a doctor is selected
        if doctor_id:
            doctor_instance = get_object_or_404(doctorDetails, id=doctor_id)  # Fetch doctor instance
            patient.doctor = doctor_instance
        else:
            patient.doctor = None  # Clear the doctor if no doctor is selected

        # Save the updated instance
        patient.save()

        return redirect("patient_record")  # Adjust redirect as needed


    return render(request, 'patient/patient_update.html', {"patient": patient, 'doctors': doctors})

def patient_delete(request,patient_id):
    patient=Patient.objects.get(id=patient_id)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('patient_record')
def patient_bill(request):
    patient = get_object_or_404(Patient, user=request.user)
    patientbill = PatientBill.objects.all()
    
    return render(request, 'patient/patient_bill.html', {'patient': patient,"patientbill": patientbill,})
#---admin patient bill--------
@login_required
def patient_bills(request, patient_id):
    bills = PatientBill.objects.filter(id=patient_id)
    return render(request, 'billing/patient_bills.html', {'bills': bills})

# View a single bill




@login_required
def create_bill(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = PatientBillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.save()
            return redirect('patient_bills', patient_id=patient.id)
    else:
        form = PatientBillForm()
    
    return render(request, 'billing/create_bill.html', {'form': form, 'patient': patient})
    
    



#------------------billing------------------

# billing with insurance details ***
def billing_patient_view(request,pk):
     # Get the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)

    # Get the patient's insurance information (if it exists)
    insurance = Insurance.objects.filter(patient=patient).first()

    # Creating a dictionary for patient details
    patientDict = {
        'patientId': pk,
        'user': patient.user,  # Accessing user from the single patient instance
        'phonenumber': patient.phone_number,
        'address': patient.address,
        'doctor_name': patient.doctor.user if patient.doctor else "No doctor assigned",
        'medical_history': patient.medical_history,
        'DateOfBirth': patient.date_of_birth,
        'insurance': insurance,  # Add the insurance details to the context
    }

    # If it's a POST request, process the bill calculation and save
    if request.method == 'POST':
        try:
            # Retrieve the POST data for charges and validate it
            room_charge = int(request.POST['roomCharge'])
            doctor_fee = int(request.POST['doctorFee'])
            medicine_cost = int(request.POST['medicineCost'])
            other_charge = int(request.POST['OtherCharge'])

            # Calculate the total
            total = room_charge + doctor_fee + medicine_cost + other_charge

            # Update the patientDict with fee details
            feeDict = {
                'roomCharge': room_charge,
                'doctorFee': doctor_fee,
                'medicineCost': medicine_cost,
                'OtherCharge': other_charge,
                'total': total
            }
            patientDict.update(feeDict)

            # If insurance exists, apply it
            if insurance:
                patientDict['insurance_coverage'] = insurance.coverage_details
                # Assume 80% coverage for simplicity, you can change the logic to reflect the actual coverage
                total_due_after_insurance = total * 0.20  # 80% is covered by insurance
            else:
                total_due_after_insurance = total

            # Create and save the PatientBill instance
            pB = PatientBill()
            pB.patient = patient
            pB.doctor_name = patient.doctor.user if patient.doctor else "No doctor assigned"
            pB.medicineCost = medicine_cost
            pB.roomCharge = room_charge
            pB.doctorFee = doctor_fee
            pB.OtherCharge = other_charge
            pB.total = total
            pB.amount_due = total_due_after_insurance  # Update the amount_due after applying insurance
            pB.insurance = insurance  # Associate the bill with insurance (if any)
            pB.save()

            # Render the final bill page with all the patient and bill details
            return render(request, 'patient/patient_final_bill.html', context=patientDict)
        
        except KeyError as e:
            # Handle missing fields in POST request
            return HttpResponseBadRequest(f"Missing parameter: {e}")
        except ValueError as e:
            # Handle non-integer values in POST data
            return HttpResponseBadRequest(f"Invalid data provided: {e}")

    # If it's a GET request, just show the generate bill form
    return render(request, 'patient/patient_generate_bill.html', context=patientDict)

#--------admin-bill view------------
def view_all_patient_bills(request):
    # Retrieve all patient bills from the database
    patient_bills = PatientBill.objects.all().select_related('patient', 'insurance')

    for bill in patient_bills:
        print(f'Bill for patient {bill.patient.user}: Paid = {bill.paid}')


    # Prepare context for rendering
    context = {
        'patient_bills': patient_bills
    }
    
    return render(request, 'admin/billing/view_patient_bills.html', context)

        
  
#payment
#-----------patient bill view-------------

# bill details**
def bill_detail(request, bill_id):
    # Fetch the patient's bill by ID
    patient_bill = get_object_or_404(PatientBill, id=bill_id)
    # Render the bill details to the user
    return render(request, 'billing/bill_detail.html', {'patient_bill': patient_bill})

#make payment admin **
def make_payment(request, bill_id):
    # Fetch the patient's bill by ID
    patient_bill = get_object_or_404(PatientBill, id=bill_id)

    if patient_bill.paid:
        messages.error(request, "This bill is already fully paid.")
        return redirect('bill_detail', bill_id=bill_id)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, initial={'amount_due': patient_bill.amount_due})
        if payment_form.is_valid():
            amount = payment_form.cleaned_data['amount']
            if amount <= 0:
                messages.error(request, "Payment amount must be greater than zero.")
                return redirect('bill_detail', bill_id=bill_id)

            with transaction.atomic():
                patient_bill.make_payment(amount)
                messages.success(request, f"Payment of {amount} has been processed.")
                return redirect('bill_detail', bill_id=bill_id)
        else:
            # Handle form validation errors
            print(payment_form.errors)
            messages.error(request, "There was an error with your payment form.")
            return redirect('bill_detail', bill_id=bill_id)
    else:
        payment_form = PaymentForm(initial={'amount_due': patient_bill.amount_due})

    return render(request, 'billing/make_payment.html', {
        'patient_bill': patient_bill,
        'payment_form': payment_form
    })
#pharmacy
def pharmacy_prescribtion_view(request):
    prescriptions=Prescription.objects.all()

    prescribcount=Prescription.objects.all().count()
    return render(request,"admin/ph_precrib_view.html",{"prescribcount":prescribcount, "prescriptions":prescriptions})

    
