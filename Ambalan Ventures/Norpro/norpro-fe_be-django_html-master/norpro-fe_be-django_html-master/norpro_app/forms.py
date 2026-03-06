from django import forms
from .models import *
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import PasswordChangeForm
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth.hashers import make_password
import random
import string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# user and permission 

class PathForm(forms.ModelForm):
    class Meta:
        model = Path
        fields = ['path_name', 'status', 'parent'] 

        widgets = {
            'path_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Path Name'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }
        

class AdminRoleForm(forms.ModelForm):
    class Meta:
        model = AdminRole
        fields = ['role_name', 'status', 'permissions']  

        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Role Name'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'permissions': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), 
        }


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'required': 'required', 
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        })
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'required': 'required', 
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'required': 'required', 
            'placeholder': 'Username',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = AdminUser
        fields = ['name','username', 'email', 'user_type', 'status', 'role', 'password', 'password_confirm']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Email'}),
            'user_type': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        
class AdminUserEditForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Username',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = AdminUser
        fields = ['name','username', 'email', 'user_type', 'status', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Email'}),
            'user_type': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Old Password',
            'autocomplete': 'current-password',
        }),
    )
    
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'autocomplete': 'new-password',
        }),
    )
    
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password',
        }),
    )
    
class SimplifiedPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password')  # Remove the old_password field
    
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'autocomplete': 'new-password',
        }),
    )
    
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password',
        }),
    )
    
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'company', 'feedback', 'test_img']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Name'}),
            'company' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Company'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'required':'required','rows': 6}),
            'test_img' : forms.ClearableFileInput(attrs={'class': 'form-control', 'required':'required'}),
        }
        
class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['title', 'description', 'schedule', 'licence_certification', 'responsibilities', 'qualifications', 'expect', 'place', 'place_2', 'status']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'schedule': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'licence_certification': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'expect': forms.Textarea(attrs={'rows': 3, 'cols': 110, 'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'place'}),
            'place_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Second place'}),
            'status' : forms.Select(attrs={'class': 'form-control', 'required':'required'}),
        }
        
class Company_testimonialForm(forms.ModelForm):
    class Meta:
        model = Company_testimonial
        fields = ['name', 'position', 'feedback', 'com_test_img']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Name'}),
            'position' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'position'}),
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 110, 'class': 'form-control'}),
            'com_test_img' : forms.ClearableFileInput(attrs={'class': 'form-control', 'required':'required'}),
        }
        

class News_and_eventsForm(forms.ModelForm):
    class Meta:
        model = News_and_events
        fields = ['title', 'date', 'description', 'news_img', 'banner_image']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'title'}),
            'description': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'news_img' : forms.ClearableFileInput(attrs={'class': 'form-control', 'required':'required'}),
            'banner_image' : forms.ClearableFileInput(attrs={'class': 'form-control', 'required':'required'}),
        }
        
        
class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'date', 'description', 'img','start_time', 'end_time']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'title'}),
            'description': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'img' : forms.ClearableFileInput(attrs={'class': 'form-control',}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
        }
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'from_date', 'to_date', 'start_time','end_time', 'price', 'place','status']

        widgets = {
            'title' : forms.Select(attrs={'class': 'form-control', 'required':'required', 'placeholder':'title'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Price'}),
            'place' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Place'}),
            'status' : forms.Select(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Status'}),
        }
class CourseFormForm(forms.ModelForm):
    class Meta:
        model = Schedule_list
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']
        
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email',}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Phone'}))
    message = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
            

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', 'video']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'rows': 4, 'cols': 100}),
            'video': forms.URLInput(attrs={'class': 'form-control','placeholder': 'Add Video URL'}),
        }

class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'company_name', 'phone', 'subject', 'message']

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    company_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone'}))
    subject = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Mine Security', 'Mine Security'),
            ('Industrial guards', 'Industrial guards'),
            ('Institutional guards', 'Institutional guards'),
            ('Patrol', 'Patrol'),
            ('Health and Safety', 'Health and Safety'),
            ('Other Services', 'Other Services'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'rows': 4}))
    
    
class MineForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Medical First Responder', 'Medical First Responder'),
            ('Screening and Testing', 'Screening and Testing'),
            ('Vehicle Search', 'Vehicle Search'),
            ('Access Control', 'Access Control'),
            ('Precious metal detection', 'Precious metal detection'),
            ('X-ray machine operations', 'X-ray machine operations'),
            ('Drug and alcohol detection', 'Drug and alcohol detection'),
            ('Testing and administration', 'Testing and administration'),
            ('Vehicle patrolling', 'Vehicle patrolling'),
            ('LIDAR speed control', 'LIDAR speed control'),
            ('RFID tracking and reporting', 'RFID tracking and reporting'),
            ('Live monitoring', 'Live monitoring'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Mine Security')


class Mobile_patrolForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Keyholder services', 'Keyholder services'),
            ('Alarm response', 'Alarm response'),
            ('Spot checks', 'Spot checks'),
            ('Parking lot patrol', 'Parking lot patrol'),
            ('Checking windows and doors', 'Checking windows and doors'),
            ('Emergency Responses', 'Emergency Responses'),
            ('Perimeter Sweeps', 'Perimeter Sweeps'),
            ('By-law enforcement', 'By-law enforcement'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Patrol')
    

class Industrial_guardsForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Site access control', 'Site access control'),
            ('Drug and alochol detection', 'Drug and alochol detection'),
            ('Testing and administration', 'Testing and administration'),
            ('Foot patrol', 'Foot patrol'),
            ('Vehicle searches', 'Vehicle searches'),
            ('Asset protection', 'Asset protection'),
            ('Monitor entrances and exits', 'Monitor entrances and exits'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Industrial Guards')

class Static_guards_and_event_managementForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Crowd control', 'Crowd control'),
            ('Event management and security', 'Event management and security'),
            ('Hotel security', 'Hotel security'),
            ('First Nations Gatherings Coordination', 'First Nations Gatherings Coordination'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Static Guards & Event Management')

class Institutional_guardsForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Emergency code response', 'Emergency code response'),
            ('Hostile patient response', 'Hostile patient response'),
            ('Perimeter Control', 'Perimeter Control'),
            ('Conflict resolution', 'Conflict resolution'),
            ('Security patrols', 'Security patrols'),
            ('ASurveilance', 'Surveilance'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Institutional guards')
    
    
class Loss_preventionForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Retail', 'Retail'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Loss Prevention')
    
    
class Other_serviceForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'service', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    service = forms.ChoiceField(
        choices=(
            ('', 'Select Service'),
            ('Cash in transit', 'Cash in transit'),
            ('Samsara', 'Samsara'),
            ('Guarda: Live Monitoring', 'Guarda: Live Monitoring'),
        ),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);background: #272727;'}),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Other services')
    
# career
class CareerformForm(forms.ModelForm):
    
    class Meta:
        model = FormCareer
        fields = ['first_name', 'last_name', 'email', 'phone', 'resume', 'cover_letter', 'other_documents', 'type_career']
        
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone'}))
    resume = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'placeholder': 'Resume'}))
    cover_letter = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'placeholder': 'Cover Letter'}))
    other_documents = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'placeholder': 'Other Documents'}))
    type_career = forms.CharField(widget=forms.HiddenInput(), initial='general')
    
    def clean_file_field(self, field_name):
        file_upload = self.cleaned_data.get(field_name)

        # Check file type
        if file_upload:
            content_type = file_upload.content_type
            allowed_types = ('application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            if not content_type.startswith(allowed_types):
                raise ValidationError(f'{field_name.capitalize()} type not supported. Please upload a PDF, DOC, or DOCX file.')

        # Check file size
        if file_upload and file_upload.size > 30 * 1024 * 1024:  # Adjust the file size limit as needed (here, 10 MB)
            raise ValidationError(f'{field_name.capitalize()} size must be no more than 30 MB.')

        return file_upload

    def clean_resume(self):
        return self.clean_file_field('resume')

    def clean_cover_letter(self):
        return self.clean_file_field('cover_letter')

    def clean_other_documents(self):
        return self.clean_file_field('other_documents')
    
    

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ['first_name', 'last_name', 'email', 'phone', 'file_upload']

    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone'}))
    file_upload = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'placeholder': 'Other Documents'}))
    
    def clean_file_upload(self):
        file_upload = self.cleaned_data.get('file_upload')

        # Check file type
        if file_upload:
            content_type = file_upload.content_type
            if not content_type.startswith(('application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')):
                raise ValidationError('File type not supported. Please upload a PDF, DOC, or DOCX file.')

        # Check file size
        if file_upload and file_upload.size > 30 * 1024 * 1024:  # Adjust the file size limit as needed (here, 10 MB)
            raise ValidationError('File size must be no more than 30 MB.')

        return file_upload
    
    

# Health & Safety Services

class Assessment_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Assessment)')
    
class Auditing_and_program_management_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Auditing & program management)')
    
    
    
class Respirator_fit_testing_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Respirator fit testing)')
    
    
    
class Program_development_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Program development)')
    
    
class Training_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Training)')
    
class Designated_substances_support_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Designated substances support)')
    
    
class Support_services_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Support Services)')
    
    
class management_system_implementation_and_auditing_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Management System Implementation & Auditing)')
    
    
class hazardous_materials_testing_management_and_remediation_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Hazardous Materials Testing, Management & Remediation)')
    
    
class indoor_air_quality_assessment_services_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Indoor Air Quality (IAQ) Assessment Services)')
    
    
class workplace_noise_assessments_Form(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'email', 'phone', 'location', 'type_service', 'message',]

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Message', 'rows': 4}))
    type_service = forms.CharField(widget=forms.HiddenInput(), initial='Health & Safety (Workplace Noise Assessments)')
    
    
    
class TeamsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Email'}))
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'})
    )
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}))
    class Meta:
        model = id_card
        fields = ['name', 'title', 'phone_number', 'bio', 'linkedin','image', 'department', 'show_in_home']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Name'}),
            'title' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Position'}),
            'phone_number': forms.Textarea(attrs={'class': 'form-control', 'required':'required','rows': 3}),
            # 'email' : forms.EmailInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control','rows': 6}),
            'linkedin' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Linkedin'}),
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control', 'required':'required'}),
            'department': Select2MultipleWidget(attrs={'class': 'form-control'}),
            'show_in_home' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'password' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password','autocomplete': 'new-password'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prepopulate email field if editing an existing instance
        if self.instance and self.instance.pk:
            if self.instance.user:  # Check if user exists
                self.fields['email'].initial = self.instance.user.email
                self.fields['status'].initial = 'active' if self.instance.user.status=="Active" else 'inactive'
            else:
                self.fields['email'].initial = ''  # Provide an empty default value
                self.fields['status'].initial = 'active'  # Default to inactive if user is missing


            # self.fields['password'].required = False  
    def save(self, commit=True):
        # Create user first
        id_card_instance = super().save(commit=False)
        email = self.cleaned_data['email']
        # password = self.cleaned_data['password']
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(password,'checkpassword')
        name = self.cleaned_data.get('name', '')
        status = self.cleaned_data['status']

        # Check if the user already exists

        if self.instance and self.instance.pk:
            user = self.instance.user
            user.email = email
            user.username = email
            user.name = name
            user.status = "Active" if status == 'active' else "Inactive"
            user.save()
        else:
            user, created = User.objects.get_or_create(username=email, defaults={
                'email': email,
                # 'password': make_password(password)  # Hash the password before saving Todo
                'user_type':'Team',
                'name': name,
                'status': "Active" if status == 'active' else "Inactive"  # Set user active/inactive

            })
            if created:
                user.set_password("12345")  # Correct way to hash password
                user.save()
        id_card_instance.user = user

        if commit:
            id_card_instance.save()
            self.save_m2m()  # Save many-to-many fields
        print("not create")
        # if created:
        #     print("created")
            # self.send_welcome_email(email,name,password,"https://norpro-announcements-fe-nextjs.vercel.app/login") Todoo

        return id_card_instance   
    
    def send_welcome_email(self,user_email, user_name,user_password, activation_link):
            subject = "Welcome to Our Platform"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email]
            print("000000000000000000000000000")

            # Render the HTML template with dynamic data
            html_content = render_to_string("email_request/send_password.html", {
                "user_name": user_name,
                "user_email":user_email,
                "user_password":user_password,
                "activation_link": activation_link
            })
            text_content = strip_tags(html_content)  # Remove HTML tags for plain text

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")  # Attach HTML version
            email.send()
            print("send emaillllllllllllllllllllllll")

        # Example Usage
    
class QrcodeForm(forms.ModelForm):
    
    class Meta:
        model = qr_code
        fields = ['link', 'qr_code']

        widgets = {
            'link': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Link'}),
            'qr_code': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title', 'status']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'title'}),
            'status' : forms.Select(attrs={'class': 'form-control', 'required':'required'}),
        }
        
        
class AlertsForm(forms.ModelForm):
    class Meta:
        model = Alerts
        fields = ['heading', 'description', 'alert_type', 'department', 'status', 'Expire_date'] 

        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Alert Heading'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Alert Description', 'rows': 4}),
            'alert_type': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'department': Select2MultipleWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'Expire_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
        }
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['heading', 'description', 'department', 'image', 'status', 'Expire_date']

        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Announcement Heading'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Announcement Description', 'rows': 4}),
            'department': Select2MultipleWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'Expire_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Greeting_banner
        fields = ['title', 'department', 'image', 'status', 'Expire_date', 'link'] 

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Banner Title'}),
            'department': Select2MultipleWidget(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'Expire_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter link URL'})
        }
        
        
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['heading', 'description', 'department', 'image', 'status'] 

        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'News Heading'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'News Description', 'rows': 4}),
            'department': Select2MultipleWidget(attrs={'class': 'form-control',}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        }