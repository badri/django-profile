from django.contrib import admin
from demoprofile.models import Jobseeker, Resume, Recruiter
from django import forms
from userprofile.views import handle_uploaded_resume

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date')
    search_fields = ('name',)



class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume

    def clean_resume_text(self):
        cleaned_data = self.cleaned_data
        return handle_uploaded_resume(cleaned_data.get('resume'))

    def clean_name(self):
        return 'foo'
    

class ResumeAdmin(admin.ModelAdmin):
    form = ResumeForm
        
        

#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Jobseeker)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Recruiter)
