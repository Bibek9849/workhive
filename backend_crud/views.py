from django.shortcuts import get_object_or_404, render,redirect
# from accounts.account_forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.conf import settings
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

from backend_crud.forms import ProfileUpdateForm
from backend_crud.models import Category, Company, ExperienceLevel, Job,JobApplication, JobType, Skill, UserSkill
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
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
            messages.success(request, "Logged in successfully.")
            return render(request, 'login.html', {'redirect_after_login': True})
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

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

    # Check if just logged in
    just_logged_in = request.session.pop('just_logged_in', False)

    return render(request, 'home.html', {
        'jobs': jobs,
        'job_count': job_count,
        'user_count': user_count,
        'company_count': company_count,
        'locations': locations,
        'categories': categories,
        'just_logged_in': just_logged_in,
    })

def navbar_view(request):
    return render(request, 'navbar.html')

def aboutUS_view(request):
    return render(request, 'aboutus.html')

def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Message from {first_name} {last_name} ({email}):\n\n{message}"

        # Email to you
        send_mail(
            subject='New Contact Form Submission',
            message=full_message,
            from_email=email,
            recipient_list=['pandeybibe098k@gmail.com'],
        )

        # Auto-reply to user
        send_mail(
            subject='Thanks for Contacting Us!',
            message=f"Hi {first_name},\n\nThanks for reaching out! We’ve received your message and will get back to you shortly.\n\nBest,\nTeam",
            from_email='pandeybibe098k@gmail.com',
            recipient_list=[email],
        )

        messages.success(request, 'Thank you for contacting us! We’ve sent a confirmation to your email.')
        return redirect('contact')

    return render(request, 'contact_us.html')

def details_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    related_jobs = Job.objects.filter(category=job.category).exclude(pk=job_id)[:4]  # max 4 related jobs

    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    return render(request, 'job_details.html', context)
from django.db.models import Q

def job_view(request):
    # Read filters from request
    title_query = request.GET.get('title', '')
    location_query = request.GET.get('location', '')
    category_query = request.GET.getlist('category')
    job_type_query = request.GET.getlist('job_type')
    experience_query = request.GET.getlist('experience')
    min_salary = request.GET.get('minSalary')
    max_salary = request.GET.get('maxSalary')
    sort_by = request.GET.get('sort', 'latest')  # default to 'latest'

    # Start base queryset
    jobs = Job.objects.select_related('company', 'category', 'job_type', 'experience')

    # Apply filters
    if title_query:
        jobs = jobs.filter(Q(title__istartswith=title_query) | Q(company__name__istartswith=title_query))

    if location_query:
        jobs = jobs.filter(company__address__icontains=location_query)

    if category_query:
        category_query = [cat for cat in category_query if cat.isdigit()]
        if category_query:
            jobs = jobs.filter(category__id__in=category_query)

    if job_type_query:
        jobs = jobs.filter(job_type__name__in=job_type_query)

    if experience_query:
        jobs = jobs.filter(experience__level__in=experience_query)

    if min_salary:
        jobs = jobs.filter(salary_min__gte=min_salary)

    if max_salary:
        jobs = jobs.filter(salary_max__lte=max_salary)

    # Apply sorting
    if sort_by == 'name':
        jobs = jobs.order_by('title')
    else:
        jobs = jobs.order_by('-posted_at')

    # Optional: limit or paginate
    jobs = jobs.distinct()[:10]

    # Get filter dropdown options
    categories = Category.objects.all()
    job_types = JobType.objects.all()
    experience_levels = ExperienceLevel.objects.all()

    # Store selected filters to maintain in form
    selected_filters = {
        'title': title_query,
        'location': location_query,
        'categories': category_query,
        'job_types': job_type_query,
        'experience_levels': experience_query,
        'minSalary': min_salary,
        'maxSalary': max_salary,
        'sort_by': sort_by
    }

    return render(request, 'jobs.html', {
        'jobs': jobs,
        'categories': categories,
        'job_types': job_types,
        'experience_levels': experience_levels,
        'selected_filters': selected_filters,
        'sort_by': sort_by
    })
def reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            # Reset URL
            reset_url = request.build_absolute_uri(f'/reset/{uid}/{token}/')

            # Render and send email
            subject = 'Password Reset Request'
            message = render_to_string('demo.html', {
                'user': user,
                'reset_url': reset_url
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

            messages.success(request, "We've sent you an email with a password reset link.")
        else:
            messages.error(request, "No user found with that email address.")

        return redirect('reset')  # Redirect to avoid form resubmission

    return render(request, 'reset.html')
def change_view(request):
    return render(request, 'change.html')
def demo_view(request):
    return render(request, 'demo.html')
def set_pass_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            elif len(password1) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password reset successful! You can now log in.")
                return redirect('login')

        return render(request, 'set_password.html', {'validlink': True})
    else:
        messages.error(request, "The password reset link is invalid or expired.")
        return render(request, 'set_password.html', {'validlink': False})

@login_required
def applied_view(request):
    user = request.user
    applications = JobApplication.objects.filter(user=user).select_related(
        'job',
        'job__company',
        'job__category',
        'job__job_type'
    )
    return render(request, 'applied.html', {'applications': applications})
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)  # include request.FILES if image upload
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            # form invalid, you can debug here
            print(form.errors)
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form, 'user': user})

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


@login_required
@require_POST
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    # Check if user already applied for this job
    if JobApplication.objects.filter(user=user, job=job).exists():
        return JsonResponse({
            'success': False,
            'message': 'You have already applied for this job.'
        })

    phone = request.POST.get('phone')
    resume = request.FILES.get('resume')

    # Check if phone or resume is missing
    if not phone:
        return JsonResponse({'success': False, 'message': 'Phone number is required.'})

    if not resume:
        return JsonResponse({'success': False, 'message': 'Resume file is required.'})

    # Update user's phone number if empty or different
    if not user.phone_no or user.phone_no != phone:
        user.phone_no = phone
        user.save()

    # Save application
    JobApplication.objects.create(user=user, job=job, phone=phone, resume=resume)

    return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})