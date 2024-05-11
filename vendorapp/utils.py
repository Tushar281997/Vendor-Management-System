from django.db.models import Count, Avg, ExpressionWrapper, F, IntegerField
from .models import PurchaseOrder, Vendor

def calculate_on_time_delivery_rate(vendor_id):
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='COMPLETED')
    total_completed_pos = completed_pos.count()
    on_time_pos = completed_pos.filter(delivery_date__lte=F('delivered_date'))
    on_time_count = on_time_pos.count()
    if total_completed_pos > 0:
        return on_time_count / total_completed_pos
    else:
        return 0

def calculate_quality_rating_average(vendor_id):
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='COMPLETED')
    return completed_pos.aggregate(quality_rating_avg=Avg('quality_rating'))['quality_rating_avg']

def calculate_average_response_time(vendor_id):
    vendor_id =1
    pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, acknowledgment_date__isnull=False)
    response_times = pos.annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=IntegerField()))
    milliseconds = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
    if not milliseconds:
        return milliseconds
    days = milliseconds / (1000000 * 60 * 60 * 24)
    return days

    return 
def calculate_fulfilment_rate(vendor_id):
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='COMPLETED')
    fulfilled_pos = completed_pos.filter(quality_rating__isnull=True)
    total_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    if total_pos.count() > 0:
        return fulfilled_pos.count() / total_pos.count()
    else:
        return 0