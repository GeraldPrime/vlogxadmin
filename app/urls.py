# logistics_app/urls.py - Updated URLs
from django.urls import path
from . import views
from .views_mailing import customer_mailing, driver_mailing, customer_mailing_ajax
from .views_faqs import faqs_list, faq_create, faq_edit, faq_delete
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication URLs
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('', views.home, name='home'),
    path('drivers/', views.drivers_management, name='drivers_management'),
    path('customers/', views.customers_management, name='customers_management'),
    path('drivers/<str:driver_id>/', views.driver_detail, name='driver_detail'),
    path('customers/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    path('vehicles/', views.vehicle_management, name='vehicle_management'),

    # Vehicle Types Management
    path('vehicle-types/', views.vehicle_types, name='vehicle_types'),
    path('vehicle-types/create/', views.create_vehicle_type, name='create_vehicle_type'),
    path('vehicle-types/<str:type_id>/update/', views.update_vehicle_type, name='update_vehicle_type'),
    path('vehicle-types/<str:type_id>/delete/', views.delete_vehicle_type, name='delete_vehicle_type'),

    # Payment Modes Management
    path('payment-modes/', views.payment_modes, name='payment_modes'),
    path('payment-modes/create/', views.create_payment_mode, name='create_payment_mode'),
    path('payment-modes/<str:payment_mode_id>/update/', views.update_payment_mode, name='update_payment_mode'),
    path('payment-modes/<str:payment_mode_id>/delete/', views.delete_payment_mode, name='delete_payment_mode'),

    # Payment Settings Management
    path('payment-settings/', views.payment_settings, name='payment_settings'),
    path('payment-settings/create/', views.create_payment_setting, name='create_payment_setting'),
    path('payment-settings/<str:payment_setting_id>/update/', views.update_payment_setting, name='update_payment_setting'),
    path('payment-settings/<str:setting_id>/delete/', views.delete_payment_setting, name='delete_payment_setting'),

    # Orders Management
    path('orders/', views.orders_management, name='orders_management'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/update-status/', views.update_order_status, name='update_order_status'),

    # AJAX endpoints
    path('ajax/update-driver-status/', views.update_driver_status, name='update_driver_status'),
    path('ajax/delete-driver/', views.delete_driver_ajax, name='delete_driver_ajax'),
    path('ajax/delete-customer/', views.delete_customer_ajax, name='delete_customer_ajax'),
    path('ajax/update-vehicle-status/', views.update_vehicle_status, name='update_vehicle_status'),
    path('ajax/delete-vehicle/', views.delete_vehicle, name='delete_vehicle'),

    # Live driver status endpoint
    path('api/drivers/<str:driver_id>/live/', views.driver_live_status, name='driver_live_status'),

    # API endpoints
    path('api/test-firebase/', views.test_firebase_connection, name='test_firebase'),
    path('api/drivers/', views.drivers_list_api, name='drivers_list_api'),
    path('api/drivers/<str:driver_id>/', views.driver_detail_api, name='driver_detail_api'),
    path('api/customers/', views.customers_list_api, name='customers_list_api'),
    path('api/customers/<str:customer_id>/', views.customer_detail_api, name='customer_detail_api'),
    path('api/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/customers/<str:customer_id>/live/', views.customer_live_status, name='customer_live_status'),


    path('mailing/customers/', customer_mailing, name='customer_mailing'),
    path('mailing/customers/ajax/', customer_mailing_ajax, name='customer_mailing_ajax'),
    path('mailing/drivers/', driver_mailing, name='driver_mailing'),
    path('faqs/', faqs_list, name='faqs'),  # Use faqs_list for /faqs/
    path('faqs/manage/', faqs_list, name='faqs_manage'),
    path('faqs/create/', faq_create, name='faq_create'),
    path('faqs/edit/<str:faq_id>/', faq_edit, name='faq_edit'),
    path('faqs/delete/<str:faq_id>/', faq_delete, name='faq_delete'),
]