from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import get_user_model





class AdminUserManager(BaseUserManager):
    """Manager for Admin User."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a user with an email and username."""
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        username = email.split('@')[0]
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class Path(models.Model):
    path_name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="Active", choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ))
    parent = models.ForeignKey('Path', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Path'

    def __str__(self):
        return self.path_name

class AdminRole(models.Model): 
    role_name = models.CharField(max_length=100)
    stat_choice = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    status = models.BooleanField(default=True, choices=stat_choice)
    permissions = models.ManyToManyField(Path, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role_name    

class AdminUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(default='Employee', max_length=20, null=True, choices=(
        ('Employee', 'Employee'),
        ('Admin', 'Admin'),
        ('Team', 'Team'),
    ))
    status = models.CharField(default='Active', max_length=20, choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ))
    role = models.ForeignKey(AdminRole, on_delete=models.CASCADE, null=True, blank=True)
    changed_pwd=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AdminUserManager() 

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='adminuser_set', 
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='adminuser_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    def __str__(self):
        return self.username

    def has_permission(self, permission_name):
        """Check if the user has a specific permission."""
        if self.is_superuser:
            return True
        if self.role:
            return permission_name in [perm.path_name for perm in self.role.permissions.all()]
        return False
    
    
# Create your models here.
class Testimonial(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    test_img = models.ImageField(upload_to="testimonial_images")
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    
class Career(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    schedule = RichTextField(null=True, blank=True)
    licence_certification = RichTextField(null=True, blank=True)
    responsibilities = RichTextField(null=True, blank=True)
    qualifications = RichTextField(null=True, blank=True)
    expect = RichTextField(null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    place_2 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
class Company_testimonial(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    com_test_img = models.ImageField(upload_to="Company_testimonial_images")
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    
class News_and_events(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    news_img = models.ImageField(upload_to="news_and_events_images")
    banner_image = models.FileField(upload_to="news_and_events_banner_images", blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    

class Gallery(models.Model):
    image = models.FileField(upload_to="Gallery_images", blank=True)
    video = EmbedVideoField(blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    
    
   
        
class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class ServiceForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    type_service = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class FormCareer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def resume_path(instance, filename):
        random_value = str(uuid.uuid4())[:8] 
        file_extension = filename.split('.')[-1]
        return f'{instance.first_name}_{instance.last_name}_resume_{random_value}.{file_extension}'
    def cover_letter_path(instance, filename):
        random_value = str(uuid.uuid4())[:8] 
        file_extension = filename.split('.')[-1]
        return f'{instance.first_name}_{instance.last_name}_cover_letter_{random_value}.{file_extension}'
    def other_documents_path(instance, filename):
        random_value = str(uuid.uuid4())[:8] 
        file_extension = filename.split('.')[-1]
        return f'{instance.first_name}_{instance.last_name}_other_documents_{random_value}.{file_extension}'
    
    resume = models.FileField(upload_to=resume_path)
    cover_letter = models.FileField(upload_to=cover_letter_path)
    other_documents = models.FileField(upload_to=other_documents_path)
    type_career = models.CharField(max_length=100, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
         
class Academy(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def file_upload_path(instance, filename):
        random_value = str(uuid.uuid4())[:8] 
        file_extension = filename.split('.')[-1]
        return f'{instance.first_name}_{instance.last_name}_{random_value}.{file_extension}'
    
    file_upload = models.FileField(upload_to=file_upload_path)  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    
class Employee_referral_program(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    referal_first_name = models.CharField(max_length=200)
    referal_last_name = models.CharField(max_length=200)
    referal_email = models.EmailField()
    referal_phone = models.CharField(max_length=15, blank=True, null=True)
    referral_reason=models.TextField()
    have_security_guard_license=models.BooleanField(null=True,blank=True,default=False)
    have_drivers_license=models.BooleanField(null=True,blank=True,default=False)
    # gift_cards = models.ManyToManyField(GiftCard, blank=True)
    # gc_president_choice=models.BooleanField(null=True,blank=True,default=False)
    # gc_the_marconi=models.BooleanField(null=True,blank=True,default=False)
    # gc_canadian_tire=models.BooleanField(null=True,blank=True,default=False)
    # gc_esso_gas_card=models.BooleanField(null=True,blank=True,default=False)
    status=models.CharField(max_length=100,null=True,blank=True,choices=(('Active','Active'),('Inactive','Inactive')),default='Active')
    created_at = models.DateTimeField(auto_now_add=True) 

class Department(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
    def __str__(self):
        return self.title
User = get_user_model() 
class id_card(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    # email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="id_card_img", blank=True)
    qr_code = models.ImageField(upload_to="qr_code")
    linkedin = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=250,blank=True,null=True)
    show_in_home = models.BooleanField(default=False)
    department = models.ManyToManyField(Department, blank=True)
    created_at = models.DateTimeField("Created at", default=now, blank=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    fcm_token=models.CharField(max_length=255,blank=True,null=True)
    # password = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)  
        
        super().save(*args, **kwargs)
        
        

class qr_code(models.Model):
    link = models.CharField(max_length=250, blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_code_image",blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)                                  
    
    
class Calendar(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="events_images",blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    
    
class Course(models.Model):
    TITLE_CHOICES = [
        ('Lead Class 1 Operations Worker Training', 'Lead Class 1 Operations Worker Training'),
        ('Lead Hazard Awareness Training', 'Lead Hazard Awareness Training'),
        ('Type 1 & 2 Asbestos Operations Worker Training', 'Type 1 & 2 Asbestos Operations Worker Training'),
        ('Asbestos Hazard Awareness Training', 'Asbestos Hazard Awareness Training'),
    ]
    
    title = models.CharField(
        max_length=255, 
        choices=TITLE_CHOICES, 
        null=True, 
        blank=True
    )
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    status=models.CharField(max_length=100,null=True,blank=True,choices=(('Active','Active'),('Inactive','Inactive')),default='Active')
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    
    
class Schedule_list(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    message = models.TextField()
    def certificate_path(instance, filename):
        random_value = str(uuid.uuid4())[:8] 
        file_extension = filename.split('.')[-1]
        return f'Certificate_images/{instance.course.title}_{instance.first_name}_certificate_{random_value}.{file_extension}'
    
    Certificate = models.FileField(upload_to=certificate_path, blank=True)
    certificate_issued = models.BooleanField(default=False)
    status=models.CharField(max_length=100,null=True,blank=True,choices=(('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected'),('Delete','Delete')),default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
## Norpro Alert

class Alerts(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    ALERT_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )
    heading = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    alert_type = models.CharField(max_length=255,  default='Low', choices=ALERT_CHOICES)
    department = models.ManyToManyField(Department, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    Expire_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.heading
    
    
class Announcement(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    heading = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="announcement_images", blank=True)
    department = models.ManyToManyField('Department', blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    Expire_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.heading


class AnnouncementFile(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to="announcement_files")

    def __str__(self):
        return f"File for {self.announcement.heading}"
    
    
class Greeting_banner(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to="greeting_banner_images", blank=True,help_text="Upload an image (recommended dimensions: 1920px width x 1080px height)")
    department = models.ManyToManyField('Department', blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    Expire_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    link = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class News(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    heading = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="news_images", blank=True,help_text="Recommended image size: 512×512 pixels")
    department = models.ManyToManyField('Department', blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.heading
    

# class UserProfile(settings.)
class NotificationPool(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
   
    team=models.ForeignKey(id_card,on_delete=models.CASCADE)
    data=models.JSONField()
    updated_at=models.DateTimeField(auto_now=True)
    # is_sent=models.BooleanField(default=False)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")

   

    def __str__(self):
        return f"{self.team.name}"