import uuid
from django.db import models
from django.contrib.auth.models import User

#Departmentts
class Department(models.Model):
    dep_name=models.CharField(max_length=100)
    dep_description= models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.dep_name}"  
    
#doctors details
class doctorDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doc_spec = models.CharField(max_length=255)
    dept_name = models.ForeignKey(Department, on_delete= models.CASCADE)    
    dep_image = models.ImageField(upload_to='doctors')
    availability = models.TextField()
    def __str__(self):
        return f"{self.user.username} - {self.doc_spec}"

#patient registration
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',  # Default is 'Other', you can change this as needed
    )
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    doctor = models.ForeignKey(doctorDetails, on_delete=models.SET_NULL, null=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}"
  #booking appointment
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE)
    date = models.DateField()
    booked_on=models.DateField(auto_now= True)
    reason = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.date}"

#billing
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    

#-------Health Resources------------


class HealthTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EducationalMaterial(models.Model):
    MATERIAL_TYPES = [
        ('article', 'Article'),
        ('infographic', 'Infographic'),
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('exercise_plan', 'Exercise Plan'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    material_type = models.CharField(choices=MATERIAL_TYPES, max_length=20, default= 'PDF')
    file = models.FileField(upload_to='materials')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

