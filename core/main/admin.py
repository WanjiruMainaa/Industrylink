from .models import StudentProfile, Skill, Project, Mentor
from django.contrib import admin


# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Mentor)


