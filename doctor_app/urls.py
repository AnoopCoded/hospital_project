from django.urls import path
from doctor_app.views import *
urlpatterns = [
    path('patient/<int:patient_id>/', patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/add-medical-history/', add_medical_history, name='add_medical_history'),
    path('patient/<int:patient_id>/add-treatment-plan/', add_treatment_plan, name='add_treatment_plan'),
    path('patient/patientbill/', patient_bill, name='patientbill'),
   



    #--------------------doctors----------------------------------
    path("doctors/register/", register_doctor, name= 'regdoctor'),
    path("doctors/login/", doctor_login, name= 'loginDoc'),
    path('doctors/doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    #----------------------doctors Panel------------------------

    path('doctor-patient', doctor_patient_view,name='doctor-patient'),
    path('doctor-appointment',doctor_appointment_view,name='doctor-appointment'),
    path('doctor-delete-appointment//<int:pk>',doctor_AppointmentDeleteView.as_view(),name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>',delete_appointment_view,name='delete-appointment'),

    path('doctor-dashboard/patient/<int:patient_id>/', patient_detail, name='doctor_patient_detail'),
    path('patient/<int:patient_id>/prescribe/', create_prescription, name='create_prescription'),


    #-----------
    #---admin---
    #-----------
     path('adminsignup', admin_signup_view, name="adminSignup"),
    path("adminPanel/adminLogin", adminLogin, name='adminLogin'),
    path("adminDashboard/", adminDashboard, name='admin_dashboard'),
    
    path("adminDashboard/admin_patient", patientManagement, name="admin_patient"),
    path("adminDashboard/admin_doctor", doctorManagement, name="admin_doctor"),
    path("adminDashboard/admin_doctor/doctor_record", doctor_record, name="doctor_record"),
    path("adminDashboard/admin_doctor/doctor_delete/", doctor_delete, name="doctor_delete"),
    path('doctor/update/<int:doctor_id>/<str:username>/', doctor_update, name='doctor_update'),


    path("adminDashboard/appointments", appoinmentDetails, name='appointment'),
    path('adminDashboard/appointment_list/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),

    path("admindashboard/Pharmacy/",pharmacy_prescribtion_view, name='precribtion_view'),

    path('patient-bills/',view_all_patient_bills, name='view_all_patient_bills'), 

     path('patient/discharge_patient/<int:pk>/', billing_patient_view, name='discharge_patient'),
    
     
    
    path("adminDashboard/admin_doctor/patient_record", patient_record, name="patient_record"),
    path("adminDashboard/admin_patient/patient_delete/<int:patient_id>/", patient_delete, name="patient_delete"),
    path('patient/update/<int:patient_id>/<str:username>/', patient_update, name='patient_update'),

    path('patient/bills/<int:patient_id>/', patient_bills, name='patient_bills'),

    
    
    path('patient/create_bill/<int:patient_id>',create_bill, name='create_bill'),

    path('bill/<int:bill_id>/', bill_detail, name='bill_detail'),
    path('bill/<int:bill_id>/pay/', make_payment, name='make_payment'),

]