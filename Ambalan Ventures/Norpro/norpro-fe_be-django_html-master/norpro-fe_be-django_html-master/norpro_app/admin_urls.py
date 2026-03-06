from django.urls import path
from . import admin_views
from .decorators import permission_required

urlpatterns = [
    path('admin_login', admin_views.user_login, name="admin_login"),
    path('logout/', admin_views.user_logout, name='logout'),
    path('', admin_views.Admin_home, name="admin_home"),
    
    #User list 
    path('create_User', permission_required('Add User')(admin_views.Create_User), name="user_create"),
    path('edituser/<int:user_id>', permission_required('Edit User')(admin_views.Edituser), name="user_edit"), 
    path('user_list', permission_required('View User List')(admin_views.User_list), name="user_list"),
    path('change_password/', admin_views.change_password, name='change_password'),
    path('user_password_change/<int:user_id>/',permission_required('View User List')(admin_views.user_password_change),name='user_password_change'),
    
    # path list
    path('create_Permission', permission_required('Add Permission')(admin_views.Create_Permission), name="permission_create"),
    path('editpermission/<int:permission_id>', permission_required('Edit Permission')(admin_views.Editpermission), name="permission_edit"),
    path('permission_list', permission_required('View Permission List')(admin_views.Permission_list), name="permission_list"),
    
    # role list
    path('create_Role', permission_required('Add Role')(admin_views.Create_Role), name="role_create"),
    path('editrole/<int:role_id>', permission_required('Edit Role')(admin_views.Editrole), name="role_edit"),
    path('role_list', permission_required('View Role List')(admin_views.Role_list), name="role_list"),
    path('set_permissions/<int:perm_id>/', permission_required('Set Permission')(admin_views.set_permissions), name='set_permissions'),
    
    #testimonial list 
    path('create_Testimonial', permission_required('Add Testimonial')(admin_views.Create_Testimonial), name="testimonial_create"),
    path('edittestimonial/<int:testimonial_id>', permission_required('Edit Testimonial')(admin_views.Edittestimonial), name="testimonial_edit"),
    path('deletetestimonial/<int:testimonial_id>', permission_required('Delete Testimonial')(admin_views.Delete_testimonial), name='delete_testimonial'),
    path('testimonial_list', permission_required('View Testimonial List')(admin_views.Testimonial_list), name="testimonial_list"),
    
    #career list 
    path('create_career', permission_required('Add Career')(admin_views.Create_career), name="career_create"),
    path('editcareer/<int:career_id>', permission_required('Edit Career')(admin_views.Editcareer), name="career_edit"),
    path('career_list', permission_required('View Career List')(admin_views.Career_list), name="career_list"),
    
    #Company testimonial list 
    path('create_company_testimonial', permission_required('Add Company Testimonial')(admin_views.Create_company_testimonial), name="company_testimonial_create"),
    path('edit_company_testimonial/<int:company_testimonial_id>', permission_required('Edit Company Testimonial')(admin_views.Edit_company_testimonial), name="company_testimonial_edit"),
    path('delete_company_testimonial/<int:company_testimonial_id>/', permission_required('Delete Company Testimonial')(admin_views.Delete_company_testimonial), name='delete_company_testimonial'),
    path('company_testimonial_list', permission_required('View Company Testimonial List')(admin_views.Company_testimonial_list), name="company_testimonial_list"),
    
    #news and events list 
    path('create_news_and_events', permission_required('Add News and Events')(admin_views.Create_news_and_events), name="newsevents_create"),
    path('edit_newsevents/<int:newsevent_id>', permission_required('Edit News and Events')(admin_views.Edit_newsevents), name="newsevents_edit"),
    path('delete_newsevents/<int:newsevent_id>/', permission_required('Delete News and Events')(admin_views.Delete_newsevents), name='delete_newsevents'),
    path('newsevents_list', permission_required('View News and Events List')(admin_views.Newsevents_list), name="newsevents_list"),
    
    #calendar list 
    path('create_calendar', permission_required('Add Calendar')(admin_views.Create_calendar), name="calendar_create"),
    path('edit_calendar/<int:calendar_id>', permission_required('Edit Calendar')(admin_views.Edit_calendar), name="calendar_edit"),
    path('delete_calendar/<int:calendar_id>/', permission_required('Delete Calendar')(admin_views.Delete_calendar), name='delete_calendar'),
    path('calendar_list', permission_required('View Calendar List')(admin_views.Calendar_list), name="calendar_list"),
    
    #Gallery list 
    path('create_gallery', permission_required('Add Gallery')(admin_views.Create_gallery), name="gallery_create"),
    path('edit_gallery/<int:gallery_id>', permission_required('Edit Gallery')(admin_views.Edit_gallery), name="gallery_edit"),
    path('delete_gallery/<int:gallery_id>/', permission_required('Delete Gallery')(admin_views.Delete_gallery), name='delete_gallery'),
    path('gallery_list', permission_required('View Gallery List')(admin_views.Gallery_list), name="gallery_list"),
    
    #course list 
    path('create_course', permission_required('Add Course')(admin_views.Create_course), name="course_create"),
    path('edit_course/<int:course_id>', permission_required('Edit Course')(admin_views.Edit_course), name="course_edit"),
    path('toggle_course/<int:course_id>/', permission_required('Status Course')(admin_views.toggle_course_status), name='toggle_course'),
    path('course_list', permission_required('View Course List')(admin_views.Course_list), name="course_list"),
    path('application_list/<int:course_id>/', permission_required('View Course Application List')(admin_views.application_list), name='application_list'),
    path("update_status/", permission_required('Update Application Status')(admin_views.update_status), name="update_status"),
    path('export/csv/<int:course_id>/', permission_required('Export CSV')(admin_views.export_csv), name='export_csv'),
    path('course/<int:course_id>/generate_pdf/', permission_required('Download PDF')(admin_views.generate_pdf), name='generate_pdf'),
    path('generate_certificate/<int:schedule_id>/', admin_views.generate_user_certificate, name='generate_user_certificate'),
    path('download_certificate/<int:schedule_id>/', admin_views.download_certificate, name='download_certificate'),
    
    #forms
    path('service_form', permission_required('View Service Form')(admin_views.Service_form), name="service_form"),
    path('delete_multiple_service_forms/', permission_required('Delete Service Form')(admin_views.delete_multiple_service_forms), name='delete_multiple_service_forms'),
    
    path('contact_form', permission_required('View Contact Form')(admin_views.Contact_form), name="contact_form"),
    path('delete_contact_form/', permission_required('Delete Contact Form')(admin_views.Delete_contact_form), name='delete_contact_form'),
    
    path('formcareer', permission_required('View Career Form')(admin_views.Page_career), name="formcareer"),
    path('delete_formcareer/', permission_required('Delete Career Form')(admin_views.Delete_formcareer), name='delete_formcareer'),
    
    path('academy_form', permission_required('View Academy Form')(admin_views.Academy_form), name="academy_form"),
    path('delete_academy_form/', permission_required('Delete Academy Form')(admin_views.Delete_academy_form), name='delete_academy_form'),
    
    path('employee_referral_form', permission_required('View Employee Referral Form')(admin_views.Form_employee_referral), name="employee_referral_form"),
    path('employee_referral_form_details/<int:employee_referral_id>', permission_required('View Employee Referral Form Details')(admin_views.employee_referral_form_details), name="employee_referral_form_details"),
    path('delete_employee_referral_form/', permission_required('Delete Employee Referral Form')(admin_views.Delete_employee_referral_form), name='delete_employee_referral_form'),
    
    
    #Teams_list
    path('Create_Teams', permission_required('Add Teams')(admin_views.Create_Teams), name="Create_Teams"),
    path('EditTeams/<int:teams_id>', permission_required('Edit Teams')(admin_views.EditTeams), name="EditTeams"),
    path('deleteteams/<int:teams_id>', permission_required('Delete Teams')(admin_views.deleteteams), name='deleteteams'),
    path('teams_list', permission_required('View Teams List')(admin_views.teams_list), name="teams_list"),
    
    # qrcode
    path('Create_qrcode', permission_required('View & Add Qrcode')(admin_views.Create_qrcode), name="Create_qrcode"),
    path('delete_qr_code/<int:qrcode_id>', permission_required('Delete Qrcode')(admin_views.delete_qr_code), name='delete_qr_code'),

    #department list 
    path('create_department', permission_required('Add Department')(admin_views.Create_department), name="department_create"),
    path('editdepartment/<int:department_id>', permission_required('Edit Department')(admin_views.Editdepartment), name="department_edit"),
    path('department_list', permission_required('View Department List')(admin_views.Department_list), name="department_list"),
    
    #alert list 
    path('create_alert', permission_required('Add Alert')(admin_views.Create_alert), name="alert_create"),
    path('editalert/<int:alert_id>', permission_required('Edit Alert')(admin_views.Editalert), name="alert_edit"),
    path('alert_list', permission_required('View Alert List')(admin_views.Alert_list), name="alert_list"),
    
    #announcement list 
    path('create_announcement', permission_required('Add Announcement')(admin_views.Create_announcement), name="announcement_create"),
    path('editannouncement/<int:announcement_id>', permission_required('Edit Announcement')(admin_views.Editannouncement), name="announcement_edit"),
    path('announcement_list', permission_required('View Announcement List')(admin_views.Announcement_list), name="announcement_list"),

    #Greeting banner list 
    path('create_banner', permission_required('Add Banner')(admin_views.Create_banner), name="banner_create"),
    path('editbanner/<int:banner_id>', permission_required('Edit Banner')(admin_views.Editbanner), name="banner_edit"),
    path('banner_list', permission_required('View Banner List')(admin_views.Banner_list), name="banner_list"),
    
    #News list 
    path('create_news', permission_required('Add News')(admin_views.Create_news), name="news_create"),
    path('editnews/<int:news_id>', permission_required('Edit News')(admin_views.Editnews), name="news_edit"),
    path('news_list', permission_required('View News List')(admin_views.News_list), name="news_list"),
]