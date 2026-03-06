from django.contrib import admin
from .models import *
# Register your models here.

class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'username', 'user_type', 'status', 'is_staff', 'is_active')
    search_fields = ('name', 'email', 'username')
    list_filter = ('user_type', 'status', 'is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'username','changed_pwd','password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Personal', {
            'fields': ('user_type', 'status', 'role'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'username', 'password1', 'password2', 'user_type', 'status', 'role', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'status', 'date')
    search_fields = ('role_name',)
    list_filter = ('status',)
    ordering = ('date',)

class PathAdmin(admin.ModelAdmin):
    list_display = ('path_name', 'status', 'created_at', 'parent')
    search_fields = ('path_name',)
    list_filter = ('status',)
    ordering = ('created_at',)

# Registering the models with the admin site
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(AdminRole, AdminRoleAdmin)
admin.site.register(Path, PathAdmin)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'feedback', 'test_img', 'created_at', 'updated_at')
    search_fields = ('name', 'company')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20
    
@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'place', 'place_2', 'created_at', 'updated_at')
    search_fields = ('title', 'place', 'place_2')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20
    
@admin.register(Company_testimonial)
class Company_testimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'feedback', 'com_test_img', 'created_at', 'updated_at')
    search_fields = ('name', 'position')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20
    
    
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'company_name', 'subject', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(ContactForm, ContactFormAdmin)

class ServiceFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'location', 'service', 'type_service', 'message', 'created_at')
    list_filter = ('location', 'service')
    search_fields = ('name', 'email', 'location', 'service')

admin.site.register(ServiceForm, ServiceFormAdmin)

@admin.register(FormCareer)
class CareerFormAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'resume', 'cover_letter', 'other_documents', 'type_career', 'created_at']
    
    
@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    
    
class EmployeeReferralAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'referal_first_name', 'referal_last_name')
    list_per_page = 20

admin.site.register(Employee_referral_program, EmployeeReferralAdmin)



# id card
class Id_card_Admin(admin.ModelAdmin):
    list_display = ('name', 'title', 'phone_number', 'bio','image', 'linkedin', 'slug',)
    list_filter = ('name', 'title')
    search_fields = ('name', 'title', 'phone_number',)
    list_per_page = 20

admin.site.register(id_card, Id_card_Admin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',  'status', 'created_at', 'updated_at')
    search_fields = ('title', 'status')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20


class Qr_code_Admin(admin.ModelAdmin):
    list_display = ('link', 'qr_code', 'created_at',)
    list_filter = ('link', 'created_at',)
    search_fields = ('link', 'created_at',)
    list_per_page = 20

admin.site.register(qr_code, Qr_code_Admin)


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'created_at', 'updated_at') 
    search_fields = ('title', 'description') 
    list_filter = ('date',)  

admin.site.register(Calendar, CalendarAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_date', 'to_date', 'price', 'place', 'created_at', 'updated_at')
    list_filter = ('title', 'from_date')
    search_fields = ('place',) 
    ordering = ('-created_at',)  

admin.site.register(Course, CourseAdmin)


class CourseListAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'get_course_title', 'status', 'certificate_issued', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'course__title', 'status')
    list_filter = ('course', 'created_at', 'status')
    ordering = ('-created_at',) 
    
    def get_course_title(self, obj):
        return obj.course.title
    
    get_course_title.short_description = 'Course Title'

admin.site.register(Schedule_list, CourseListAdmin)


class AlertsAdmin(admin.ModelAdmin):
    list_display = ('heading', 'alert_type', 'status', 'created_at', 'updated_at')
    list_filter = ('alert_type', 'status', 'created_at')
    search_fields = ('heading', 'discription')

admin.site.register(Alerts, AlertsAdmin)

class AnnouncementFileInline(admin.TabularInline):
    model = AnnouncementFile
    extra = 1


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('heading', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('heading', 'description')
    inlines = [AnnouncementFileInline]
    filter_horizontal = ('department',)
    
    
@admin.register(Greeting_banner)
class GreetingBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'updated_at', 'Expire_date')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('heading', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('heading', 'description')
    date_hierarchy = 'created_at'

@admin.register(NotificationPool)
class NotificationPooladmin(admin.ModelAdmin):
    list_display=('team','updated_at','status')
    list_filter=('updated_at','team','status')
    search_fields=('team.name',)
    date_hierarchy='updated_at'