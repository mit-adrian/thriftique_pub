from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from menu.forms import CategoryForm, ProductItemForm
from orders.models import Order, OrderedFood
from .forms import VendorForm, OpeningHoursForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import OpeningHour, Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import CategoryModel, ProductModel
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendorProfile')
    else:
        profile_form = UserProfileForm(instance= profile)
        vendor_form = VendorForm(instance= vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }

    return render(request, 'vendor/vendorProfile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = CategoryModel.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,

    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def productitems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(CategoryModel, pk=pk)
    product_items = ProductModel.objects.filter(vendor=vendor, category=category)
    context = {
        'product_items': product_items,
        'category': category,
    }
    return render(request, 'vendor/productitems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {
        'form': form,
        
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(CategoryModel, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
        
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(CategoryModel, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted succesfully!')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_item(request):
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES)
        if form.is_valid():
            productTitle = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(productTitle)
            form.save()
            messages.success(request, 'Product/Item added successfully!')
            return redirect('productitems_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductItemForm()
        # modifying the product form 
        form.fields['category'].queryset = CategoryModel.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_item.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
    product = get_object_or_404(ProductModel, pk=pk)
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            productTitle = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(productTitle)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('productitems_by_category', product.category.id)
        else:
            print(form.errors)
    else:
        form = ProductItemForm(instance=product)
        form.fields['category'].queryset = CategoryModel.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'product': product,
        
    }
    return render(request, 'vendor/edit_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request, pk=None):
    product = get_object_or_404(ProductModel, pk=pk)
    product.delete()
    messages.success(request, 'Product/Item has been deleted succesfully!')
    return redirect('productitems_by_category', product.category.id)



def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHoursForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)

def add_opening_hours(request):
    # handle the data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid request')


def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})
        

        
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = OrderedFood.objects.filter(order=order, product_item__vendor=get_vendor(request))

        context = {
            'order': order,
            'ordered_food': ordered_product,
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'tax_data': order.get_total_by_vendor()['tax_dict'],
            'grand_total': order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')
    
    return render(request, 'vendor/order_detail.html', context)

def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'vendor/my_orders.html', context)