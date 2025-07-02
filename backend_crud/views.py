from django.shortcuts import get_object_or_404, render,redirect
# from accounts.account_forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate

from backend_crud.forms import ProfileUpdateForm
from backend_crud.models import Job, Skill, UserSkill


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
    return render(request, 'home.html', {'jobs': jobs})

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
    jobs = Job.objects.select_related('company', 'category', 'job_type').order_by('-posted_at')[:5]

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
        form = ProfileUpdateForm(request.POST, instance=user, user=user)
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








