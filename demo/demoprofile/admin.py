from django.contrib import admin
from demoprofile.models import Jobseeker, Resume, Recruiter

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date')
    search_fields = ('name',)

#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Jobseeker)
admin.site.register(Resume)
admin.site.register(Recruiter)
