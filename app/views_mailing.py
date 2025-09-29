from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from app.firebase_service import FirebaseService
from django.http import JsonResponse
import time

firebase_service = FirebaseService()

@csrf_exempt
def customer_mailing(request):
    success = error = None
    customers = firebase_service.get_all_customers()
    total_customers = len([c for c in customers if c.get('email')])
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        emails = [c.get('email') for c in customers if c.get('email')]
        sent_count = 0
        if emails:
            try:
                for email in emails:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],  # Send to one recipient at a time
                        fail_silently=False,
                    )
                    sent_count += 1
                success = f'Email sent to {sent_count} customers.'
            except Exception as e:
                error = f'Error sending email: {e}'
        else:
            error = 'No customer emails found.'
    return render(request, 'customers/customer_mailing.html', {'success': success, 'error': error, 'total_customers': total_customers})

@csrf_exempt
def driver_mailing(request):
    success = error = None
    drivers = firebase_service.get_all_drivers()
    total_drivers = len([d for d in drivers if d.get('email')])
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        emails = [d.get('email') for d in drivers if d.get('email')]
        if emails:
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    emails,  # Send to all at once
                    fail_silently=False,
                )
                success = f'Email sent to all drivers.'
            except Exception as e:
                error = f'Error sending email: {e}'
        else:
            error = 'No driver emails found.'
    return render(request, 'drivers/driver_mailing.html', {'success': success, 'error': error, 'total_drivers': total_drivers})

@csrf_exempt
def customer_mailing_ajax(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        customers = firebase_service.get_all_customers()
        emails = [c.get('email') for c in customers if c.get('email')]
        total = len(emails)
        sent = 0
        errors = []
        for email in emails:
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                sent += 1
            except Exception as e:
                errors.append(str(e))
            # Simulate delay for demo (remove in production)
            time.sleep(0.2)
        return JsonResponse({'sent': sent, 'total': total, 'errors': errors})
    return JsonResponse({'error': 'Invalid request'}, status=400)
