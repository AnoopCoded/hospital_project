from django.db import models
from django.forms import ValidationError
from my_app.models import *
from django.utils import timezone

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition = models.CharField(max_length=200)
    date_diagnosed = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.condition} - {self.patient}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_plans')
    treatment_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Treatment Plan for {self.patient}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    prescribed_date = models.DateField()
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient}: {self.medication_name}"
    
class Insurance(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    coverage_details = models.TextField()

    def __str__(self):
        return f"{self.provider_name} - {self.policy_number}"

class PatientBill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='PatientBill')
    doctor_name = models.CharField(max_length=100, null=True)
    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Track the total paid
    paid = models.BooleanField(default=False)
    insurance = models.ForeignKey(Insurance, null=True, blank=True, on_delete=models.SET_NULL)
    paid_date = models.DateTimeField( default=timezone.now)
    def save(self, *args, **kwargs):
        self.total = sum([
            getattr(self, 'medicineCost', 0),
            getattr(self, 'roomCharge', 0),
            getattr(self, 'doctorFee', 0),
            getattr(self, 'OtherCharge', 0)
        ])
        self.amount_due = self.total - self.total_paid  # Ensure amount_due reflects the unpaid amount
        super().save(*args, **kwargs)

    def make_payment(self, amount):
        """Handle payment and mark as paid if fully paid."""
        self.total_paid += amount
        if self.total_paid >= self.total:
            self.paid = True
        self.amount_due = self.total - self.total_paid
        self.save()

    def clean(self):
        if self.total < 0:
            raise ValidationError('Total cost cannot be negative.')
        if self.amount_due < 0:
            raise ValidationError('Amount due cannot be negative.')

    def __str__(self):
        return f"Bill for {self.patient.user} ({self.total})"






   
