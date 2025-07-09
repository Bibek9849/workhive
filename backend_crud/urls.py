from django.urls import include, path

from backend_crud import views
from backend_crud.views import aboutUS_view, applied_view, apply_job_view, change_password_view, change_view, contact_view, details_view, home_view, job_view, login_view, logout_view, navbar_view, profile_view, register_view, reset_view, upload_profile_image
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import set_language


urlpatterns = [
    path('', home_view, name='home'),  # Use 'home' as the name for the root URL
    path('login', login_view, name='login'),  # Use 'home' as the name for the root URL
    path('navbar', navbar_view, name='navbar'),  # Use 'home' as the name for the root URL
    path('register', register_view, name='register'),  # Use 'home' as the name for the root URL
    path('about', aboutUS_view, name='about'),  # Use 'home' as the name for the root URL
    path('contact', contact_view, name='contact'),  # Use 'home' as the name for the root URL
    path('details/<int:job_id>/', details_view, name='details'),
    path('job', job_view, name='job'),  # Use 'home' as the name for the root URL
    path('reset', reset_view, name='reset'),  # Use 'home' as the name for the root URL
    path('change', change_view, name='change'),  # Use 'home' as the name for the root URL
    path('applied', applied_view, name='applied'),  # Use 'home' as the name for the root URL
    path('profile', profile_view, name='profile'),  # Use 'home' as the name for the root URL
    path('logout/', logout_view, name='logout'),
    path('profile/upload-image/', upload_profile_image, name='upload_profile_image'),
    path('change-password/', change_password_view, name='change_password'),
path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_complete.html'), name='password_reset_complete'),
    path('apply/<int:job_id>/', apply_job_view, name='apply_job'),
    path('i18n/setlang/', set_language, name='set_language'),

]

