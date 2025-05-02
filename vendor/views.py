from django.shortcuts import render

def vendorProfile(request):
    return render(request, 'vendor/vendorProfile.html')
