from django.contrib import admin
from demoprofile.models import Jobseeker, Resume, Recruiter
from django import forms
from userprofile.views import handle_uploaded_resume

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date')
    search_fields = ('name',)


class ResumeAdmin(admin.ModelAdmin):
    fields = ('user', 'resume')
        
        

#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Jobseeker)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Recruiter)
