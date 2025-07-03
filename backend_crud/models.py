from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(('email address'), unique = True)
    phone_no = models.CharField(max_length = 10)
    gender = models.CharField(max_length = 10)
    experience = models.CharField(max_length = 10)
    education = models.CharField(max_length = 10)
    dob = models.CharField(max_length = 10)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # ✅ Add this line

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.name
    
class UserSkill(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_skill')
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE, related_name='skill_user')

    def __str__(self):
        return f"{self.user.email} - {self.skill.name}"

class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    address = models.CharField(max_length=255)  # e.g. Dillibazzar, Kathmandu
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
class JobType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. Full Time, Internship

    def __str__(self):
        return self.name
    
class ExperienceLevel(models.Model):
    level = models.CharField(max_length=50, unique=True)  # e.g. Mid-level, Entry-level

    def __str__(self):
        return self.level
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g. IT, Finance, Marketing

    def __str__(self):
        return self.name
    
class Job(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    job_type = models.ForeignKey('JobType', on_delete=models.SET_NULL, null=True)
    experience = models.ForeignKey('ExperienceLevel', on_delete=models.SET_NULL, null=True)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    description = models.TextField()
    responsibilities = models.TextField()
    skills = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
