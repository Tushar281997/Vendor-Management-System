from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, VendorPerformanceAPIView, AcknowledgePurchaseOrderAPIView, DeliveredPurchaseOrderAPIView

# Create a router and register the ViewSet with it
router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='_vendor')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_order')



# The router generates the URL patterns for the ViewSet
urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge_purchase_order'),
    path('purchase_orders/<int:po_id>/Delivered/', DeliveredPurchaseOrderAPIView.as_view(), name='acknowledge_purchase_order'),
]