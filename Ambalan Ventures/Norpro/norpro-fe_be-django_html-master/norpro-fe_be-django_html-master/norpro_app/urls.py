from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name="index"),
    path('company', views.Company, name="company"),
    path('memberships_and_partnerships', views.memberships_and_partnerships, name="memberships_and_partnerships"),
    path('gallery', views.Gallery_view, name="gallery"),
    path('news_events', views.News_events, name="news_events"),
    path('news_event_details/<int:news_id>', views.News_event_details, name="news_event_details"),
    path('calendar', views.calendar, name="calendar"),
    path('events/<int:Calendar_id>', views.events, name="events"),
#  security
    path('mine_security', views.Mine_security, name="mine_security"),
    path('mobile_patrol', views.Mobile_patrol, name="mobile_patrol"),
    path('industrial_guards', views.Industrial_guards, name="industrial_guards"),
    path('static_guards_and_event_management', views.static_guards_and_event_management, name="static_guards_and_event_management"),
    path('institutional_guards', views.Institutional_guards, name="institutional_guards"),
    path('Loss_prevention', views.Loss_prevention, name="Loss_prevention"),
    path('other_service', views.Other_service, name="other_service"),
    path('security', views.security, name="security"),
    
    path('join_our_team', views.Join_our_team, name="join_our_team"),
    path('academy', views.Academy, name="academy"),
    # courses
    path('courses', views.Courses, name="courses"),
    path('security_guard_training', views.security_guard_training, name="security_guard_training"),
    path('smart_serve', views.smart_serve, name="smart_serve"),
    
    path('contact', views.Contact, name="contact"),
    path('career_description/<int:careers_id>', views.Career_description, name="career_description"),
    path('employee-referral-program-norpro-security', views.Employee_referral_security, name="employee_refferal_security"),
# health_and_safety
    path('training', views.training, name="training"),
    # training
    path('training/lead_class_1_operations_worker_training', views.lead_class_1_operations_worker_training, name="lead_class_1_operations_worker_training"),
    path('training/lead_hazard_awareness_training', views.lead_hazard_awareness_training, name="lead_hazard_awareness_training"),
    path('training/type_1_and_2_asbestos_operations_worker_training', views.type_1_and_2_asbestos_operations_worker_training, name="type_1_and_2_asbestos_operations_worker_training"),
    path('training/asbestos_hazard_awareness_training', views.asbestos_hazard_awareness_training, name="asbestos_hazard_awareness_training"),
    
    path('respirator_fit_testing', views.respirator_fit_testing, name="respirator_fit_testing"),
    path('health_and_safety', views.health_and_safety, name="health_and_safety"),
    path('check-email/', views.check_email_uniqueness, name='check_email_uniqueness'),
    path('support_services', views.support_services, name="support_services"),
    path('management_system_implementation_and_auditing', views.management_system_implementation_and_auditing, name="management_system_implementation_and_auditing"),
    path('hazardous_materials_testing_management_and_remediation', views.hazardous_materials_testing_management_and_remediation, name="hazardous_materials_testing_management_and_remediation"),
    path('indoor_air_quality_assessment_services', views.indoor_air_quality_assessment_services, name="indoor_air_quality_assessment_services"),
    path('workplace_noise_assessments', views.workplace_noise_assessments, name="workplace_noise_assessments"),
# id card
    path('id_card/<str:slug_id>', views.identity_card, name="id_card"),
    path('meet_the_team', views.meet_the_team, name="meet_the_team"),
    
# vcard
    path('download_vcard/<str:slug>', views.download_vcard, name="download_vcard"),
# site map
    path('sitemap.xml',views.siteMap,name="sitemap"),
    
    path('privacy_and_policy', views.privacy_and_policy, name="privacy_and_policy"),
    path('terms_and_conditions', views.terms_and_conditions, name="terms_and_conditions"),
]