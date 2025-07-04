from django.shortcuts import get_object_or_404, render,redirect
# from accounts.account_forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate

from backend_crud.forms import ProfileUpdateForm
from backend_crud.models import Category, Company, Job, Skill, UserSkill
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


# ✅ Correct:
from django.contrib.auth import get_user_model
User = get_user_model()

# # Create your views here.
def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists with this email.")
            return redirect('register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
  # redirect to login page on failure

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    jobs = Job.objects.select_related('company', 'category', 'job_type').order_by('-posted_at')[:5]

    # Count data for stats section
    job_count = Job.objects.count()
    user_count = User.objects.count()
    company_count = Company.objects.count()

    # Fetch distinct locations from companies
    locations = Job.objects.values_list('company__address', flat=True).distinct()

    # Fetch all categories
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'jobs': jobs,
        'job_count': job_count,
        'user_count': user_count,
        'company_count': company_count,
        'locations': locations,
        'categories': categories,
    })
def navbar_view(request):
    return render(request, 'navbar.html')

def aboutUS_view(request):
    return render(request, 'aboutus.html')

def contact_view(request):
    return render(request, 'contact_us.html')

def details_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_details.html', {'job': job})

def job_view(request):
    title_query = request.GET.get('title', '')
    location_query = request.GET.get('location', '')
    category_query = request.GET.get('category', '')

    jobs = Job.objects.select_related('company', 'category', 'job_type').order_by('-posted_at')

    # Filter by title or company name if provided
    if title_query:
        jobs = jobs.filter(Q(title__icontains=title_query) | Q(company__name__icontains=title_query))

    # Filter by company address/location if provided
    if location_query:
        jobs = jobs.filter(company__address__icontains=location_query)

    # Filter by category if provided
    if category_query:
        jobs = jobs.filter(category__id=category_query)

    # Optional: limit to latest 5 filtered jobs, or remove limit if you want all results
    jobs = jobs[:5]

    return render(request, 'jobs.html', {'jobs': jobs})
def reset_view(request):
    return render(request, 'reset.html')


def change_view(request):
    return render(request, 'change.html')


def applied_view(request):
    return render(request, 'applied.html')
def profile_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()

            # Save selected skills
            skills = form.cleaned_data['skills']
            UserSkill.objects.filter(user=user).delete()
            for skill in skills:
                UserSkill.objects.create(user=user, skill=skill)

            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Or wherever you want
    else:
        form = ProfileUpdateForm(instance=user, user=user)

    return render(request, 'profile.html', {'form': form})


@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            user = request.user
            user.image = image
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No image uploaded'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        user = request.user

        if not user.check_password(current_password):
            return JsonResponse({'success': False, 'error': 'Your current password is incorrect.'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error': 'New passwords do not match.'})

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keeps the user logged in after password change
        return JsonResponse({'success': True, 'message': 'Password changed successfully.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})