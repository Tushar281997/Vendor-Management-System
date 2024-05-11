
import django
django.setup()

import requests
import pytest
from datetime import datetime, timedelta
from .models import PurchaseOrder, Vendor


LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = "8000"

@pytest.mark.django_db
def test_acknowledge_purchase_order_api_view():
    vendor = Vendor.objects.create(vendor_email="test@gmail.com",
                                    name="Test user",
                                    address="MH, In",
                                    contact_details="7768898098"
                                    )

    # Create a sample Purchase Order
    po = PurchaseOrder.objects.create(
        order_date = datetime.now(),
        delivery_date= datetime.now() + timedelta(days=1),
        items = {"bat":"2"},
        quality_rating = 5,
        vendor_id=vendor.vendor_code
    )
    ack_url = f"http://{LOCAL_HOST}:{LOCAL_PORT}/api/purchase_orders/{po.po_number}/acknowledge/"
    acknowledgment_date = datetime.now().date()

    data = {'acknowledgment_date': acknowledgment_date}

    response = requests.post(ack_url,data)
    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Refresh the PurchaseOrder object from the database to get the updated acknowledgment_date
    po.refresh_from_db()
    # Check that the acknowledgment_date has been updated
    assert po.acknowledgment_date == acknowledgment_date
    # po.delete()
    vendor.delete()

