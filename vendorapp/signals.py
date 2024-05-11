from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.db.models import F


@receiver(pre_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.pk is not None:  # Check if the instance is being updated
        old_instance = sender.objects.get(pk=instance.pk)
        if instance.status == 'COMPLETED' and old_instance.status != instance.status and old_instance.delivery_date <= instance.delivered_date:  # Check if status has changed
                vendor = instance.vendor  # Assuming Order model has a ForeignKey to Vendor
                total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
                on_time_orders = PurchaseOrder.objects.filter(
                    vendor=vendor,
                    status='COMPLETED',
                    delivery_date__lte=F("delivered_date"),
                ).count()
                if total_orders > 0:
                    vendor.on_time_delivery_rate = ((on_time_orders+1) / (total_orders+1)) * 100
                    vendor.save()