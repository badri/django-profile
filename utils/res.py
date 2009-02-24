#!/usr/bin/python
from pyparsing import *
import sys, re
import codecs
usage = """\
./res.py <filename>.txt
"""
"""
# from a given resume, extract only educational info - done
# from edu info, extract only a list of shools or colleges
	- have an xml file for key terms for schools and colleges. Ex: for school - sch, school, secondary, for college - university, institution, insitute, univ etc

	- a script which will use the terms, look into the user data and extract the information
	- another script whihc will normalize the seacrh results(optional)
          Ex. grouping of NE univs in US, normalizing Carnige Mellon univ, Carnige Mellonuniversity into 1 form.
	- dynamically create your attribute file in flamenco.
 Publications
 Internships

"""

if len(sys.argv) < 2:
	print usage
	sys.exit()

class ResumeParser:
    def __init__(self, resume):

        self.idTag =  ""
        self.eduTag = ""
        self.objTag = ""
        self.skillTag = ""
        self.personalTag = ""
        self.experienceTag = ""
        self.interestTag = ""
        self.certifTag = ""
        self.refTag = ""


        # open the resume
        file_obj = open(resume)
        _whole_test = file_obj.read()

        objBlock = Literal("-OBJECTIVE-")
        persBlock = Literal("-PERSONAL-")
        eduBlock = Literal("-EDUCATION-")
        expBlock = Literal("-EXPERIENCE-")
        skilBlock = Literal("-SKILLS-")
        interestBlock = Literal("-INTERESTS-")
        certifBlock = Literal("-CERTIF-")
        refBlock = Literal("-REF-")

        block = eduBlock ^ objBlock ^ persBlock ^ expBlock ^ skilBlock \
                     ^ interestBlock ^ certifBlock ^ refBlock

        carriageReturn = Literal('\r')


        education = eduBlock + SkipTo(block|stringEnd)
        objective = objBlock + SkipTo(block|stringEnd)
        skills = skilBlock + SkipTo(block|stringEnd)
        experience = expBlock + SkipTo(block|stringEnd)
        interests = interestBlock + SkipTo(block|stringEnd)
        certifications = certifBlock + SkipTo(block|stringEnd)
        references = refBlock + SkipTo(block|stringEnd)
        # personal_details = StringStart() + persBlock + SkipTo(block|stringEnd)
        personal_details = Optional(StringStart()) + persBlock + SkipTo(block|stringEnd)
        section = education ^ objective ^ skills \
                       ^ personal_details ^ experience ^ interests ^ certifications ^ references
        text = StringStart() + SkipTo(section|StringEnd())
        doc = Optional(text) + ZeroOrMore(section)

        education.setParseAction(self.tagifyEducation)
        objective.setParseAction(self.tagifyObjective)
        skills.setParseAction(self.tagifySkills)
        experience.setParseAction(self.tagifyExperience)
        personal_details.setParseAction(self.tagifyPersonal)
        interests.setParseAction(self.tagifyInterests)
        certifications.setParseAction(self.tagifyCertifications)
        references.setParseAction(self.tagifyReferences)
        text.setParseAction(self.tagifyOther)
        
        # parsing grammar - ends here
        # setDebug(True) # if you want to see how the text is parsed
        eduRe = re.compile(r"""\n(Education|Educational Qualification|Educational Background|\
                              Qualification|Summary of Qualification|Qualifications|\
                              Summary of Qualifications|Education & Training|Academic Background)""", re.IGNORECASE)
        edu_whole_test = eduRe.sub('-EDUCATION-',_whole_test)

        skillRe = re.compile(r"""\n(Skill|Skillsets|Skill Sets|Skills|Skill|\
                                 Specialization|Specialisation|Specializations|Specializations|\
                                 Abilities|Technical Summary|Technical Qualifications|Technical Proficiency|\
                                 Computer Proficiency|Computer Skills|Professional Skills|Relevant Skills|\
                                 Exposure|IT Exposure|Technical Skills)""", re.IGNORECASE)
        skill_whole_test = skillRe.sub('-SKILLS-', edu_whole_test)

        expRe = re.compile(r"""\n(Experience|Professional Experience|Work Experience|\
                                 Employment History|Career History|Background|\
                                 Projects|Employment|Professional Background|Working Experience|\
                                 Academic Projects|Projects Handled|Project Details)""", re.IGNORECASE)
        exp_whole_test = expRe.sub('-EXPERIENCE-', skill_whole_test)

        objRe = re.compile(r"""\n(Career Objective|Objective|Job Objective)""", re.IGNORECASE)
        obj_whole_test = objRe.sub('-OBJECTIVE-', exp_whole_test)

        personalRe = re.compile(r"""\n(Personal Details|Personal Information|Personal|About Me|\
                                       Strengths|Personal Profile)""", re.IGNORECASE)
        pers_whole_test = personalRe.sub('-PERSONAL-', obj_whole_test)

        interestRe = re.compile(r"""\n(Personal Interests|Hobbies|Activities|Interests|Other Interests)""", re.IGNORECASE)
        interest_whole_test = interestRe.sub('-INTERESTS-', pers_whole_test)

        certifRe = re.compile(r"""\n(Certifications|Honours|Honors|Awards|Prizes|Achievements|Accomplishments)""", re.IGNORECASE)
        certif_whole_test = certifRe.sub('-CERTIF-', interest_whole_test)

        refRe = re.compile(r"""\nReferences""", re.IGNORECASE)
        whole_test = refRe.sub('-REF-', certif_whole_test)

        doc.parseString(whole_test)


    def tagifyEducation(self, st, locn, toks):        
        self.eduTag += toks[1]


    def tagifyObjective(self, st, locn, toks):
        self.objTag += toks[1]


    def tagifySkills(self, st, locn, toks):
        self.skillTag += toks[1]


    def tagifyPersonal(self, st, locn, toks):
        self.personalTag += toks[1]


    def tagifyExperience(self, st, locn, toks):
        self.experienceTag += toks[1]


    def tagifyOther(self, st, locn, toks):
        self.personalTag += toks[0]

    def tagifyInterests(self, st, locn, toks):
        self.interestTag += toks[1]


    def tagifyCertifications(self, st, locn, toks):
        self.certifTag += toks[1]


    def tagifyReferences(self, st, locn, toks):
        self.refTag += toks[1]


    # exposed methods which will be used.
    # TODO: convert each of these into a python property builtin
    @property
    def education(self):
        return self.eduTag

    @property
    def objective(self):
        return self.objTag

    @property
    def skills(self):
        return self.skillTag

    @property
    def personal(self):
        return self.personalTag

    @property
    def experience(self):
        return self.experience

    @property
    def interests(self):
        return self.interestTag

    @property
    def certifications(self):
        return self.certifTag

    @property
    def references(self):
        return self.refTag

"""
p = ResumeParser(sys.argv[1])

print p.skills

print p.personal

"""
