from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count
import qrcode, json
from io import BytesIO
from datetime import datetime
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse, FileResponse
import base64
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import csv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import HexColor
from django.db.models import Case, When
import uuid, os, re
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter, PageObject
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from uuid import uuid4

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Authenticate using the custom EmailBackend
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_staff and user.user_type != "Team" :
            login(request, user)
            messages.success(request, "Successfully logged in...")
            return redirect("admin_home")
        else:
            messages.error(request, "Email or password mismatch, please try again.")
            return redirect("admin_login")
    
    return render(request, 'crm/main/auth/admin_login.html', {})
    
def user_logout(request):
    logout(request)
    messages.success(request, ("Successfully logged out..."))
    return redirect('admin_login')

@login_required(login_url="admin_login")
def Admin_home(request):
    return render(request, 'crm/main/index.html')


# User_list
def Create_User(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
    else:
        form = AdminUserForm()
    return render(request, 'crm/main/auth/user/create.html', {'form': form})


def Edituser(request, user_id):
    customuser = get_object_or_404(AdminUser, pk=user_id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=customuser)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        form = AdminUserEditForm(instance=customuser)

    return render(request, 'crm/main/auth/user/edit.html', {'form': form, 'customuser': customuser})


def User_list(request):
    user_custome = AdminUser.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        user_custome = AdminUser.objects.filter(
            Q(username__icontains=search_query) |  Q(email__icontains=search_query)
        )
    else:
        user_custome = AdminUser.objects.all().order_by('-id')
    
    paginator = Paginator(user_custome, 50)
    
    page_number = request.GET.get('page')
    user_custome = paginator.get_page(page_number)
    context={'tests': user_custome}
    return render(request, 'crm/main/auth/user/user.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save() 
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('admin_login')  
    else:
        form = CustomPasswordChangeForm(request.user)  

    return render(request, 'crm/main/auth/user/password_change.html', {
        'form': form
    })
    
@login_required
def user_password_change(request, user_id):
    user = get_object_or_404(AdminUser, id=user_id)
    if request.method == 'POST':
        form = SimplifiedPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Password for {user.username} has been changed successfully!")
            return redirect('user_list')
    else:
        form = SimplifiedPasswordChangeForm(user)

    return render(request, 'crm/main/auth/user/password_change_user.html', {'form': form, 'user': user})
    
# path list
def Create_Permission(request):
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission added successfully!')
            return redirect('permission_list') 
    else:
        form = PathForm()
    
    return render(request, 'crm/main/auth/permission/create.html', {'form': form})


def Editpermission(request, permission_id):
    permission_instance = get_object_or_404(Path, pk=permission_id)
    
    if request.method == 'POST':
        form = PathForm(request.POST, instance=permission_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission updated successfully!')
            return redirect('permission_list') 
    else:
        form = PathForm(instance=permission_instance)

    return render(request, 'crm/main/auth/permission/edit.html', {'form': form, 'permission': permission_instance})


def Permission_list(request):
    permissions = Path.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        permissions = Path.objects.filter(
            Q(path_name__icontains=search_query)
        )
    else:
        permissions = Path.objects.all().order_by('id')
    
    paginator = Paginator(permissions, 50)
    
    page_number = request.GET.get('page')
    permissions = paginator.get_page(page_number)
    context={'tests': permissions}
    return render(request, 'crm/main/auth/permission/permission.html', context)


# role list
def Create_Role(request):
    if request.method == 'POST':
        form = AdminRoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role added successfully!')
            return redirect('role_list') 
    else:
        form = AdminRoleForm()
    
    return render(request, 'crm/main/auth/role/create.html', {'form': form})


def Editrole(request, role_id):
    role_instance = get_object_or_404(AdminRole, pk=role_id)
    
    if request.method == 'POST':
        form = AdminRoleForm(request.POST, instance=role_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully!')
            return redirect('role_list') 
    else:
        form = AdminRoleForm(instance=role_instance)

    return render(request, 'crm/main/auth/role/edit.html', {'form': form, 'role': role_instance})


def Role_list(request):
    roles = AdminRole.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        roles = AdminRole.objects.filter(
            Q(role_name__icontains=search_query)
        )
    else:
        roles = AdminRole.objects.all().order_by('-id')
    
    paginator = Paginator(roles, 50)
    
    page_number = request.GET.get('page')
    roles = paginator.get_page(page_number)
    context={'tests': roles}
    return render(request, 'crm/main/auth/role/role.html', context)


def set_permissions(request, perm_id):
    context = {}
    path = Path.objects.filter(status="Active", parent=None)
    context['path'] = path

    addperm = get_object_or_404(AdminRole, id=perm_id)

    if request.method == "POST":
        perm = request.POST.getlist('sub_perm')
        mainperm = request.POST.getlist('main_perm')

        addperm.permissions.clear()
        for perm_id in perm:
            addperm.permissions.add(Path.objects.get(id=perm_id))
        for mainperm_id in mainperm:
            addperm.permissions.add(Path.objects.get(id=mainperm_id))

        messages.success(request, "Permissions added successfully")

        return redirect('role_list')
    permission_ids = [p.id for p in addperm.permissions.all()]
    context['permission'] = permission_ids

    return render(request, 'crm/main/auth/role/set_permission.html', context)
    
# Testimonial_list
def Create_Testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial created successfully.')
            return redirect('testimonial_list')
    else:
        form = TestimonialForm()
    return render(request, 'crm/main/testimonial/create.html', {'form': form})

def Edittestimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('testimonial_list')
    else:
        form = TestimonialForm(instance=testimonial)
        form.fields['test_img'].widget.attrs['required'] = False

    return render(request, 'crm/main/testimonial/edit.html', {'form': form, 'testimonial': testimonial})

def Delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully.')
    return redirect('testimonial_list')

def Testimonial_list(request):
    test = Testimonial.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        test = Testimonial.objects.filter(
            Q(name__icontains=search_query) |  Q(company__icontains=search_query)
        )
    else:
        test = Testimonial.objects.all().order_by('-id')
    
    paginator = Paginator(test, 50)
    
    page_number = request.GET.get('page')
    tests = paginator.get_page(page_number)
    context={'tests': tests}
    return render(request, 'crm/main/testimonial/testimonial.html', context)


# Career_list
def Create_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Career created successfully.')
            return redirect('career_list')
    else:
        form = CareerForm()
    return render(request, 'crm/main/careers/create.html', {'form': form})

def Editcareer(request, career_id):
    careers = get_object_or_404(Career, pk=career_id)
    
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES, instance=careers)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career updated successfully.')
            return redirect('career_list')
    else:
        form = CareerForm(instance=careers)

    return render(request, 'crm/main/careers/edit.html', {'form': form, 'careers': careers})

def Career_list(request):
    careers = Career.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        careers = Career.objects.filter(
            Q(title__icontains=search_query) |  Q(place__icontains=search_query)
        )
    else:
        careers = Career.objects.all().order_by('-updated_at')
    
    paginator = Paginator(careers, 50)
    
    page_number = request.GET.get('page')
    career_p = paginator.get_page(page_number)
    context={'career_p': career_p}
    return render(request, 'crm/main/careers/careers.html', context)

# company_testimonial
def Create_company_testimonial(request):
    if request.method == 'POST':
        form = Company_testimonialForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Company testimonial created successfully.')
            return redirect('company_testimonial_list')
    else:
        form = Company_testimonialForm()
    return render(request, 'crm/main/company_testimonial/create.html', {'form': form})

def Edit_company_testimonial(request, company_testimonial_id):
    company_testimonial = get_object_or_404(Company_testimonial, pk=company_testimonial_id)
    
    if request.method == 'POST':
        form = Company_testimonialForm(request.POST, request.FILES, instance=company_testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company testimonial updated successfully.')
            return redirect('company_testimonial_list')
    else:
        form = Company_testimonialForm(instance=company_testimonial)
        form.fields['com_test_img'].widget.attrs['required'] = False

    return render(request, 'crm/main/company_testimonial/edit.html', {'form': form, 'company_testimonial': company_testimonial})

def Delete_company_testimonial(request, company_testimonial_id):
    company_testimonial = get_object_or_404(Company_testimonial, pk=company_testimonial_id)
    company_testimonial.delete()
    messages.success(request, 'Company testimonial deleted successfully.')
    return redirect('company_testimonial_list')

def Company_testimonial_list(request):
    com_test = Company_testimonial.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        com_test = Company_testimonial.objects.filter(
            Q(name__icontains=search_query) |  Q(position__icontains=search_query)
        )
    else:
        com_test = Company_testimonial.objects.all().order_by('-id')
    
    paginator = Paginator(com_test, 50)
    
    page_number = request.GET.get('page')
    com_tests = paginator.get_page(page_number)
    context={'com_tests': com_tests}
    return render(request, 'crm/main/company_testimonial/company_testimonial.html', context)

# news and events
def Create_news_and_events(request):
    if request.method == 'POST':
        form = News_and_eventsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'News and events created successfully.')
            return redirect('newsevents_list')
    else:
        form = News_and_eventsForm()
    return render(request, 'crm/main/news_and_events/create.html', {'form': form})

def Edit_newsevents(request, newsevent_id):
    news_and_events = get_object_or_404(News_and_events, pk=newsevent_id)
    
    if request.method == 'POST':
        form = News_and_eventsForm(request.POST, request.FILES, instance=news_and_events)
        if form.is_valid():
            form.save()
            messages.success(request, 'News and events updated successfully.')
            return redirect('newsevents_list')
    else:
        form = News_and_eventsForm(instance=news_and_events)
        form.fields['news_img'].widget.attrs['required'] = False

    return render(request, 'crm/main/news_and_events/edit.html', {'form': form, 'news_and_events': news_and_events})

def Delete_newsevents(request, newsevent_id):
    news_and_events = get_object_or_404(News_and_events, pk=newsevent_id)
    news_and_events.delete()
    messages.success(request, 'News and events deleted successfully.')
    return redirect('newsevents_list')

def Newsevents_list(request):
    news_events = News_and_events.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        news_events = News_and_events.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        news_events = News_and_events.objects.all().order_by('-id')
    
    paginator = Paginator(news_events, 50)
    
    page_number = request.GET.get('page')
    
    ne_page = paginator.get_page(page_number)
    context={'ne_page': ne_page}
    return render(request, 'crm/main/news_and_events/news_and_events.html', context)


# calendar
def Create_calendar(request):
    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('calendar_list')
    else:
        form = CalendarForm()
    return render(request, 'crm/main/calendar/create.html', {'form': form})

def Edit_calendar(request, calendar_id):
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    
    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES, instance=calendar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('calendar_list')
    else:
        form = CalendarForm(instance=calendar)
        form.fields['img'].widget.attrs['required'] = False

    return render(request, 'crm/main/calendar/edit.html', {'form': form, 'calendar': calendar})

def Delete_calendar(request, calendar_id):
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    calendar.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('calendar_list')

def Calendar_list(request):
    calendar = Calendar.objects.all().order_by('-date')
    search_query = request.GET.get('search')
    if search_query:
        calendar = Calendar.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        calendar = Calendar.objects.all().order_by('-date')
    
    paginator = Paginator(calendar, 50)
    
    page_number = request.GET.get('page')
    
    ne_page = paginator.get_page(page_number)
    context={'ne_page': ne_page}
    return render(request, 'crm/main/calendar/calendar.html', context)


# gallery
def Create_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery created successfully.')
            return redirect('gallery_list')
    else:
        form = GalleryForm()
    return render(request, 'crm/main/gallery/create.html', {'form': form})

def Edit_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery updated successfully.')
            return redirect('gallery_list')
    else:
        form = GalleryForm(instance=gallery)

    return render(request, 'crm/main/gallery/edit.html', {'form': form, 'gallery': gallery})

def Delete_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    gallery.delete()
    messages.success(request, 'Gallery deleted successfully.')
    return redirect('gallery_list')

def Gallery_list(request):
    gallery = Gallery.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        gallery = Gallery.objects.filter(
            Q(updated_at__icontains=search_query)
        )
    else:
        gallery = Gallery.objects.all().order_by('-id')
    
    paginator = Paginator(gallery, 50)
    
    page_number = request.GET.get('page')
    
    g_page = paginator.get_page(page_number)
    context={'g_page': g_page}
    return render(request, 'crm/main/gallery/gallery.html', context)

# Course
def Create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'crm/main/course/create.html', {'form': form})

def Edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'crm/main/course/edit.html', {'form': form, 'course': course})

def toggle_course_status(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if course.status == 'Active':
        course.status = 'Inactive'
        messages.success(request, f'Course "{course.title}" disabled successfully.')
    else:
        course.status = 'Active'
        messages.success(request, f'Course "{course.title}" enabled successfully.')
    course.save()
    return redirect('course_list')

def Course_list(request):
    course = Course.objects.all().order_by('-from_date')
    search_query = request.GET.get('search')
    if search_query:
        course = Course.objects.filter(
            Q(title__icontains=search_query)
        ).annotate(application_count=Count('schedule_list',filter=Q(schedule_list__status__in=['Pending', 'Accepted','Rejected']))).order_by('-from_date')
    else:
        course = Course.objects.annotate(application_count=Count('schedule_list',filter=Q(schedule_list__status__in=['Pending', 'Accepted','Rejected']))).order_by('-from_date')
    
    paginator = Paginator(course, 50)
    
    page_number = request.GET.get('page')
    
    ne_page = paginator.get_page(page_number)
    context={'ne_page': ne_page}
    return render(request, 'crm/main/course/course.html', context)


def application_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    search_query = request.GET.get('search')
    if search_query:
        applications = Schedule_list.objects.filter(
            course=course
        ).filter(
            Q(status__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).exclude(status='Delete')
    else:
        applications = Schedule_list.objects.filter(course=course).order_by('-created_at').exclude(status='Delete')

    paginator = Paginator(applications, 50)
    page_number = request.GET.get('page')
    ne_page = paginator.get_page(page_number)

    context = {
        'course': course,
        'ne_page': ne_page,
    }
    return render(request, 'crm/main/course/application_list.html', context)


@csrf_exempt
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            schedule_list = Schedule_list.objects.get(id=data["id"])
            schedule_list.status = data["status"]
            schedule_list.save()
            return JsonResponse({"success": True})
        except Schedule_list.DoesNotExist:
            return JsonResponse({"success": False, "error": "Entry not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


def export_csv(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    applications = Schedule_list.objects.filter(course=course).exclude(status='Delete')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{course.title}_applications.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Message', 'Submitted At', 'Status'])

    for application in applications:
        writer.writerow([
            application.first_name,
            application.last_name,
            application.email,
            application.phone,
            application.message,
            application.created_at.strftime('%d-%m-%Y'),
            application.status
        ])

    return response


def generate_pdf(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    applications = Schedule_list.objects.filter(course=course).exclude(status='Delete').annotate(
        custom_order=Case(
            When(status='Pending', then=1),
            When(status='Accepted', then=2),
            When(status='Rejected', then=3),
            default=4,
            output_field=models.IntegerField(),
        )
    ).order_by('custom_order')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{course.title}_applications.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    pdf.title = f"Applications for {course.title}"
    elements = []

    title = [[f"Applications for {course.title} - {course.from_date.strftime('%d-%m-%y')}"]]  # Corrected line
    title_table = Table(title)
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(title_table)
    elements.append(Table([[""]]))

    data = [["Name", "Email", "Phone", "Status"]]

    for app in applications:
        data.append([f"{app.first_name} {app.last_name}", app.email, app.phone, app.status])

    table = Table(data, colWidths=[2.5 * inch, 2 * inch, 1.5 * inch, 1 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#800000")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white)
    ]))

    elements.append(table)

    pdf.build(elements)
    return response

def draw_text_centered(c, text, y, page_width):
    font_size = 18
    font_name = "Helvetica"
    text_width = c.stringWidth(text, font_name, font_size)
    x = (page_width - text_width) / 2
    c.setFont(font_name, font_size)
    c.drawString(x, y, text)

def generate_certificate(schedule, request):
    certificate_template_path = os.path.join(
        BASE_DIR,
        'norpro_app/static/certificate',
        f"{schedule.course.title} Certificate.pdf"
    ).replace('\\', '/')

    certificate_filename = f"{schedule.course.title}_{schedule.first_name}_certificate_{str(uuid.uuid4())[:8]}.pdf"

    overlay_buffer = BytesIO()
    c = canvas.Canvas(overlay_buffer, pagesize=landscape(letter))
    
    page_width = landscape(letter)[0]

    c.setFont("Helvetica", 18)
    first_name = schedule.first_name
    last_name = schedule.last_name
    instructor_name = request.user.name
    course_date = schedule.course.from_date.strftime('%d/%m/%Y')

    full_name = f"{first_name} {last_name}"
    draw_text_centered(c, full_name, 395, page_width)
    c.drawString(135, 120, f"{instructor_name}")
    c.drawString(550, 120, f"{course_date}")
    c.save()

    overlay_buffer.seek(0)
    overlay_pdf = PdfReader(overlay_buffer)

    template_pdf = PdfReader(certificate_template_path)

    output = PdfWriter()
    template_page = template_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]

    template_page.merge_page(overlay_page)
    output.add_page(template_page)

    final_buffer = BytesIO()
    output.write(final_buffer)

    final_buffer.seek(0)
    schedule.Certificate.save(certificate_filename, ContentFile(final_buffer.read()), save=True)

    schedule.certificate_issued = True
    schedule.save()

    final_buffer.seek(0)
    
    certificate_url = request.build_absolute_uri(schedule.Certificate.url)

    # # Prepare the email content
    # email_subject = f"Congratulations, Your Certification for {schedule.course.title} is Ready!"
    # email_message_html = render_to_string('email_request/certificate_send_email.html', {
    #     'course_title': schedule.course.title,
    #     'course_date': schedule.course.from_date.strftime('%d/%m/%Y'),
    #     'first_name': schedule.first_name,
    #     'last_name': schedule.last_name,
    #     'email': schedule.email,
    #     'phone': schedule.phone,
    #     'certificate_url': certificate_url,
    # })

    # email_message = EmailMessage(
    #     email_subject,
    #     email_message_html,
    #     settings.EMAIL_HOST_USER,
    #     [schedule.email],  # Send the email to the participant's email
    # )

    # # Set the content subtype to 'html' to send as HTML
    # email_message.content_subtype = 'html'
    
    # # Attach the certificate PDF
    # email_message.attach(certificate_filename, final_buffer.read(), 'application/pdf')

    # # Send the email
    # email_message.send(fail_silently=False)

    # Return the PDF response to the user
    final_buffer.seek(0)
    return HttpResponse(final_buffer, content_type='application/pdf')


def generate_user_certificate(request, schedule_id):
    schedule = Schedule_list.objects.get(id=schedule_id)
    
    if schedule.status == 'Accepted' and not schedule.certificate_issued:
        generate_certificate(schedule, request)
        messages.success(request, f"The certificate for {schedule.first_name} {schedule.last_name} has been issued successfully.")

    return redirect('application_list', course_id=schedule.course.id)


def download_certificate(request, schedule_id):
    schedule = Schedule_list.objects.get(id=schedule_id)

    certificate_file_path = schedule.Certificate.path
    
    if os.path.exists(certificate_file_path):
        return FileResponse(open(certificate_file_path, 'rb'), as_attachment=True, filename=f"{schedule.course.title}_Certificate.pdf")
    else:
        return HttpResponse("Certificate file not found.", status=404)

# service form
def Service_form(request):
    Service = ServiceForm.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        Service = ServiceForm.objects.filter(
            Q(name__icontains=search_query) | Q(type_service__icontains=search_query) | Q(service__icontains=search_query)
        ).order_by('-created_at')
    else:
        Service = ServiceForm.objects.all().order_by('-created_at')
    
    paginator = Paginator(Service, 50)
    
    page_number = request.GET.get('page')
    
    s_page = paginator.get_page(page_number)
    context={'s_page': s_page}
    return render(request, 'crm/main/service/serviceform.html', context)

def delete_multiple_service_forms(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_service_forms')
        ServiceForm.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected service entry deleted successfully.')
    return redirect('service_form')

# contact form
def Contact_form(request):
    contact = ContactForm.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        contact = ContactForm.objects.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query) | Q(company_name__icontains=search_query)
        ).order_by('-created_at')
    else:
        contact = ContactForm.objects.all().order_by('-created_at')
    
    paginator = Paginator(contact, 50)
    
    page_number = request.GET.get('page')
    
    c_page = paginator.get_page(page_number)
    context={'c_page': c_page}
    return render(request, 'crm/main/contact/contactform.html', context)

def Delete_contact_form(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_contact_forms')
        ContactForm.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected contact entry deleted successfully.')
    return redirect('contact_form')

# career form
def Page_career(request):
    formcareer = FormCareer.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        formcareer = FormCareer.objects.filter(
           Q(type_career__icontains=search_query)
        ).order_by('-created_at')
    else:
        formcareer = FormCareer.objects.all().order_by('-created_at')
    
    paginator = Paginator(formcareer, 50)
    
    page_number = request.GET.get('page')
    
    carpage = paginator.get_page(page_number)
    context={'carpage': carpage}
    return render(request, 'crm/main/careerform/careerform.html', context)

def Delete_formcareer(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_career_forms')
        FormCareer.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected career entry deleted successfully.')
    return redirect('formcareer')


#academy form
def Academy_form(request):
    academy = Academy.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        academy = Academy.objects.filter(
           Q(first_name__icontains=search_query) |  Q(last_name__icontains=search_query)
        ).order_by('-created_at')
    else:
        academy = Academy.objects.all().order_by('-created_at')
    
    paginator = Paginator(academy, 50)
    
    page_number = request.GET.get('page')
    
    acpage = paginator.get_page(page_number)
    context={'acpage': acpage}
    return render(request, 'crm/main/academy/academy.html', context)


def Delete_academy_form(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_academy_forms')
        Academy.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected academy entry deleted successfully.')
    return redirect('academy_form')


#Employee referral form
def Form_employee_referral(request):
    employee_referral = Employee_referral_program.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        employee_referral = Employee_referral_program.objects.filter(
           Q(first_name__icontains=search_query) |  Q(last_name__icontains=search_query) | 
            Q(email__icontains=search_query) |  Q(phone__icontains=search_query) |
              Q(referal_first_name__icontains=search_query) |  Q(referal_last_name__icontains=search_query) | 
                Q(referal_email__icontains=search_query) |  Q(referal_phone__icontains=search_query)
           
        ).order_by('-created_at')
    else:
        employee_referral = Employee_referral_program.objects.all().order_by('-created_at')
    
    paginator = Paginator(employee_referral, 50)
    
    page_number = request.GET.get('page')
    
    acpage = paginator.get_page(page_number)
    context={'acpage': acpage}
    return render(request, 'crm/main/employee_referral/employee_referral.html', context)


def Delete_employee_referral_form(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_employee_referral_forms')
        Employee_referral_program.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected employee referral entry deleted successfully.')
    return redirect('employee_referral_form')


def employee_referral_form_details(request, employee_referral_id):
    
    employee_referral = get_object_or_404(Employee_referral_program, pk=employee_referral_id)
    
    return render(request, 'crm/main/employee_referral/employee_referral_detail.html', {'employee_referral': employee_referral})



# Teams_list
def Create_Teams(request):
    if request.method == 'POST':
        form = TeamsForm(request.POST, request.FILES)

        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            form.save_m2m()
            qr_code_image = generate_qrcode(instance)
            instance.qr_code.save(f'qr_code_{instance.name}.png', ContentFile(qr_code_image.getvalue()), save=False)
            instance.save()
            messages.success(request, 'Id card created successfully.')
            return redirect('teams_list')
    else:
        form = TeamsForm()
    return render(request, 'crm/main/teams/create.html', {'form': form})

def EditTeams(request, teams_id):
    teams = get_object_or_404(id_card, pk=teams_id)
    
    if request.method == 'POST':
        form = TeamsForm(request.POST, request.FILES, instance=teams)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            form.save_m2m()
            qr_code_image = generate_qrcode(instance)
            instance.qr_code.save(f'qr_code_{instance.name}.png', ContentFile(qr_code_image.getvalue()), save=False)
            instance.save()
            messages.success(request, 'Id card updated successfully.')
            return redirect('teams_list')
    else:
        form = TeamsForm(instance=teams)
        form.fields['image'].widget.attrs['required'] = False

    return render(request, 'crm/main/teams/edit.html', {'form': form, 'teams': teams})


def deleteteams(request, teams_id):
    teams = get_object_or_404(id_card, pk=teams_id)
    if teams.user:  # Check if a user exists
        teams.user.delete()  # Delete the associated user
    teams.delete()
    messages.success(request, 'Id card deleted successfully.')
    return redirect('teams_list')

def teams_list(request):
    test = id_card.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        test = id_card.objects.filter(
            Q(name__icontains=search_query) |  Q(title__icontains=search_query) | Q(phone_number__icontains=search_query) | Q(user__email__icontains=search_query)
        )
    else:
        test = id_card.objects.all().order_by('-id')
    
    paginator = Paginator(test, 50)
    
    page_number = request.GET.get('page')
    tests = paginator.get_page(page_number)
    context={'tests': tests}
    return render(request, 'crm/main/teams/teams.html', context)


# qrcode
from PIL import Image
from norpro_security.settings import BASE_DIR
import os
def generate_qrcode(user):
    today_date=datetime.today()
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # url = request.GET.get('url')
    # username = request.GET.get('username')
    url = f'https://norpro.ca/id_card/{user.slug}'
    print(url,'url')
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="#0d223f", back_color="white")

    '''commented below code to download to system and changed it to save to database'''
    # # Save the image or return it as HttpResponse
    # response = HttpResponse(content_type="image/png")
    # response['Content-Disposition'] = f'attachment; filename="qr_code_{username}_{today_date}.png"'
    # img.save(response, "PNG")
    # return response
    # Open the image to be added in the center
    center_image_path = os.path.join(BASE_DIR, 'norpro_app/static/logo/new-logos-qrcode.png')
    center_image = Image.open(center_image_path)
    new_size = (50, 50)
    center_image = center_image.resize(new_size)

    # Calculate the position to place the center image in the middle of the QR code
    position = ((img.size[0] - center_image.size[0]) // 2, (img.size[1] - center_image.size[1]) // 2)

    # Paste the center image onto the QR code
    img.paste(center_image, position, center_image)
    # Save the image to BytesIO buffer
    image_buffer = BytesIO()
    img.save(image_buffer, format="PNG")

    return image_buffer

# qrcode
def Create_qrcode(request):
    test = qr_code.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        test = qr_code.objects.filter(
            Q(link__icontains=search_query)
        )
    else:
        test = qr_code.objects.all().order_by('-id')
    
    paginator = Paginator(test, 50)
    
    page_number = request.GET.get('page')
    tests = paginator.get_page(page_number)
    if request.method == 'POST':
        form = QrcodeForm(request.POST, request.FILES)

        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            qr_code_image = custome_generate_qrcode(instance)
            today_date = datetime.today()
            filename = f'qr_code_{today_date}.png'
            instance.qr_code.save(filename, ContentFile(qr_code_image.getvalue()), save=False)
            instance.save()
            # Download the QR code image
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            qr_code_image.seek(0)
            response.write(qr_code_image.read())
            messages.success(request, 'QR code successfully created!')
            return response
        else:
            messages.error(request, 'Form is not valid. Please check the input.')

            # messages.success(request, 'QR code successfully created!')
            # return redirect('Create_qrcode')
    else:
        form = QrcodeForm()
    context={'form': form, 'tests': tests}
    return render(request, 'crm/main/qrcode/create.html',context)

def delete_qr_code(request, qrcode_id):
    qrcodes = get_object_or_404(qr_code, pk=qrcode_id)
    qrcodes.delete()
    messages.success(request, 'QR code deleted successfully.')
    return redirect('Create_qrcode')

def custome_generate_qrcode(instance):
    today_date = datetime.today()

    # Access the link from the instance
    link = instance.link
    print(link, 'url')

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    url = link

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="#0d223f", back_color="white")

    # Open the image to be added in the center
    center_image_path = os.path.join(BASE_DIR, 'norpro_app/static/logo/new-logos-qrcode.png')
    center_image = Image.open(center_image_path)
    new_size = (50, 50)
    center_image = center_image.resize(new_size)

    # Calculate the position to place the center image in the middle of the QR code
    position = ((img.size[0] - center_image.size[0]) // 2, (img.size[1] - center_image.size[1]) // 2)

    # Paste the center image onto the QR code
    img.paste(center_image, position, center_image)
    # Save the image to BytesIO buffer
    image_buffer = BytesIO()
    img.save(image_buffer, format="PNG")

    return image_buffer

#### Norpro Alert App ####

# Department_list
def Create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'crm/main/department/create.html', {'form': form})

def Editdepartment(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'crm/main/department/edit.html', {'form': form, 'department': department})

def Department_list(request):
    department = Department.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        department = Department.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        department = Department.objects.all().order_by('-updated_at')
    
    paginator = Paginator(department, 50)
    
    page_number = request.GET.get('page')
    department_p = paginator.get_page(page_number)
    context={'department_p': department_p}
    return render(request, 'crm/main/department/department.html', context)


# Alert_list
def Create_alert(request):
    if request.method == 'POST':
        form = AlertsForm(request.POST, request.FILES)
        print("fomrrrrrrr")
        if form.is_valid():
            alert = form.save(commit=False)
            alert.created_by = request.user
            alert.save()
            form.save_m2m()

            # Reload the alert instance to access ManyToMany fields
            # alert.refresh_from_db()

            # Find users with matching departments
            if alert.status == 1 and (not alert.Expire_date or alert.Expire_date >= now().date()):
                # Find users with matching departments
                teams = id_card.objects.filter(department__in=alert.department.all(),user__status="Active").distinct()
                for team in teams:
                    print(team.name, team.user.status, "← status of user")
                
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"alert",
                            "fcm_token": team.fcm_token,
                            "title": alert.heading,
                            "description": alert.description,
                            }
                        )

            messages.success(request, 'Alert created successfully.')
            return redirect('alert_list')
    else:
        form = AlertsForm()
    return render(request, 'crm/main/alert/create.html', {'form': form})

def Editalert(request, alert_id):
    alert = get_object_or_404(Alerts, pk=alert_id)
    
    if request.method == 'POST':
        form = AlertsForm(request.POST, request.FILES, instance=alert)
        if form.is_valid():
            form.save()
            
            if alert.status == 1 and (not alert.Expire_date or alert.Expire_date >= now().date()):
                teams = id_card.objects.filter(department__in=alert.department.all(),user__status="Active").distinct()
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"alert",
                            "fcm_token": team.fcm_token,
                            "title": alert.heading,
                            "description": alert.description,
                            }
                        )



            messages.success(request, 'Alert updated successfully.')
            return redirect('alert_list')
    else:
        form = AlertsForm(instance=alert)

    return render(request, 'crm/main/alert/edit.html', {'form': form, 'alert': alert})

def Alert_list(request):
    alert = Alerts.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        alert = Alerts.objects.filter(
            Q(heading__icontains=search_query) | Q(department__title__icontains=search_query)
        )
    else:
        alert = Alerts.objects.all().order_by('-updated_at')
    
    paginator = Paginator(alert, 50)
    
    page_number = request.GET.get('page')
    alert_p = paginator.get_page(page_number)
    context={'alert_p': alert_p}
    return render(request, 'crm/main/alert/alert.html', context)


# Announcement_list
def Create_announcement(request):
    
    if request.method == 'POST':
        print("post:",request.POST)
        form = AnnouncementForm(request.POST, request.FILES)

        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            form.save_m2m()
            Announcement_files = request.FILES.getlist('Announcement_files') 
            for files in Announcement_files:
                AnnouncementFile.objects.create(announcement=announcement, file=files)

            # Create notifications only if announcement is active and not expired
            if announcement.status == 1 and (not announcement.Expire_date or announcement.Expire_date >= now().date()):
                teams = id_card.objects.filter(department__in=announcement.department.all(),user__status="Active").distinct()
                
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"announcement",
                            "fcm_token": team.fcm_token,
                            "title": announcement.heading,
                            "description": announcement.description,
                            "image": announcement.image.url if announcement.image else None  # Ensure the image is properly formatted
                            }
                        )

            
            messages.success(request, 'Announcement created successfully.')
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
        
    return render(request, 'crm/main/announcement/create.html', {'form': form})

def Editannouncement(request, announcement_id):
    announcement = get_object_or_404(Announcement.objects.prefetch_related('files'), pk=announcement_id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():     
            announcement = form.save()
            Announcement_files = request.FILES.getlist('Announcement_files') 
            for files in Announcement_files:
                AnnouncementFile.objects.create(announcement=announcement, file=files)
            
            deleted_files_ids = request.POST.get('deleted_files_ids', '').split(',')
            
            # Convert the deleted images IDs into integers
            deleted_files_ids = [int(id) for id in deleted_files_ids if id.strip().isdigit()]
            
            if deleted_files_ids:
                AnnouncementFile.objects.filter(id__in=deleted_files_ids).delete()

            if announcement.status == 1 and (not announcement.Expire_date or announcement.Expire_date >= now().date()):
                teams = id_card.objects.filter(department__in=announcement.department.all(),user__status="Active").distinct()
                
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                             data={
                            "type":"announcement",
                            "fcm_token": team.fcm_token,
                            "title": announcement.heading,
                            "description": announcement.description,
                            "image": announcement.image.url if announcement.image else None  # Ensure the image is properly formatted
                            }
                        )
                
            messages.success(request, 'Announcement updated successfully.')
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
        
    file_icons = []
    for file in announcement.files.all():
        file_type = file.file.name.split('.')[-1].lower()
        file_icons.append({
            'file': file,
            'icon': get_file_icon(file_type)
        })
    print('file_icons: ',file_icons)

    return render(request, 'crm/main/announcement/edit.html', {'form': form, 'announcement': announcement, 'file_icons': file_icons})

def get_file_icon(file_type):
    file_icons = {
        'pdf': 'crm/assets/img/icon/pdf.svg',
        'txt': 'crm/assets/img/icon/txt.svg',
        'docx': 'crm/assets/img/icon/docx.svg',
        'csv': 'crm/assets/img/icon/csv.svg',
        'xlsx': 'crm/assets/img/icon/xlsx.svg',
        'rtf': 'crm/assets/img/icon/rtf.svg',
        'zip': 'crm/assets/img/icon/zip.svg',
    }
    return file_icons.get(file_type, 'crm/assets/img/icon/file.svg')


def Announcement_list(request):
    announcement = Announcement.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        announcement = Announcement.objects.filter(
            Q(heading__icontains=search_query) | Q(department__title__icontains=search_query)
        )
    else:
        announcement = Announcement.objects.all().order_by('-updated_at')
    
    paginator = Paginator(announcement, 50)
    
    page_number = request.GET.get('page')
    announcement_p = paginator.get_page(page_number)
    context={'announcement_p': announcement_p}
    return render(request, 'crm/main/announcement/announcement.html', context)


# Banner_list
def Create_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)

        if form.is_valid():
            banner = form.save(commit=False)
            banner.created_by = request.user
            banner.save()
            form.save_m2m()

            if banner.status == 1 and (not banner.Expire_date or banner.Expire_date >= now().date()):
                teams = id_card.objects.filter(department__in=banner.department.all(),user__status="Active").distinct()
                
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"banner",
                            "fcm_token": team.fcm_token,
                            "title": banner.title,
                            "image": banner.image.url if banner.image else None  # Ensure the image is properly formatted
                            }
                            
                        )


            messages.success(request, 'Banner created successfully.')
            return redirect('banner_list')
    else:
        form = BannerForm()
    return render(request, 'crm/main/greeting_banner/create.html', {'form': form})

def Editbanner(request, banner_id):
    banner = get_object_or_404(Greeting_banner, pk=banner_id)
    
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()

            if banner.status == 1 and (not banner.Expire_date or banner.Expire_date >= now().date()):
                teams = id_card.objects.filter(department__in=banner.department.all(),user__status="Active").distinct()
                print("00000000000000000",teams)
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                             data={
                            "type":"banner",
                            "fcm_token": team.fcm_token,
                            "title": banner.title,
                            "image": banner.image.url if banner.image else None  # Ensure the image is properly formatted
                            }
                            
                        )

            messages.success(request, 'Banner updated successfully.')
            return redirect('banner_list')
    else:
        form = BannerForm(instance=banner)

    return render(request, 'crm/main/greeting_banner/edit.html', {'form': form, 'banner': banner})

def Banner_list(request):
    Banner = Greeting_banner.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        Banner = Greeting_banner.objects.filter(
            Q(title__icontains=search_query) | Q(department__title__icontains=search_query)
        )
    else:
        Banner = Greeting_banner.objects.all().order_by('-updated_at')
    
    paginator = Paginator(Banner, 50)
    
    page_number = request.GET.get('page')
    banner_p = paginator.get_page(page_number)
    context={'banner_p': banner_p}
    return render(request, 'crm/main/greeting_banner/greeting_banner.html', context)


# News_list
def Create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.save()
            form.save_m2m()

            if news.status == 1 :
                teams = id_card.objects.filter(department__in=news.department.all(),user__status="Active").distinct()
                print("00000000000000000",teams)
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"news",
                            "fcm_token": team.fcm_token,
                            "title": news.heading,
                            "description": news.description,
                            "image": news.image.url if news.image else None  # Ensure the image is properly formatted
                            }
                            
                        )

            messages.success(request, 'News created successfully.')
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'crm/main/news/create.html', {'form': form})

def Editnews(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()

            if news.status == 1 :
                teams = id_card.objects.filter(department__in=news.department.all(),user__status="Active").distinct()
                print("00000000000000000",teams)
                for team in teams:
                    if team.fcm_token:
                        NotificationPool.objects.create(
                            team=team,
                            data={
                            "type":"news",
                            "fcm_token": team.fcm_token,
                            "title": news.heading,
                            "description": news.description,
                            "image": news.image.url if news.image else None  # Ensure the image is properly formatted
                            }
                                                
                        )


            messages.success(request, 'News updated successfully.')
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)

    return render(request, 'crm/main/news/edit.html', {'form': form, 'news': news})

def News_list(request):
    news = News.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        news = News.objects.filter(
            Q(heading__icontains=search_query) | Q(department__title__icontains=search_query)
        )
    else:
        news = News.objects.all().order_by('-updated_at')
    
    paginator = Paginator(news, 50)
    
    page_number = request.GET.get('page')
    news_p = paginator.get_page(page_number)
    context={'news_p': news_p}
    return render(request, 'crm/main/news/news.html', context)
