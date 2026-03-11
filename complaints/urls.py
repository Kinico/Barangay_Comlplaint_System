from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Complaint URLs
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('track/', views.track_complaint, name='track_complaint'),
    path('success/<str:tracking_code>/', views.complaint_success, name='complaint_success'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-status/<int:complaint_id>/', views.update_complaint_status, name='update_status'),
    path('make-admin/', views.make_admin, name='make_admin'),
]