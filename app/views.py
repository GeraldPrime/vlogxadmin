
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .firebase_service import FirebaseService
import json
import logging

logger = logging.getLogger(__name__)
firebase_service = FirebaseService()

# Template Views (for your admin interface)
# def home(request):
#     """Dashboard home page"""
#     try:
#         driver_stats = firebase_service.get_drivers_stats()
#         customer_stats = firebase_service.get_customers_stats()
        
#         context = {
#             'driver_stats': driver_stats,
#             'customer_stats': customer_stats,
#             'total_drivers': driver_stats.get('total_drivers', 0),
#             'active_drivers': driver_stats.get('active_drivers', 0),
#             'total_customers': customer_stats.get('total_customers', 0),
#         }
#         return render(request, "index.html", context)
#     except Exception as e:
#         messages.error(request, f"Error loading dashboard: {str(e)}")
#         return render(request, "index.html", {'driver_stats': {}, 'customer_stats': {}})

def home(request):
    """Dashboard home page"""
    try:
        driver_stats = firebase_service.get_drivers_stats()
        customer_stats = firebase_service.get_customers_stats()
        
        total_drivers = driver_stats.get('total_drivers', 0)
        active_drivers = driver_stats.get('active_drivers', 0)
        offline_drivers = max(0, total_drivers - active_drivers)  # Ensure non-negative

        context = {
            'driver_stats': driver_stats,
            'customer_stats': customer_stats,
            'total_drivers': total_drivers,
            'active_drivers': active_drivers,
            'offline_drivers': offline_drivers,
            'total_customers': customer_stats.get('total_customers', 0),
            'pending_drivers': driver_stats.get('pending_drivers', 0),  # Assuming this is available
            'approved_drivers': driver_stats.get('approved_drivers', 0),  # Assuming this is available
        }
        return render(request, "index.html", context)
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, "index.html", {
            'driver_stats': {},
            'customer_stats': {},
            'total_drivers': 0,
            'active_drivers': 0,
            'offline_drivers': 0,
            'total_customers': 0,
            'pending_drivers': 0,
            'approved_drivers': 0,
        }) 


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
    """Driver detail page with documents and vehicle review"""
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

        context = {
            'driver': driver,
            'driver_documents': driver_documents,
            'vehicle': vehicle,
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
        
        context = {
            'customer': customer,
            'page_title': f'Customer Details - {customer.get("firstName", "")} {customer.get("lastName", "")}'
        }
        return render(request, "customers/customer_detail.html", context)
    except Exception as e:
        messages.error(request, f"Error loading customer: {str(e)}")
        return redirect('customers_management')

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

def delete_driver_ajax(request):
    """AJAX endpoint to delete driver"""
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