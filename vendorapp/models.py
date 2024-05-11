import datetime
from xml.dom import ValidationErr
import django
from email.policy import default
from django.db import models
import random
from simple_history.models import HistoricalRecords

class Vendor(models.Model):
    vendor_email = models.EmailField(max_length=40, unique=True)
    name = models.CharField(max_length=30)
    contact_details = models.TextField(max_length=10)
    address = models.TextField(max_length=250)
    vendor_code  = models.AutoField(primary_key=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True) 
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.vendor_email
    
class PurchaseOrder(models.Model):
    status_choices = (
        ('PENDING', 'PENDING'),
        ('CANCELLED', 'CANCELLED'),
        ('COMPLETED', 'COMPLETED'),
    ) 
    po_number = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, )
    order_date = models.DateField(null=False)
    delivery_date = models.DateField(null=False)
    items =models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20,null=True, choices=status_choices)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateField(default=datetime.datetime.now().date())
    acknowledgment_date = models.DateField(blank=True, null=True)
    delivered_date = models.DateField(blank=True, null=True)


class HistoricalPerformance(models.Model):
    vendor  = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date =  models.DateField(default=datetime.datetime.now().date())
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)
