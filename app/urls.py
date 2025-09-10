# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
    
#     # Driver endpoints
#     path('test-firebase/', views.test_firebase_connection, name='test_firebase'),
    
#     path('drivers/', views.drivers_list, name='drivers_list'),
#     path('drivers/<str:driver_id>/', views.driver_detail, name='driver_detail'),
    
#     # Customer endpoints
#     path('customers/', views.customers_list, name='customers_list'),
#     path('customers/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    
#     # Analytics endpoints
#     path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
  
  
# ]

# logistics_app/urls.py - Updated URLs
from django.urls import path
from . import views

urlpatterns = [
    
    
    # Existing URLs remain unchanged...
    # path('', views.home, name='home'),
    # path('drivers/', views.drivers_management, name='drivers_management'),
    # path('customers/', views.customers_management, name='customers_management'),
    # path('drivers/<str:driver_id>/', views.driver_detail, name='driver_detail'),
    # path('customers/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    # path('vehicles/', views.vehicle_management, name='vehicle_management'),
    # # AJAX endpoints...
    # path('ajax/update-driver-status/', views.update_driver_status, name='update_driver_status'),
    # path('ajax/delete-driver/', views.delete_driver_ajax, name='delete_driver_ajax'),
    # path('ajax/delete-customer/', views.delete_customer_ajax, name='delete_customer_ajax'),
    # path('ajax/update-vehicle-status/', views.update_vehicle_status, name='update_vehicle_status'),
    # path('ajax/delete-vehicle/', views.delete_vehicle, name='delete_vehicle'),
    # # API endpoints...
    # path('api/test-firebase/', views.test_firebase_connection, name='test_firebase'),
    # path('api/drivers/', views.drivers_list_api, name='drivers_list_api'),
    # path('api/drivers/<str:driver_id>/', views.driver_detail_api, name='driver_detail_api'),
    # path('api/customers/', views.customers_list_api, name='customers_list_api'),
    # path('api/customers/<str:customer_id>/', views.customer_detail_api, name='customer_detail_api'),
    # path('api/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    
    
    path('', views.home, name='home'),
    path('drivers/', views.drivers_management, name='drivers_management'),
    path('customers/', views.customers_management, name='customers_management'),
    path('drivers/<str:driver_id>/', views.driver_detail, name='driver_detail'),
    path('customers/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    path('vehicles/', views.vehicle_management, name='vehicle_management'),
    path('ajax/update-driver-status/', views.update_driver_status, name='update_driver_status'),
    path('ajax/delete-driver/', views.delete_driver_ajax, name='delete_driver_ajax'),
    path('ajax/delete-customer/', views.delete_customer_ajax, name='delete_customer_ajax'),
    path('ajax/update-vehicle-status/', views.update_vehicle_status, name='update_vehicle_status'),
    path('ajax/delete-vehicle/', views.delete_vehicle, name='delete_vehicle'),
    path('api/test-firebase/', views.test_firebase_connection, name='test_firebase'),
    path('api/drivers/', views.drivers_list_api, name='drivers_list_api'),
    path('api/drivers/<str:driver_id>/', views.driver_detail_api, name='driver_detail_api'),
    path('api/customers/', views.customers_list_api, name='customers_list_api'),
    path('api/customers/<str:customer_id>/', views.customer_detail_api, name='customer_detail_api'),
    path('api/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    
    
    
]