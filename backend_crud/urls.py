from django.urls import include, path

from backend_crud.views import aboutUS_view, applied_view, change_view, contact_view, details_view, home_view, job_view, login_view, logout_view, navbar_view, profile_view, register_view, reset_view


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

]

