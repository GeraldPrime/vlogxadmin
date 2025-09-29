from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .firebase_service import FirebaseService
import json
import logging

logger = logging.getLogger(__name__)
firebase_service = FirebaseService()

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('signin')
    
    return render(request, 'signin.html')

def signout_view(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def home(request):
    """Enhanced dashboard home page with comprehensive analytics"""
    try:
        # Get enhanced statistics
        driver_stats = firebase_service.get_driver_stats_enhanced()
        customer_stats = firebase_service.get_customers_stats()
        trip_analytics = firebase_service.get_trip_analytics()
        
        # Get recent orders for real-time updates
        recent_orders = firebase_service.get_all_trips(limit=10)
        
        # Get recent drivers and customers
        recent_drivers = firebase_service.get_all_drivers()[:5]
        recent_customers = firebase_service.get_all_customers()[:5]

        context = {
            'driver_stats': driver_stats,
            'customer_stats': customer_stats,
            'trip_analytics': trip_analytics,
            'recent_orders': recent_orders,
            'recent_drivers': recent_drivers,
            'recent_customers': recent_customers,
            'total_drivers': driver_stats.get('total_drivers', 0),
            'active_drivers': driver_stats.get('active_drivers', 0),
            'offline_drivers': driver_stats.get('offline_drivers', 0),
            'total_customers': customer_stats.get('total_customers', 0),
            'pending_drivers': driver_stats.get('pending_drivers', 0),
            'approved_drivers': driver_stats.get('approved_drivers', 0),
            'total_trips': trip_analytics.get('total_trips', 0),
            'completed_trips': trip_analytics.get('completed_trips', 0),
            'total_revenue': trip_analytics.get('total_revenue', 0),
            'completion_rate': trip_analytics.get('completion_rate', 0),
        }
        return render(request, "index.html", context)
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, "index.html", {
            'driver_stats': {},
            'customer_stats': {},
            'trip_analytics': {},
            'recent_orders': [],
            'recent_drivers': [],
            'recent_customers': [],
            'total_drivers': 0,
            'active_drivers': 0,
            'offline_drivers': 0,
            'total_customers': 0,
            'pending_drivers': 0,
            'approved_drivers': 0,
            'total_trips': 0,
            'completed_trips': 0,
            'total_revenue': 0,
            'completion_rate': 0,
        }) 


@login_required(login_url='signin')
def drivers_management(request):
    """Drivers management page"""
    try:
        drivers = firebase_service.get_all_drivers()
        context = {
            'drivers': drivers,
            'drivers_count': len(drivers),
            'active_drivers': len([d for d in drivers if d.get('isDriverOnline', False)]),
            'page_title': 'Driver Management'
        }
        return render(request, "drivers/drivers_list.html", context)
    except Exception as e:
        messages.error(request, f"Error loading drivers: {str(e)}")
        return render(request, "drivers/drivers_list.html", {'drivers': [], 'drivers_count': 0})

def customers_management(request):
    """Customers management page"""
    try:
        customers = firebase_service.get_all_customers()
        context = {
            'customers': customers,
            'customers_count': len(customers),
            'page_title': 'Customer Management'
        }
        return render(request, "customers/customers_list.html", context)
    except Exception as e:
        messages.error(request, f"Error loading customers: {str(e)}")
        return render(request, "customers/customers_list.html", {'customers': [], 'customers_count': 0})



def driver_detail(request, driver_id):
    """Driver detail page with comprehensive information including trips, ratings, balance, and analytics"""
    logger.info(f"Loading driver detail for driver_id: {driver_id}")
    try:
        driver = firebase_service.get_driver_by_id(driver_id)
        if not driver:
            messages.error(request, "Driver not found")
            return redirect('drivers_management')

        # Fetch driver documents
        driver_documents = firebase_service.get_driver_documents(driver_id)

        # Fetch vehicle
        vehicle = None
        vehicles_ref = firebase_service.db.collection('VehicleDetails').where('userID', '==', driver['id']).stream()
        for doc in vehicles_ref:
            vehicle_data = doc.to_dict()
            vehicle_data['id'] = doc.id
            vehicle = vehicle_data
            break
            
        # Fetch driver trips with enhanced data
        trips = firebase_service.get_driver_trips(driver_id)
        completed_trips = [trip for trip in trips if trip.get('status') in ['completed', 'ended', 'delivered']]
        ongoing_trips = [trip for trip in trips if trip.get('status') in ['pending', 'accepted', 'picked_up', 'in_progress']]
        cancelled_trips = [trip for trip in trips if trip.get('status') in ['cancelled', 'cancelled_by_driver', 'cancelled_by_customer']]
        
        # Fetch enhanced driver ratings with trip context
        ratings = firebase_service.get_driver_ratings(driver_id)
        rating_analytics = firebase_service.get_rating_analytics(driver_id)
        if not rating_analytics:
            rating_analytics = {
                'total_ratings': 0,
                'average_rating': 0,
                'rating_breakdown': {},
                'recent_ratings': []
            }
        
        # Fetch comprehensive earnings and balance info
        earnings_info = firebase_service.get_driver_earnings(driver_id)
        if not earnings_info:
            earnings_info = {
                'total_earnings': 0,
                'total_trips': 0,
                'avg_earnings_per_trip': 0,
                'current_balance': 0,
                'pending_amount': 0,
                'total_withdrawals': 0
            }
        balance_info = firebase_service.get_driver_balance(driver_id)
        
        # Fetch driver location
        location_info = firebase_service.get_driver_location(driver_id)
        
        # Debug logging
        logger.info(f"Driver {driver_id} data summary:")
        logger.info(f"  - Trips: {len(trips)}")
        logger.info(f"  - Ratings: {len(ratings)}")
        logger.info(f"  - Earnings: {earnings_info}")
        logger.info(f"  - Balance: {balance_info}")
        logger.info(f"  - Location: {location_info}")
        
        # Additional debugging for trips
        if trips:
            logger.info(f"  - Sample trip: {trips[0]}")
        else:
            logger.warning(f"  - No trips found for driver {driver_id}")
            
        # Additional debugging for ratings
        if ratings:
            logger.info(f"  - Sample rating: {ratings[0]}")
            logger.info(f"  - Rating analytics: {rating_analytics}")
        else:
            logger.warning(f"  - No ratings found for driver {driver_id}")
            logger.warning(f"  - Rating analytics: {rating_analytics}")
        
        # Get recent activity (last 10 trips)
        recent_trips = sorted(trips, key=lambda x: x.get('dateCreated', ''), reverse=True)[:10]

        context = {
            'driver': driver,
            'driver_documents': driver_documents,
            'vehicle': vehicle,
            'trips': trips,
            'completed_trips': completed_trips,
            'ongoing_trips': ongoing_trips,
            'cancelled_trips': cancelled_trips,
            'recent_trips': recent_trips,
            'trips_count': len(trips),
            'completed_trips_count': len(completed_trips),
            'ratings': ratings,
            'rating_analytics': rating_analytics,
            'ratings_count': len(ratings),
            'avg_rating': rating_analytics.get('average_rating', 0),
            'balance_info': balance_info,
            'earnings_info': earnings_info,
            'location_info': location_info,
            'page_title': f'Driver Details - {driver.get("firstName", "")} {driver.get("lastName", "")}'
        }
        return render(request, "drivers/driver_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading driver {driver_id}: {str(e)}")
        messages.error(request, f"Error loading driver: {str(e)}")
        return redirect('drivers_management')



def customer_detail(request, customer_id):
    """Customer detail page"""
    try:
        customer = firebase_service.get_customer_by_id(customer_id)
        if not customer:
            messages.error(request, "Customer not found")
            return redirect('customers_management')
        # Fetch location and orders
        customer_location = firebase_service.get_customer_location(customer_id)
        customer_trips = firebase_service.get_customer_trips(customer_id)

        # Group orders by status
        completed = [t for t in customer_trips if t.get('status') in ['completed', 'ended', 'delivered']]
        in_transit = [t for t in customer_trips if t.get('status') in ['accepted', 'picked_up', 'in_progress', 'started', 'ongoing']]
        pending = [t for t in customer_trips if t.get('status') in ['pending']]
        cancelled = [t for t in customer_trips if t.get('status') in ['cancelled', 'cancelled_by_driver', 'cancelled_by_customer']]

        context = {
            'customer': customer,
            'customer_location': customer_location,
            'customer_trips': customer_trips,
            'completed_trips': completed,
            'in_transit_trips': in_transit,
            'pending_trips': pending,
            'cancelled_trips': cancelled,
            'page_title': f'Customer Details - {customer.get("firstName", "")} {customer.get("lastName", "")}'
        }
        return render(request, "customers/customer_detail.html", context)
    except Exception as e:
        messages.error(request, f"Error loading customer: {str(e)}")
        return redirect('customers_management')

def customer_live_status(request, customer_id: str):
    """Return JSON with customer's current location for live tracking."""
    try:
        customer = firebase_service.get_customer_by_id(customer_id)
        if not customer:
            return JsonResponse({'success': False, 'message': 'Customer not found'}, status=404)
        location = firebase_service.get_customer_location(customer_id)
        return JsonResponse({
            'success': True,
            'customer': {
                'id': customer.get('id'),
                'firstName': customer.get('firstName'),
                'lastName': customer.get('lastName')
            },
            'location': location
        })
    except Exception as e:
        logger.error(f"customer_live_status error for {customer_id}: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

def update_driver_status(request):
    """AJAX endpoint to update driver status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            driver_id = data.get('driver_id')
            new_status = data.get('status')
            
            if not driver_id or new_status is None:
                return JsonResponse({'success': False, 'message': 'Missing required fields'})
            
            success = firebase_service.update_driver(driver_id, {'isApproved': new_status})
            
            if success:
                return JsonResponse({'success': True, 'message': 'Driver status updated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to update driver status'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def payment_modes(request):
    """Payment modes management page"""
    try:
        payment_modes = firebase_service.get_payment_modes()
        context = {
            'payment_modes': payment_modes,
            'page_title': 'Payment Modes Management'
        }
        return render(request, "payments/payment_modes.html", context)
    except Exception as e:
        logger.error(f"Error loading payment modes: {str(e)}")
        messages.error(request, f"Error loading payment modes: {str(e)}")
        return redirect('home')

def create_payment_mode(request):
    """Create new payment mode"""
    if request.method == 'POST':
        try:
            mode = request.POST.get('mode')
            status = request.POST.get('status', 'Active')
            
            if not mode:
                messages.error(request, "Payment mode is required")
                return redirect('payment_modes')
            
            data = {
                'mode': mode,
                'status': status
            }
            
            payment_mode_id = firebase_service.create_payment_mode(data)
            
            if payment_mode_id:
                messages.success(request, "Payment mode created successfully")
            else:
                messages.error(request, "Failed to create payment mode")
                
        except Exception as e:
            logger.error(f"Error creating payment mode: {str(e)}")
            messages.error(request, f"Error creating payment mode: {str(e)}")
            
    return redirect('payment_modes')

def update_payment_mode(request, payment_mode_id):
    """Update payment mode"""
    if request.method == 'POST':
        try:
            mode = request.POST.get('mode')
            status = request.POST.get('status', 'Active')
            
            if not mode:
                messages.error(request, "Payment mode is required")
                return redirect('payment_modes')
            
            data = {
                'mode': mode,
                'status': status
            }
            
            success = firebase_service.update_payment_mode(payment_mode_id, data)
            
            if success:
                messages.success(request, "Payment mode updated successfully")
            else:
                messages.error(request, "Failed to update payment mode")
                
        except Exception as e:
            logger.error(f"Error updating payment mode: {str(e)}")
            messages.error(request, f"Error updating payment mode: {str(e)}")
            
    return redirect('payment_modes')

def delete_payment_mode(request, payment_mode_id):
    """Delete payment mode"""
    if request.method == 'POST':
        try:
            success = firebase_service.delete_payment_mode(payment_mode_id)
            
            if success:
                messages.success(request, "Payment mode deleted successfully")
            else:
                messages.error(request, "Failed to delete payment mode")
                
        except Exception as e:
            logger.error(f"Error deleting payment mode: {str(e)}")
            messages.error(request, f"Error deleting payment mode: {str(e)}")
            
    return redirect('payment_modes')

# def payment_settings(request):
#     """Payment settings management page"""
#     try:
#         payment_settings = firebase_service.get_payment_settings()
#         vehicle_types = firebase_service.get_vehicle_types()
        
#         context = {
#             'payment_settings': payment_settings,
#             'vehicle_types': vehicle_types,
#             'page_title': 'Payment Settings Management'
#         }
#         return render(request, "payments/payment_settings.html", context)
#     except Exception as e:
#         logger.error(f"Error loading payment settings: {str(e)}")
#         messages.error(request, f"Error loading payment settings: {str(e)}")
#         return redirect('home')


def payment_settings(request):
    """Payment settings management page"""
    try:
        payment_settings = firebase_service.get_payment_settings()
        vehicle_types = firebase_service.get_vehicle_types()
        
        context = {
            'payment_settings': payment_settings,
            'vehicle_types': vehicle_types,
            'page_title': 'Payment Settings Management'
        }
        return render(request, "payments/payment_settings.html", context)
    except Exception as e:
        logger.error(f"Error loading payment settings: {str(e)}")
        messages.error(request, f"Error loading payment settings: {str(e)}")
        return redirect('home')


def create_payment_setting(request):
    """Create new payment setting"""
    if request.method == 'POST':
        try:
            vehicle_type = request.POST.get('vehicle_type')
            price_per_distance = request.POST.get('price_per_distance')
            add_on_fee = request.POST.get('add_on_fee')
            
            if not vehicle_type or not price_per_distance or not add_on_fee:
                messages.error(request, "All fields are required")
                return redirect('payment_settings')
            
            data = {
                'vehicleTypeId': vehicle_type,
                'pricePerDistance': str(price_per_distance),  # Store as string to match your DB
                'addOnFee': float(add_on_fee)  # Use correct field name from your DB
            }
            
            payment_setting_id = firebase_service.create_payment_setting(data)
            
            if payment_setting_id:
                messages.success(request, "Payment setting created successfully")
            else:
                messages.error(request, "Failed to create payment setting")
                
        except Exception as e:
            logger.error(f"Error creating payment setting: {str(e)}")
            messages.error(request, f"Error creating payment setting: {str(e)}")
            
    return redirect('payment_settings')

def update_payment_setting(request, payment_setting_id):
    """Update payment setting"""
    if request.method == 'POST':
        try:
            price_per_distance = request.POST.get('price_per_distance')
            add_on_fee = request.POST.get('add_on_fee')
            
            if not price_per_distance or not add_on_fee:
                messages.error(request, "All fields are required")
                return redirect('payment_settings')
            
            data = {
                'pricePerDistance': float(price_per_distance),
                'addOnFee': float(add_on_fee)
            }
            
            success = firebase_service.update_payment_setting(payment_setting_id, data)
            
            if success:
                messages.success(request, "Payment setting updated successfully")
            else:
                messages.error(request, "Failed to update payment setting")
                
        except Exception as e:
            logger.error(f"Error updating payment setting: {str(e)}")
            messages.error(request, f"Error updating payment setting: {str(e)}")
            
    return redirect('payment_settings')

def delete_payment_setting(request, setting_id):
    """Delete payment setting"""
    if request.method == 'POST':
        try:
            success = firebase_service.delete_payment_setting(setting_id)
            
            if success:
                messages.success(request, "Payment setting deleted successfully")
            else:
                messages.error(request, "Failed to delete payment setting")
                
        except Exception as e:
            logger.error(f"Error deleting payment setting: {str(e)}")
            messages.error(request, f"Error deleting payment setting: {str(e)}")
            
    return redirect('payment_settings')


def orders_management(request):
    try:
        status_filter = request.GET.get('status', None)
        trips = firebase_service.get_all_trips(limit=50, status=status_filter)
        
        # Calculate statistics
        pending_count = len([t for t in trips if t.get('status') == 'pending'])
        completed_count = len([t for t in trips if t.get('status') == 'ended'])
        total_revenue = sum(float(t.get('deliveryAmount', 0)) for t in trips if t.get('status') == 'ended')
        
        context = {
            'trips': trips,
            'status_filter': status_filter,
            'pending_count': pending_count,
            'completed_count': completed_count,
            'total_revenue': total_revenue,
            'page_title': 'Orders Management'
        }
        return render(request, "orders/orders_list.html", context)
    except Exception as e:
        logger.error(f"Error loading orders: {str(e)}")
        messages.error(request, f"Error loading orders: {str(e)}")
        return redirect('home')

def order_detail(request, order_id):
    """Order detail page with tracking information"""
    try:
        trip = firebase_service.get_trip_by_id(order_id)
        
        if not trip:
            messages.error(request, "Order not found")
            return redirect('orders_management')
        
        context = {
            'trip': trip,
            'page_title': f'Order #{order_id[:8]}'
        }
        return render(request, "orders/order_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading order details: {str(e)}")
        messages.error(request, f"Error loading order details: {str(e)}")
        return redirect('orders_management')

def update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        try:
            status = request.POST.get('status')
            
            if not status:
                messages.error(request, "Status is required")
                return redirect('order_detail', order_id=order_id)
            
            success = firebase_service.update_trip_status(order_id, status)
            
            if success:
                messages.success(request, "Order status updated successfully")
            else:
                messages.error(request, "Failed to update order status")
                
        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}")
            messages.error(request, f"Error updating order status: {str(e)}")
            
    return redirect('order_detail', order_id=order_id)

def vehicle_types(request):
    """Vehicle types management page"""
    try:
        vehicle_types = firebase_service.get_vehicle_types()
        
        context = {
            'vehicle_types': vehicle_types,
            'page_title': 'Vehicle Types Management'
        }
        return render(request, "vehicles/vehicle_types.html", context)
    except Exception as e:
        logger.error(f"Error loading vehicle types: {str(e)}")
        messages.error(request, f"Error loading vehicle types: {str(e)}")
        return redirect('home')

# def create_vehicle_type(request):
#     """Create new vehicle type"""
#     if request.method == 'POST':
#         try:
#             name = request.POST.get('name')
#             base_fare = request.POST.get('base_fare')
#             per_km_charge = request.POST.get('per_km_charge')
#             per_minute_charge = request.POST.get('per_minute_charge')
#             capacity = request.POST.get('capacity')
#             description = request.POST.get('description')
#             is_active = request.POST.get('is_active') == 'on'
            
#             if not name:
#                 messages.error(request, "Vehicle type name is required")
#                 return redirect('vehicle_types')
            
#             data = {
#                 'name': name,
#                 'baseFare': float(base_fare) if base_fare else 0,
#                 'perKmCharge': float(per_km_charge) if per_km_charge else 0,
#                 'perMinuteCharge': float(per_minute_charge) if per_minute_charge else 0,
#                 'capacity': int(capacity) if capacity else 0,
#                 'description': description,
#                 'isActive': is_active
#             }
            
#             vehicle_type_id = firebase_service.create_vehicle_type(data)
            
#             if vehicle_type_id:
#                 messages.success(request, "Vehicle type created successfully")
#             else:
#                 messages.error(request, "Failed to create vehicle type")
                
#         except Exception as e:
#             logger.error(f"Error creating vehicle type: {str(e)}")
#             messages.error(request, f"Error creating vehicle type: {str(e)}")
            
#     return redirect('vehicle_types')


def create_vehicle_type(request):
    """Create new vehicle type"""
    if request.method == 'POST':
        try:
            vehicle_type = request.POST.get('type')
            vehicle_icon = request.POST.get('vehicleIcon')
            status = request.POST.get('status', 'Active')
            
            if not vehicle_type or not vehicle_icon:
                messages.error(request, "Vehicle type and icon are required")
                return redirect('vehicle_types')
            
            data = {
                'type': vehicle_type,
                'vehicleIcon': vehicle_icon,
                'status': status
            }
            
            vehicle_type_id = firebase_service.create_vehicle_type(data)
            
            if vehicle_type_id:
                messages.success(request, "Vehicle type created successfully")
            else:
                messages.error(request, "Failed to create vehicle type")
                
        except Exception as e:
            logger.error(f"Error creating vehicle type: {str(e)}")
            messages.error(request, f"Error creating vehicle type: {str(e)}")
            
    return redirect('vehicle_types')


def update_vehicle_type(request, type_id):
    """Update vehicle type"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            base_fare = request.POST.get('base_fare')
            per_km_charge = request.POST.get('per_km_charge')
            per_minute_charge = request.POST.get('per_minute_charge')
            capacity = request.POST.get('capacity')
            description = request.POST.get('description')
            is_active = request.POST.get('is_active') == 'on'
            vehicle_icon = request.POST.get('vehicleIcon')
            status = request.POST.get('status')
            
            if not name:
                messages.error(request, "Vehicle type name is required")
                return redirect('vehicle_types')
            
            data = {
                'type': name,  # Change 'name' to 'type' to match Firestore
                'baseFare': float(base_fare) if base_fare else 0,
                'perKmCharge': float(per_km_charge) if per_km_charge else 0,
                'perMinuteCharge': float(per_minute_charge) if per_minute_charge else 0,
                'capacity': int(capacity) if capacity else 0,
                'description': description,
                'isActive': is_active,
                'vehicleIcon': vehicle_icon,
                'status': status
            }
            
            success = firebase_service.update_vehicle_type(type_id, data)
            
            if success:
                messages.success(request, "Vehicle type updated successfully")
            else:
                messages.error(request, "Failed to update vehicle type")
                
        except Exception as e:
            logger.error(f"Error updating vehicle type: {str(e)}")
            messages.error(request, f"Error updating vehicle type: {str(e)}")
            
    return redirect('vehicle_types')

def delete_vehicle_type(request, type_id):
    """Delete vehicle type"""
    if request.method == 'POST':
        try:
            success = firebase_service.delete_vehicle_type(type_id)
            
            if success:
                messages.success(request, "Vehicle type deleted successfully")
            else:
                messages.error(request, "Failed to delete vehicle type")
                
        except Exception as e:
            logger.error(f"Error deleting vehicle type: {str(e)}")
            messages.error(request, f"Error deleting vehicle type: {str(e)}")
            
    return redirect('vehicle_types')

def delete_driver_ajax(request):
    """Delete a driver via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            driver_id = data.get('driver_id')
            
            if not driver_id:
                return JsonResponse({'success': False, 'message': 'Driver ID is required'})
            
            success = firebase_service.delete_driver(driver_id)
            
            if success:
                return JsonResponse({'success': True, 'message': 'Driver deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to delete driver'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_customer_ajax(request):
    """AJAX endpoint to delete customer"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer_id')
            
            if not customer_id:
                return JsonResponse({'success': False, 'message': 'Customer ID is required'})
            
            success = firebase_service.delete_customer(customer_id)
            
            if success:
                return JsonResponse({'success': True, 'message': 'Customer deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to delete customer'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Keep the existing API views for external access
@api_view(['GET', 'POST'])
def drivers_list_api(request):
    if request.method == 'GET':
        drivers = firebase_service.get_all_drivers()
        return Response({
            'success': True,
            'data': drivers,
            'count': len(drivers)
        })
    elif request.method == 'POST':
        data = request.data
        driver_id = firebase_service.create_driver(data)
        if driver_id:
            return Response({
                'success': True,
                'message': 'Driver created successfully',
                'driver_id': driver_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Failed to create driver'
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def driver_detail_api(request, driver_id):
    if request.method == 'GET':
        driver = firebase_service.get_driver_by_id(driver_id)
        if driver:
            return Response({'success': True, 'data': driver})
        else:
            return Response({
                'success': False,
                'message': 'Driver not found'
            }, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        data = request.data
        success = firebase_service.update_driver(driver_id, data)
        if success:
            return Response({'success': True, 'message': 'Driver updated successfully'})
        else:
            return Response({
                'success': False,
                'message': 'Failed to update driver'
            }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        success = firebase_service.delete_driver(driver_id)
        if success:
            return Response({'success': True, 'message': 'Driver deleted successfully'})
        else:
            return Response({
                'success': False,
                'message': 'Failed to delete driver'
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def customers_list_api(request):
    if request.method == 'GET':
        customers = firebase_service.get_all_customers()
        return Response({
            'success': True,
            'data': customers,
            'count': len(customers)
        })
    elif request.method == 'POST':
        data = request.data
        customer_id = firebase_service.create_customer(data)
        if customer_id:
            return Response({
                'success': True,
                'message': 'Customer created successfully',
                'customer_id': customer_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Failed to create customer'
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail_api(request, customer_id):
    if request.method == 'GET':
        customer = firebase_service.get_customer_by_id(customer_id)
        if customer:
            return Response({'success': True, 'data': customer})
        else:
            return Response({
                'success': False,
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        data = request.data
        success = firebase_service.update_customer(customer_id, data)
        if success:
            return Response({'success': True, 'message': 'Customer updated successfully'})
        else:
            return Response({
                'success': False,
                'message': 'Failed to update customer'
            }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        success = firebase_service.delete_customer(customer_id)
        if success:
            return Response({'success': True, 'message': 'Customer deleted successfully'})
        else:
            return Response({
                'success': False,
                'message': 'Failed to delete customer'
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_stats_api(request):
    driver_stats = firebase_service.get_drivers_stats()
    customer_stats = firebase_service.get_customers_stats()
    return Response({
        'success': True,
        'data': {'drivers': driver_stats, 'customers': customer_stats}
    })

@api_view(['GET'])
def test_firebase_connection(request):
    try:
        if not firebase_service.db:
            return Response({
                'success': False,
                'message': 'Firebase not connected',
                'error': 'Database connection failed'
            })
        
        collections = firebase_service.db.collections()
        collection_names = [col.id for col in collections]
        collection_info = {}
        for col_name in collection_names:
            try:
                docs = list(firebase_service.db.collection(col_name).limit(5).stream())
                collection_info[col_name] = {
                    'document_count': len(docs),
                    'sample_ids': [doc.id for doc in docs]
                }
            except Exception as e:
                collection_info[col_name] = {'error': str(e)}
        
        return Response({
            'success': True,
            'message': 'Firebase connected successfully',
            'collections': collection_names,
            'collection_details': collection_info
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Firebase connection test failed',
            'error': str(e)
        })

# def vehicle_management(request):
#     """Vehicle management page to view and manage vehicle statuses"""
#     try:
#         vehicles = firebase_service.get_all_vehicles()
#         processed_vehicles = []
#         pending_count = 0
#         approved_count = 0
#         active_count = 0

#         for vehicle in vehicles:
#             driver_id = vehicle.get('userID')
#             driver = firebase_service.get_driver_by_id(driver_id) if driver_id else None
#             vehicle['driver_name'] = f"{driver.get('firstName', '')} {driver.get('lastName', '')}" if driver else 'Unknown'
#             vehicle['driver_id'] = driver_id

#             if not vehicle.get('isApproved', False):
#                 vehicle['status'] = 'Pending Approval'
#                 pending_count += 1
#             else:
#                 vehicle['status'] = 'Approved'
#                 approved_count += 1
#                 if driver and driver.get('isDriverOnline', False):
#                     vehicle['status'] = 'Active'
#                     active_count += 1
#                     approved_count -= 1

#             processed_vehicles.append(vehicle)

#         context = {
#             'vehicles': processed_vehicles,
#             'pending_count': pending_count,
#             'approved_count': approved_count,
#             'active_count': active_count,
#             'page_title': 'Vehicle Management'
#         }
#         return render(request, "vehicles/vehicle_management.html", context)
#     except Exception as e:
#         messages.error(request, f"Error loading vehicles: {str(e)}")
#         return render(request, "vehicles/vehicle_management.html", {
#             'vehicles': [], 
#             'pending_count': 0, 
#             'approved_count': 0, 
#             'active_count': 0
#         })



def vehicle_management(request):
    """Vehicle management page to view and manage vehicle statuses"""
    try:
        vehicles = firebase_service.get_all_vehicles()
        processed_vehicles = []
        pending_count = 0
        approved_count = 0
        active_count = 0

        for vehicle in vehicles:
            driver_id = vehicle.get('userID')
            driver = firebase_service.get_driver_by_id(driver_id) if driver_id else None
            vehicle['driver_name'] = f"{driver.get('firstName', 'Unknown')} {driver.get('lastName', 'Driver')}" if driver else 'Unknown Driver'
            vehicle['driver_id'] = driver_id

            if not vehicle.get('isApproved', False):
                vehicle['status'] = 'Pending Approval'
                pending_count += 1
            else:
                vehicle['status'] = 'Approved'
                approved_count += 1
                if driver and driver.get('isDriverOnline', False):
                    vehicle['status'] = 'Active'
                    active_count += 1
                    approved_count -= 1

            processed_vehicles.append(vehicle)
            logger.info(f"Processed vehicle {vehicle.get('id', 'N/A')} for driver {vehicle['driver_name']} with status {vehicle['status']}")

        context = {
            'vehicles': processed_vehicles,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'active_count': active_count,
            'page_title': 'Vehicle Management'
        }
        return render(request, "vehicles/vehicle_management.html", context)
    except Exception as e:
        logger.error(f"Error loading vehicles: {str(e)}")
        messages.error(request, f"Error loading vehicles: {str(e)}")
        return render(request, "vehicles/vehicle_management.html", {
            'vehicles': [], 
            'pending_count': 0, 
            'approved_count': 0, 
            'active_count': 0
        })


def update_vehicle_status(request):
    """AJAX endpoint to update vehicle status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle_id = data.get('vehicle_id')
            new_status = data.get('status')
            
            if not vehicle_id or new_status is None:
                return JsonResponse({'success': False, 'message': 'Missing required fields'})
            
            success = firebase_service.update_vehicle(vehicle_id, {'isApproved': new_status})
            
            if success:
                return JsonResponse({'success': True, 'message': 'Vehicle status updated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to update vehicle status'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_vehicle(request):
    """AJAX endpoint to delete vehicle"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle_id = data.get('vehicle_id')
            
            if not vehicle_id:
                return JsonResponse({'success': False, 'message': 'Vehicle ID is required'})
            
            success = firebase_service.delete_vehicle(vehicle_id)
            
            if success:
                return JsonResponse({'success': True, 'message': 'Vehicle deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to delete vehicle'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def driver_live_status(request, driver_id: str):
    """Return JSON with driver's current location and active trip for live tracking."""
    try:
        driver = firebase_service.get_driver_by_id(driver_id)
        if not driver:
            return JsonResponse({'success': False, 'message': 'Driver not found'}, status=404)

        location = firebase_service.get_driver_location(driver_id)
        current_trip = firebase_service.get_driver_current_trip(driver_id)

        # Shape response
        payload = {
            'success': True,
            'driver': {
                'id': driver.get('id'),
                'firstName': driver.get('firstName'),
                'lastName': driver.get('lastName'),
                'isDriverOnline': driver.get('isDriverOnline', False)
            },
            'location': location,
            'current_trip': None
        }

        if current_trip:
            payload['current_trip'] = {
                'id': current_trip.get('id'),
                'status': current_trip.get('status'),
                'pickupLocation': current_trip.get('pickupLocation'),
                'dropOffLocation': current_trip.get('dropOffLocation'),
                'pickupLatLng': current_trip.get('pickupLatLng'),
                'dropOffLatLng': current_trip.get('dropOffLatLng'),
                'deliveryAmount': current_trip.get('deliveryAmount'),
                'orderID': current_trip.get('orderID')
            }

        return JsonResponse(payload)
    except Exception as e:
        logger.error(f"driver_live_status error for {driver_id}: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)