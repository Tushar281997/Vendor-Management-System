from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_on_time_delivery_rate, calculate_quality_rating_average, calculate_average_response_time, calculate_fulfilment_rate

# Create your views here.

class VendorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for managing YourModel instances.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "on_time_delivery_rate": calculate_on_time_delivery_rate(vendor_id),
            "quality_rating_avg": calculate_quality_rating_average(vendor_id),
            "average_response_time": calculate_average_response_time(vendor_id),
            "fulfilment_rate": calculate_fulfilment_rate(vendor_id)
        }
        return Response(data)

class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        acknowledgment_date = request.data.get('acknowledgment_date')
        if acknowledgment_date is None:
            return Response({"error": "Acknowledgment date is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            po = PurchaseOrder.objects.get(pk=po_id)
            po.acknowledgment_date = acknowledgment_date
            po.save()
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_404_NOT_FOUND)

        # Recalculate average_response_time
        vendor_id = po.vendor_id
        vendor = Vendor.objects.get(pk=vendor_id)
        average_response_time = calculate_average_response_time(vendor_id)
        print (f"printing average_response_time {average_response_time}")
        vendor.average_response_time = average_response_time
        vendor.save()

        return Response({"message": "Purchase Order acknowledged successfully"})
    
class DeliveredPurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        delivered_date = request.data.get('delivered_date')
        quality_rating = request.data.get('quality_rating')
        order_status = request.data.get('status')
        if delivered_date is None:
            return Response({"error": "delivered_date is required"}, status=status.HTTP_400_BAD_REQUEST)
        if quality_rating is None:
            return Response({"error": "quality_rating is required"}, status=status.HTTP_400_BAD_REQUEST)
        if order_status is None:
            return Response({"error": "order_status is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            po = PurchaseOrder.objects.get(pk=po_id)
            po.status = str(status)
            po.delivered_date = delivered_date
            po.quality_rating = quality_rating
            po.save()
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_404_NOT_FOUND)

        # Recalculate average_response_time
        vendor_id = po.vendor_id
        vendor = Vendor.objects.get(pk=vendor_id)

        HistoricalPerformance.objects.create(vendor=vendor,
                                            average_response_time=vendor.average_response_time,
                                            quality_rating_avg=vendor.quality_rating_avg,
                                            on_time_delivery_rate=vendor.on_time_delivery_rate,
                                            fulfillment_rate=vendor.fulfillment_rate)
        vendor.average_response_time = calculate_on_time_delivery_rate(vendor_id)

        vendor.quality_rating_avg = calculate_quality_rating_average(vendor_id)

        vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor_id)

        vendor.fulfillment_rate = calculate_fulfilment_rate(vendor_id)
        vendor.save()

        return Response({"message": "Purchase Order Delivered successfully"})
    