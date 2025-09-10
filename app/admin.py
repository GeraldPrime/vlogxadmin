from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .firebase_service import FirebaseService

firebase_service = FirebaseService()

# Custom Admin Views for Firebase Data
def drivers_admin_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        driver_id = request.POST.get('driver_id')
        
        if action == 'delete' and driver_id:
            success = firebase_service.delete_driver(driver_id)
            if success:
                messages.success(request, f'Driver {driver_id} deleted successfully')
            else:
                messages.error(request, f'Failed to delete driver {driver_id}')
    
    drivers = firebase_service.get_all_drivers()
    context = {
        'drivers': drivers,
        'title': 'Manage Drivers'
    }
    return render(request, 'admin/drivers_list.html', context)

def customers_admin_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')
        
        if action == 'delete' and customer_id:
            success = firebase_service.delete_customer(customer_id)
            if success:
                messages.success(request, f'Customer {customer_id} deleted successfully')
            else:
                messages.error(request, f'Failed to delete customer {customer_id}')
    
    customers = firebase_service.get_all_customers()
    context = {
        'customers': customers,
        'title': 'Manage Customers'
    }
    return render(request, 'admin/customers_list.html', context)

def analytics_admin_view(request):
    driver_stats = firebase_service.get_drivers_stats()
    customer_stats = firebase_service.get_customers_stats()
    
    context = {
        'driver_stats': driver_stats,
        'customer_stats': customer_stats,
        'title': 'Analytics Dashboard'
    }
    return render(request, 'admin/analytics.html', context)