

from django.contrib import admin
from .models import Category, Company, ExperienceLevel,JobType,Job, Skill, User, UserSkill,JobApplication

admin.site.register(Company)
admin.site.register(ExperienceLevel)
admin.site.register(Job)
admin.site.register(JobType)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(JobApplication)

