from rest_framework import serializers
from .models import PurchaseOrder, Vendor, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Vendor
        fields = '__all__'
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(format="%Y-%m-%d")
    delivery_date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
