from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app.firebase_service import FirebaseService

firebase_service = FirebaseService()

@csrf_exempt
def faqs_list(request):
    faqs = firebase_service.get_all_faqs()
    return render(request, 'faqs_manage.html', {'faqs': faqs})

@csrf_exempt
def faq_create(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        if question and answer:
            firebase_service.create_faq({'question': question, 'answer': answer})
        return redirect('faqs_manage')
    return render(request, 'faq_form.html', {'action': 'Create'})

@csrf_exempt
def faq_edit(request, faq_id):
    faq = firebase_service.get_faq_by_id(faq_id)
    if not faq:
        return redirect('faqs_manage')
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        if question and answer:
            firebase_service.update_faq(faq_id, {'question': question, 'answer': answer})
        return redirect('faqs_manage')
    return render(request, 'faq_form.html', {'faq': faq, 'action': 'Edit'})

@csrf_exempt
def faq_delete(request, faq_id):
    firebase_service.delete_faq(faq_id)
    return redirect('faqs_manage')
