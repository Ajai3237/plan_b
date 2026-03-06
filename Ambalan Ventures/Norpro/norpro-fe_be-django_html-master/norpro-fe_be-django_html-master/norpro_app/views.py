from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse  
from django.core.paginator import Paginator

base_url = "https://norpro.ca/"

# Create your views here.
def Index(request):
    testml = Testimonial.objects.all()
    context={'test': testml}
    return render(request,  "index.html", context)



def Company(request):
    com_test = Company_testimonial.objects.all()
    context={'test': com_test}
    return render(request, "company.html", context)



def memberships_and_partnerships(request):
    
    return render(request, "atss.html")



def Gallery_view(request):
    gallery = Gallery.objects.all()
    
    paginator = Paginator(gallery, 10)
    page_number = request.GET.get('page')
    gallery = paginator.get_page(page_number)
    
    context = {'gallery': gallery}
    return render(request, "video.html", context)



def News_events(request):
    news_events = News_and_events.objects.filter(date__lte=datetime.today()).order_by('-updated_at')
    context={'news_events': news_events}
    return render(request, "news_events.html", context)



def News_event_details(request, news_id):
    news_events = get_object_or_404(News_and_events, pk=news_id)
    next_news = News_and_events.objects.filter(updated_at__gt=news_events.updated_at).order_by('updated_at').first()
    prev_news = News_and_events.objects.filter(updated_at__lt=news_events.updated_at).order_by('-updated_at').first()
    context={'news_events':news_events, 'next_news': next_news, 'prev_news': prev_news}
    return render(request, "news_event_details.html", context)


from datetime import timedelta
def calendar(request):
    calendar_events = Calendar.objects.all()
    course_events = Course.objects.all()

    events = []
    
    training_base_path = '/training/'
    course_url_mapping = {
        'Lead Class 1 Operations Worker Training': 'lead_class_1_operations_worker_training',
        'Lead Hazard Awareness Training': 'lead_hazard_awareness_training',
        'Type 1 & 2 Asbestos Operations Worker Training': 'type_1_and_2_asbestos_operations_worker_training',
        'Asbestos Hazard Awareness Training': 'asbestos_hazard_awareness_training',
    }

    for event in calendar_events:
        events.append({
            'start_time': event.start_time,
            'end_time': event.end_time,
            'date': event.date,
            'title': event.title,
            'main_title': "Event",
            'pk': event.pk,
            'type': 'calendar',
            'url': reverse('events', args=[event.pk]),
        })
        
    for course in course_events:
        course_title = course.title
        
        course_key = course_url_mapping.get(course_title)
        url = f'{training_base_path}{course_key}' if course_key else None
        
        if course.from_date and course.to_date:
            current_date = course.from_date
            end_date = course.to_date

            while current_date <= end_date:
                events.append({
                    'start_time': course.start_time,
                    'end_time': course.end_time,
                    'date': current_date.isoformat(),
                    'title': course.title,
                    'main_title': "Training",
                    'pk': course.pk,
                    'type': 'course',
                    'url': url,
                })
                current_date += timedelta(days=1)
        elif course.from_date:
            events.append({
                'start_time': course.start_time,
                'end_time': course.end_time,
                'date': course.from_date.isoformat(),
                'title': course.title,
                'main_title': "Training",
                'pk': course.pk,
                'type': 'course',
                'url': url,
            })
            

    context = {'events': events}
    return render(request, "calendar.html",context)

def events(request, Calendar_id):
    events_details = get_object_or_404(Calendar, pk=Calendar_id)
    event_url = request.build_absolute_uri(reverse('events', args=[Calendar_id]))
    context={'events_details':events_details,'event_url': event_url}
    return render(request, "calendar_details.html", context)


def Mine_security(request):
    if request.method == 'POST':
            form = MineForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('mine_security')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = MineForm()
    return render(request, "Security/mine_security.html", {'form': form})

def Mobile_patrol(request):
    if request.method == 'POST':
            form = Mobile_patrolForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('mobile_patrol')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Mobile_patrolForm()
    return render(request, "Security/mobile_patrol.html", {'form': form})

def Industrial_guards(request):
    if request.method == 'POST':
        form = Industrial_guardsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('industrial_guards')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Industrial_guardsForm()
    return render(request, "Security/industrial_guards.html", {'form': form})

def static_guards_and_event_management(request):
    if request.method == 'POST':
        form = Static_guards_and_event_managementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('static_guards_and_event_management')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Static_guards_and_event_managementForm()
    return render(request, "Security/static_guards_and_event_management.html", {'form': form})

def Institutional_guards(request):
    if request.method == 'POST':
        form = Institutional_guardsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('institutional_guards')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Institutional_guardsForm()
    return render(request, "Security/institutional_guards.html", {'form': form})

def Loss_prevention(request):
    if request.method == 'POST':
        form = Loss_preventionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('Loss_prevention')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Loss_preventionForm()
    return render(request, "Security/loss_prevention.html", {'form': form})

def Other_service(request):
    if request.method == 'POST':
        form = Other_serviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('other_service')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Other_serviceForm()
    return render(request, "Security/other_service.html", {'form': form})

def Join_our_team(request):
    career = Career.objects.filter(status=1).order_by('-updated_at')
    if request.method == 'POST':
        print(request.POST)
        form = CareerformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('join_our_team')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CareerformForm()
    context={'career': career, 'form': form}
    return render(request, "page-career.html", context)

def Career_description(request, careers_id):
    
    career = get_object_or_404(Career, pk=careers_id)
    if request.method == 'POST':
        print(request.POST)
        form = CareerformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.type_career = career.title
            print(career.title)
            form.save()
            print(form)
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('join_our_team')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
            
    else:
        form = CareerformForm()
    context={'career': career, 'form': form}
    
    return render(request, "career_description.html", context)

def Academy(request):
    if request.method == 'POST':
        print(request.POST)
        form = AcademyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('academy')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = AcademyForm()
    return render(request, "training_school.html",{'form': form} )


def Courses(request):
    return render(request, "courses.html")

def security_guard_training(request):
    return render(request, "Training/security_guard_training.html")

def smart_serve(request):
    return render(request, "Training/smart_serve.html")

def Contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactFormForm()
    return render(request, "page-contact.html", {'form': form})

# def Mine_security(request):
#     if request.method == 'POST':
#             form = MineForm(request.POST)
#             if form.is_valid():
#                 form_instance = form.save(commit=False)
#                 form_instance.save()

#                 # Get form data
#                 form_data = form.cleaned_data

#                 # Prepare email content
#                 email_subject = f'Service request - {form_data["email"]}'
                
#                 # HTML message rendering using a template
#                 email_message_html = render_to_string('email_request/service_request_email.html', {
#                     'name': form_data['name'],
#                     'email': form_data['email'],
#                     'phone': form_data['phone'],
#                     'location': form_data['location'],
#                     'service': form_data['service'],
#                     'type_service': form_data['type_service'],
#                 })

#                 # Send email with both HTML and plain text alternatives
#                 send_mail(
#                     email_subject,
#                     '',  # Blank for plain text alternative (you're sending HTML)
#                     settings.EMAIL_HOST_USER,  # Sender's email
#                     ['info@norpro.ca'],  # Recipient's email
#                     html_message=email_message_html,  # Pass the HTML message
#                     fail_silently=False,
#                 )
                
#                 messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#                 return redirect('mine_security')
#             else:
#                 messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = MineForm()
#     return render(request, "Security/mine_security.html", {'form': form})



# def Mobile_patrol(request):
#     if request.method == 'POST':
#         form = Mobile_patrolForm(request.POST)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Service request - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/service_request_email.html', {
#                 'name': form_data['name'],
#                 'email': form_data['email'],
#                 'phone': form_data['phone'],
#                 'location': form_data['location'],
#                 'service': form_data['service'],
#                 'type_service': form_data['type_service'],
#             })

#             # Send email with both HTML and plain text alternatives
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['info@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )

#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('mobile_patrol')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = Mobile_patrolForm()
#     return render(request, "Security/mobile_patrol.html", {'form': form})



# def Industrial_guards(request):
#     if request.method == 'POST':
#         form = Industrial_guardsForm(request.POST)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Service request - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/service_request_email.html', {
#                 'name': form_data['name'],
#                 'email': form_data['email'],
#                 'phone': form_data['phone'],
#                 'location': form_data['location'],
#                 'service': form_data['service'],
#                 'type_service': form_data['type_service'],
#             })

#             # Send email with both HTML and plain text alternatives
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['info@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('industrial_guards')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = Industrial_guardsForm()
#     return render(request, "Security/industrial_guards.html", {'form': form})



# def Institutional_guards(request):
#     if request.method == 'POST':
#         form = Institutional_guardsForm(request.POST)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Service request - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/service_request_email.html', {
#                 'name': form_data['name'],
#                 'email': form_data['email'],
#                 'phone': form_data['phone'],
#                 'location': form_data['location'],
#                 'service': form_data['service'],
#                 'type_service': form_data['type_service'],
#             })

#             # Send email with both HTML and plain text alternatives
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['info@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('institutional_guards')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = Institutional_guardsForm()
#     return render(request, "Security/institutional_guards.html", {'form': form})



# def Other_service(request):
#     if request.method == 'POST':
#         form = Other_serviceForm(request.POST)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Service request - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/service_request_email.html', {
#                 'name': form_data['name'],
#                 'email': form_data['email'],
#                 'phone': form_data['phone'],
#                 'location': form_data['location'],
#                 'service': form_data['service'],
#                 'type_service': form_data['type_service'],
#             })
            
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['info@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('other_service')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = Other_serviceForm()
#     return render(request, "Security/other_service.html", {'form': form})



# def Join_our_team(request):
#     career = Career.objects.filter(status=1).order_by('-updated_at')
#     if request.method == 'POST':
#         print(request.POST)
#         form = CareerformForm(request.POST, request.FILES)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Career - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/career_request.html', {
#                 'first_name': form_data['first_name'],
#                 'last_name': form_data['last_name'],
#                 'email': form_data['email'],
#                 'phone' : form_data['phone'],
#                 'resume': f"{base_url}{form_instance.resume.url}" if form_instance.resume else None,
#                 'cover_letter': f"{base_url}{form_instance.cover_letter.url}" if form_instance.cover_letter else None,
#                 'other_documents': f"{base_url}{form_instance.other_documents.url}" if form_instance.other_documents else None,
#                 'type_career' : form_data['type_career'],
#             })
            
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['hiring@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('join_our_team')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = CareerformForm()
#     context={'career': career, 'form': form}
#     return render(request, "page-career.html", context)

# def Career_description(request, careers_id):
    
#     career = get_object_or_404(Career, pk=careers_id)
#     if request.method == 'POST':
#         print(request.POST)
#         form = CareerformForm(request.POST, request.FILES)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.type_career = career.title  # Assuming career is defined somewhere
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Career - {form_data["email"]}'

#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/career_request.html', {
#                 'first_name': form_data['first_name'],
#                 'last_name': form_data['last_name'],
#                 'email': form_data['email'],
#                 'phone': form_data['phone'],
#                 'resume': f"{base_url}{form_instance.resume.url}" if form_instance.resume else None,
#                 'cover_letter': f"{base_url}{form_instance.cover_letter.url}" if form_instance.cover_letter else None,
#                 'other_documents': f"{base_url}{form_instance.other_documents.url}" if form_instance.other_documents else None,
#                 'type_career': form_instance.type_career,
#             })

#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['hiring@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('join_our_team')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
            
#     else:
#         form = CareerformForm()
#     context={'career': career, 'form': form}
    
#     return render(request, "career_description.html", context)

# def Academy(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = AcademyForm(request.POST, request.FILES)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Academy - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/academy_request.html', {
#                 'first_name': form_data['first_name'],
#                 'last_name': form_data['last_name'],
#                 'email': form_data['email'],
#                 'phone' : form_data['phone'],
#                 'file_upload': f"{base_url}{form_instance.file_upload.url}" if form_instance.file_upload else None,
#             })
            
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['hiring@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('academy')
#         else:
#             messages.error(request, 'There was an error with your submission. Please check the form and try again.')
#     else:
#         form = AcademyForm()
#     return render(request, "training_school.html",{'form': form} )

# def Contact(request):
#     if request.method == 'POST':
#         form = ContactFormForm(request.POST)
#         if form.is_valid():
#             form_instance = form.save(commit=False)
#             form_instance.save()

#             # Get form data
#             form_data = form.cleaned_data

#             # Prepare email content
#             email_subject = f'Contact - {form_data["email"]}'
            
#             # HTML message rendering using a template
#             email_message_html = render_to_string('email_request/contact_request.html', {
#                 'name': form_data['name'],
#                 'email': form_data['email'],
#                 'company_name': form_data['company_name'],
#                 'phone' : form_data['phone'],
#                 'subject' : form_data['subject'],
#                 'message' : form_data['message'],
#             })
            
#             send_mail(
#                 email_subject,
#                 '',  # Blank for plain text alternative (you're sending HTML)
#                 settings.EMAIL_HOST_USER,  # Sender's email
#                 ['info@norpro.ca'],  # Recipient's email
#                 html_message=email_message_html,  # Pass the HTML message
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Thank you for your submission! We will get back to you soon.')
#             return redirect('contact')
#     else:
#         form = ContactFormForm()
#     return render(request, "page-contact.html", {'form': form})


def Employee_referral_security(request):
    print(request.POST)
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        phone = request.POST.get('phone')
        rf_first_name = request.POST.get('rf_first_name')
        rf_last_name = request.POST.get('rf_last_name')
        rf_email = request.POST.get('rf_email')
        rf_confirm_email = request.POST.get('rf_confirm_email')
        rf_phone = request.POST.get('rf_phone')
        referal_reason = request.POST.get('referal_reason')
        security_license = request.POST.get('security_license') == 'yes'
        drivers_license = request.POST.get('drivers_license') == 'yes'
        # gc_president_choice = 'giftCard1' in request.POST
        # gc_the_marconi = 'giftCard2' in request.POST
        # gc_canadian_tire = 'giftCard3' in request.POST
        # gc_esso_gas_card = 'giftCard4' in request.POST
        if email != confirm_email:
            messages.error(request,'Your emails does not match')
        if rf_email != rf_confirm_email:
            messages.error(request,'Referal emails does not match')

        # Create an instance of the model and populate fields
        employee_referral = Employee_referral_program(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            referal_first_name=rf_first_name,
            referal_last_name=rf_last_name,
            referal_email=rf_email,
            referal_phone=rf_phone,
            referral_reason=referal_reason,
            have_security_guard_license=security_license,
            have_drivers_license=drivers_license,
            # gc_president_choice=gc_president_choice,
            # gc_the_marconi=gc_the_marconi,
            # gc_canadian_tire=gc_canadian_tire,
            # gc_esso_gas_card=gc_esso_gas_card,
        )

        # Save the instance to the database
        employee_referral.save()
        # email_subject = f'Referal Request - {email}'
        
        # # HTML message rendering using a template
        # email_message_html = render_to_string('email_request/referal_email.html', {
        #     'first_name': first_name,
        #     'last_name': last_name,
        #     'email': email,
        #     'phone' : phone,
        #     'referal_first_name':rf_first_name,
        #     'referal_last_name':rf_last_name,
        #     'referal_email':rf_email,
        #     'referal_phone':rf_phone,
        #     'referral_reason':referal_reason,
        #     'have_security_guard_license':security_license,
        #     'have_drivers_license':drivers_license,
        #     # 'gc_president_choice':gc_president_choice,
        #     # 'gc_the_marconi':gc_the_marconi,
        #     # 'gc_canadian_tire':gc_canadian_tire,
        #     # 'gc_esso_gas_card':gc_esso_gas_card,
        # })
        
        # send_mail(
        #     email_subject,
        #     '',  # Blank for plain text alternative (you're sending HTML)
        #     settings.EMAIL_HOST_USER,  # Sender's email
        #     ['muhammedalthaj.primalcodes@gmail.com'],  # Recipient's email
        #     html_message=email_message_html,  # Pass the HTML message
        #     fail_silently=False,
        # )
        
        messages.success(request, 'Thank you for your submission! We will get back to you soon.')
        return redirect('employee_refferal_security')
    return render(request,'employee_referral_security.html',locals()) 



# health_and_safety

# TRANING
def training(request):
    if request.method == 'POST':
            form = Training_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('training')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Training_Form()
    return render(request, "health_and_safety/Training.html", {'form': form})

def lead_class_1_operations_worker_training(request):
    today = timezone.now().date()
    active_courses_1 = (
        Course.objects.filter(status='Active', from_date__gte=today, title='Lead Class 1 Operations Worker Training')
        .annotate(participant_count=Count('schedule_list', filter=Q(schedule_list__status__in=['Pending', 'Accepted'])))
        .values('id', 'title', 'from_date', 'to_date', 'start_time', 'end_time', 'price', 'place', 'participant_count')
    )
    
    if request.method == 'POST':
        form = CourseFormForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            course_instance = Course.objects.get(id=course_id)
            if course_instance.from_date >= today:
                    course_list_instance = form.save(commit=False)
                    course_list_instance.course = course_instance
                    course_list_instance.save()
                    
                    # # Get form data
                    # form_data = form.cleaned_data

                    # # Prepare email content
                    # email_subject = f'Training request - {form_data["email"]}'
                    
                    # # HTML message rendering using a template
                    # email_message_html = render_to_string('email_request/course_request_email.html', {
                    #     'course_title': course_instance.title,
                    #     'course_date': course_instance.from_date,
                    #     'first_name': form_data['first_name'],
                    #     'last_name': form_data['last_name'],
                    #     'email': form_data['email'],
                    #     'phone': form_data['phone'],
                    #     'message': form_data['message'],
                    # })
                    
                    # email_subject_1 = f'Training Submission - {settings.EMAIL_HOST_USER}'
                    # # HTML message rendering using a template
                    # email_message_html_1 = render_to_string('email_request/course_request_greeting_email.html', {
                    #     'course_title': course_instance.title,
                    #     'course_date': course_instance.from_date,
                    #     'first_name': form_data['first_name'],
                    #     'last_name': form_data['last_name'],
                    # })

                    # # Send email with both HTML and plain text alternatives
                    # send_mail(
                    #     email_subject,
                    #     '',
                    #     settings.EMAIL_HOST_USER,
                    #     ['sageer.primalcodes@gmail.com'], 
                    #     html_message=email_message_html,
                    #     fail_silently=False,
                    # )
                    
                    #  # Send email with both HTML and plain text alternatives
                    # send_mail(
                    #     email_subject_1,
                    #     '',
                    #     settings.EMAIL_HOST_USER,
                    #     [form_data["email"]], 
                    #     html_message=email_message_html_1,
                    #     fail_silently=False,
                    # )

                    messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                    return redirect('lead_class_1_operations_worker_training')
                
            else:
                messages.error(request, 'This course is no longer available.')
                return redirect('lead_class_1_operations_worker_training')
        else:
            print('Form Errors:', form.errors)
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CourseFormForm()
    
    return render(request, "health_and_safety/lead_training_services_1.html", {'form': form,
                                                                             'courses_1': active_courses_1,
                                                                             'today': today})
    
    
def lead_hazard_awareness_training(request):
    today = timezone.now().date()
    active_courses_2 = (
        Course.objects.filter(status='Active', from_date__gte=today, title='Lead Hazard Awareness Training')
        .annotate(participant_count=Count('schedule_list', filter=Q(schedule_list__status__in=['Pending', 'Accepted'])))
        .values('id', 'title', 'from_date', 'to_date', 'start_time', 'end_time', 'price', 'place', 'participant_count')
    )
    
    if request.method == 'POST':
        form = CourseFormForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            course_instance = Course.objects.get(id=course_id)
            if course_instance.from_date >= today:
                    course_list_instance = form.save(commit=False)
                    course_list_instance.course = course_instance
                    course_list_instance.save()

                    messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                    return redirect('lead_hazard_awareness_training')
                
            else:
                messages.error(request, 'This course is no longer available.')
                return redirect('lead_hazard_awareness_training')
        else:
            print('Form Errors:', form.errors)
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CourseFormForm()
    
    return render(request, "health_and_safety/lead_training_services_2.html", {'form': form,
                                                                             'courses_2': active_courses_2,
                                                                             'today': today})


def type_1_and_2_asbestos_operations_worker_training(request):
    today = timezone.now().date()
    active_courses_1 = (
        Course.objects.filter(status='Active', from_date__gte=today, title='Type 1 & 2 Asbestos Operations Worker Training')
        .annotate(participant_count=Count('schedule_list', filter=Q(schedule_list__status__in=['Pending', 'Accepted'])))
        .values('id', 'title', 'from_date', 'to_date', 'start_time', 'end_time', 'price', 'place', 'participant_count')
    )
    
    if request.method == 'POST':
        form = CourseFormForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            course_instance = Course.objects.get(id=course_id)
            if course_instance.from_date >= today:
                    course_list_instance = form.save(commit=False)
                    course_list_instance.course = course_instance
                    course_list_instance.save()

                    messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                    return redirect('type_1_and_2_asbestos_operations_worker_training')
                
            else:
                messages.error(request, 'This course is no longer available.')
                return redirect('type_1_and_2_asbestos_operations_worker_training')
        else:
            print('Form Errors:', form.errors)
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CourseFormForm()
        
    return render(request, "health_and_safety/asbestos_training_services_1.html", {'form': form,
                                                                                'courses_1': active_courses_1,
                                                                                'today': today})
    

def asbestos_hazard_awareness_training(request):
    today = timezone.now().date()
    active_courses_2 = (
        Course.objects.filter(status='Active', from_date__gte=today, title='Asbestos Hazard Awareness Training')
        .annotate(participant_count=Count('schedule_list', filter=Q(schedule_list__status__in=['Pending', 'Accepted'])))
        .values('id', 'title', 'from_date', 'to_date', 'start_time', 'end_time', 'price', 'place', 'participant_count')
    )
    
    if request.method == 'POST':
        form = CourseFormForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            course_instance = Course.objects.get(id=course_id)
            if course_instance.from_date >= today:
                    course_list_instance = form.save(commit=False)
                    course_list_instance.course = course_instance
                    course_list_instance.save()

                    messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                    return redirect('asbestos_hazard_awareness_training')
                
            else:
                messages.error(request, 'This course is no longer available.')
                return redirect('asbestos_hazard_awareness_training')
        else:
            print('Form Errors:', form.errors)
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = CourseFormForm()
        
    return render(request, "health_and_safety/asbestos_training_services_2.html", {'form': form,
                                                                                'courses_2': active_courses_2,
                                                                                'today': today})
      
def check_email_uniqueness(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        course_id = request.POST.get('course_id')

        course_instance = Course.objects.get(id=course_id)
        exists = Schedule_list.objects.filter(email=email, course=course_instance).exists()

        return JsonResponse({'exists': exists})


def respirator_fit_testing(request):
    if request.method == 'POST':
            form = Respirator_fit_testing_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('respirator_fit_testing')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Respirator_fit_testing_Form()
    return render(request, "health_and_safety/respirator_fit_testing.html", {'form': form})



def support_services(request):
    if request.method == 'POST':
            form = Support_services_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('support_services')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = Support_services_Form()
    return render(request, "health_and_safety/support_services.html", {'form': form})


def management_system_implementation_and_auditing(request):
    if request.method == 'POST':
            form = management_system_implementation_and_auditing_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('management_system_implementation_and_auditing')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = management_system_implementation_and_auditing_Form()
    return render(request, "health_and_safety/management_system_implementation_and_auditing.html", {'form': form})


def hazardous_materials_testing_management_and_remediation(request):
    if request.method == 'POST':
            form = hazardous_materials_testing_management_and_remediation_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('hazardous_materials_testing_management_and_remediation')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = hazardous_materials_testing_management_and_remediation_Form()
    return render(request, "health_and_safety/hazardous_materials_testing_management_and_remediation.html", {'form': form})


def indoor_air_quality_assessment_services(request):
    if request.method == 'POST':
            form = indoor_air_quality_assessment_services_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('indoor_air_quality_assessment_services')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = indoor_air_quality_assessment_services_Form()
    return render(request, "health_and_safety/indoor_air_quality_assessment_services.html", {'form': form})


def workplace_noise_assessments(request):
    if request.method == 'POST':
            form = workplace_noise_assessments_Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your submission! We will get back to you soon.')
                return redirect('workplace_noise_assessments')
            else:
                messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = workplace_noise_assessments_Form()
    return render(request, "health_and_safety/workplace_noise_assessments.html", {'form': form})


def security(request):
    context={}
    return render(request, "security.html", context)

def health_and_safety(request):
    context={}
    return render(request, "health_and_safety.html", context)

# id card
def identity_card(request, slug_id):
    abs_url = request.build_absolute_uri()
    card= id_card.objects.filter(slug=slug_id)
    context={"id_card":card, "abs_url":abs_url}
    return render(request, "id_card.html", context)

def meet_the_team(request):
    card= id_card.objects.filter(show_in_home=True)
    context={"card":card}
    return render(request, "meet_our_support_team.html", context)


import vobject
from django.http import HttpResponse
def download_vcard(request, slug):
    try:
        # Retrieve a specific id_card object using get()
        card = id_card.objects.get(slug=slug)

        # Create vCard
        vcard = vobject.vCard()

        # Add Full Name (FN)
        if card.name:
            vcard.add('fn').value = card.name

        # Add Title
        if card.title:
            vcard.add('title').value = card.title

        # Add Phone Number
        if card.phone_number:
            vcard.add('tel').value = card.phone_number

        # Add Email
        if card.email:
            vcard.add('email').value = card.email

        # Add Bio
        if card.bio:
            vcard.add('note').value = card.bio

        # Add LinkedIn
        if card.linkedin:
            vcard.add('linkedin').value = card.linkedin

        # Add more fields as needed

        # Serve vCard as a downloadable file
        response = HttpResponse(vcard.serialize(), content_type='text/vcard')
        response['Content-Disposition'] = f'attachment; filename={card.name}_contact.vcf'
        return response
    except id_card.DoesNotExist:
        return HttpResponse("id_card not found", status=404)
    
    
def siteMap(request):
    sitemap_path = ('sitemap.xml')
    with open(sitemap_path, 'r') as f:
        sitemap_content = f.read()
    return HttpResponse(sitemap_content, content_type='application/xml')


def privacy_and_policy(request):
    context={}
    return render(request, "privacy_and_policy.html", context)

def terms_and_conditions(request):
    context={}
    return render(request, "terms_and_conditions.html", context)
