from django.db import models
from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
import datetime

from utils.fileFilter import extractText
from utils.res import ResumeParser
import os

from demo.middleware import threadlocals
from django.contrib.auth.models import User
            

"""
TODO:
# user can have many resumes 
# user can cater many different profiles.
# why are we storing files in different formats instead of generating them on demand?
# each resume must have a name
"""
def get_rdf_path(instance, filename):
    return 'resumes/%s/%s' % (instance.user, filename)


GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class Resume(models.Model):
        'resume information.'
        # who owns the resume
        user = models.ForeignKey('Jobseeker')
        # name of the current resume
        name = models.CharField(max_length=50)
        # usual resume tags
        education = models.TextField(blank = True)
        objective = models.TextField(blank = True)
        skills = models.TextField(blank = True)
        personal = models.TextField(blank = True)
        experience = models.TextField(blank = True)
        interests = models.TextField(blank = True)
        certifications = models.TextField(blank = True)
        references = models.TextField(blank = True) 
        # resume in an RDF format
        rdf_file = models.FileField(upload_to=get_rdf_path, blank=True)
        # the original file format supplied by the user
        resume = models.FileField(upload_to=get_rdf_path, blank=True)
        # text form of resume, will be removed in future versions`
        resume_text = models.TextField(blank=True)

        def __unicode__(self):
            return u"%s" % (self.name)
        
        class Meta:
                permissions = (
                                 ("resume_is_public", "resume is available for\
                                  public view"),
                              )

        @models.permalink
        def get_absolute_url(self):
            return ('resume_public', (), {
                'username': self.user.user.username,
                'resumename': self.name})
        
        def save(self, force_insert=False, force_update=False):
            if not force_update:
                self.resume_text = extractText(self.resume)
                
            fieldset = ResumeParser(self.resume_text)
            self.education = fieldset.education
            self.objective = fieldset.objective
            self.experience = fieldset.experience
            self.skills = fieldset.skills
            self.personal = fieldset.personal
            self.certifications = fieldset.certifications
            self.references = fieldset.references
            super(Resume, self).save(force_insert, force_update)
            
    
        
class Jobseeker(BaseProfile):
        'person searching for jobs.'
        about = models.TextField(blank=True)
        # resumes = models.ManyToManyField(Resume, limit_choices_to={'user':threadlocals.get_current_user()}, blank=True)
        # resumes = models.ManyToManyField(Resume, blank=True)
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

