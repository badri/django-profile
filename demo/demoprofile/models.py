from django.db import models
from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
import datetime

"""
TODO:
# user can have many resumes 
# user can cater many different profiles.
# why are we storing files in different formats instead of generating them on demand?
"""
def get_rdf_path(instance, filename):
    return 'resumes/%s/rdf/%s' % (instance.user, filename)

def get_original_format_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, '/resumes/%s/orig/%s' % (instance.user, filename))

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class Resume(models.Model):
        'resume information.'
        # who owns the resume
        user = models.ForeignKey('Jobseeker', unique=True)
        # name of the current resume
        name = models.CharField(max_length=50)
        # usual resume tags
        education = models.TextField()
        objective = models.TextField(blank = True)
        skills = models.TextField()
        personal = models.TextField()
        experience = models.TextField()
        interests = models.TextField(blank = True)
        certifications = models.TextField(blank = True)
        references = models.TextField(blank = True) 
        # resume in an RDF format
        rdf_file = models.FileField(upload_to=get_rdf_path, blank=True)
        # the original file format supplied by the user
        resume = models.FileField(upload_to=get_original_format_path, blank=True)
        # text form of resume, will be removed in future versions`
        resume_text = models.TextField(blank=True)
        class Meta:
                permissions = (
                                 ("resume_is_public", "resume is available for\
                                  public view"),
                              )
        def get_absoulte_url(self):
            return "%i/%i" % (self.user, self.name)
        
class Jobseeker(BaseProfile):
        'person searching for jobs.'
        about = models.TextField(blank=True)
        resumes = models.ManyToManyField(Resume, blank=True)
        def is_jobseeker(self):
                return True

class Recruiter(BaseProfile):
        'wades through a pile of resumes.'
        FIELD_CHOICES = (
                                ('PL', 'location'),
                                ('SK', 'skill sets'),
                                ('EX', 'experience'),
                                ('IN', 'Institution'),
                                ('CO', 'Employer')
                        )
        field1 = models.CharField(max_length = 2, choices = FIELD_CHOICES)
        field2 = models.CharField(max_length = 2, choices = FIELD_CHOICES)
        field3 = models.CharField(max_length = 2, choices = FIELD_CHOICES)
        class Meta:
                permissions = (
                                ('can_peep', 'paid user who can see personal\
                                 information'),
                              )
        def is_recruiter(self):
                return True

