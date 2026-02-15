from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer


@api_view(['GET'])
def public_vendor_list(request):
    vendors = Vendor.objects.filter(is_approved=True)
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)
