#!/usr/bin/python
from pyparsing import *
import sys, re
import codecs
usage = """\
./res.py <filename>.txt <id> <output xml file>
"""
"""
# from a given resume, extract only educational info - done
# from edu info, extract only a list of shools or colleges
	- have an xml file for key terms for schools and colleges. Ex: for school - sch, school, secondary, for college - university, institution, insitute, univ etc

	- a script which will use the terms, look into the user data and extract the information
	- another script whihc will normalize the seacrh results(optional) -Ex. grouping of NE univs in US, normalizing Carnige Mellon univ, Carnige Mellonuniversity into 1 form.
	- dynamically create your attribute file in flamenco. 
"""

if len(sys.argv) < 4:
	print usage
	sys.exit()

idTag =  "<field name=\"id\">"
eduTag = "<field name=\"education\">"
objTag = "<field name=\"objective\">"
skillTag = "<field name=\"skills\">"
personalTag = "<field name=\"personal\">"
experienceTag = "<field name=\"experience\">"
interestTag = "<field name=\"activities\">"
certifTag = "<field name=\"certifications\">"
refTag = "<field name=\"references\">"

def tagifyEducation(st, locn, toks):
    global eduTag
    eduTag += toks[1]
#    print eduTag 

def tagifyObjective(st, locn, toks):
    global objTag
    objTag += toks[1]
#    print objTag

def tagifySkills(st, locn, toks):
    global skillTag
    skillTag += toks[1]
#    print skillTag

def tagifyPersonal(st, locn, toks):
    global personalTag
    personalTag += toks[1]
#    print personalTag

def tagifyExperience(st, locn, toks):
    global experienceTag
    experienceTag += toks[1]
#    print experienceTag

def tagifyOther(st, locn, toks):
    global personalTag
    personalTag += toks[0]

def tagifyInterests(st, locn, toks):
    global interestTag
    interestTag += toks[1]
#    print interestTag 

def tagifyCertifications(st, locn, toks):
    global certifTag
    certifTag += toks[1]
#    print certifTag 

def tagifyReferences(st, locn, toks):
    global refTag
    refTag += toks[1]
#    print regTag 

# basic parsing grammar -starts here
objBlock = Literal("-OBJECTIVE-")
persBlock = Literal("-PERSONAL-")
eduBlock = Literal("-EDUCATION-")
expBlock = Literal("-EXPERIENCE-")
skilBlock = Literal("-SKILLS-")
interestBlock = Literal("-INTERESTS-")
certifBlock = Literal("-CERTIF-")
refBlock = Literal("-REF-")

block = eduBlock ^ objBlock ^ persBlock ^ expBlock ^ skilBlock ^ interestBlock ^ certifBlock ^ refBlock

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
section = education ^ objective ^ skills ^ personal_details ^ experience ^ interests ^certifications ^ references
text = StringStart() + SkipTo(section|StringEnd())
doc = Optional(text) + ZeroOrMore(section)

education.setParseAction(tagifyEducation)
objective.setParseAction(tagifyObjective)
skills.setParseAction(tagifySkills)
experience.setParseAction(tagifyExperience)
personal_details.setParseAction(tagifyPersonal)
interests.setParseAction(tagifyInterests)
certifications.setParseAction(tagifyCertifications)
references.setParseAction(tagifyReferences)
text.setParseAction(tagifyOther)
# parsing grammar - ends here
# setDebug(True) # if you want to see how the text is parsed

# open the input text file
file_obj = open(sys.argv[1])
_whole_test = file_obj.read( )

# substitute macros for common keywords in repective fields
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

personalRe = re.compile(r"""\n(Personal Details|Personal Information|Personal|About Me|Strengths|Personal Profile)""", re.IGNORECASE)
pers_whole_test = personalRe.sub('-PERSONAL-', obj_whole_test)

interestRe = re.compile(r"""\n(Personal Interests|Hobbies|Activities|Interests|Other Interests)""", re.IGNORECASE)
interest_whole_test = interestRe.sub('-INTERESTS-', pers_whole_test)

certifRe = re.compile(r"""\n(Certifications|Honours|Honors|Awards|Prizes|Achievements|Accomplishments)""", re.IGNORECASE)
certif_whole_test = certifRe.sub('-CERTIF-', interest_whole_test)

refRe = re.compile(r"""\nReferences""", re.IGNORECASE)
whole_test = refRe.sub('-REF-', certif_whole_test)
file_obj.close( )

# Publications
# Internships

# parse the processed document
doc.parseString(whole_test)
idTag += sys.argv[2] + "</field>\n"
eduTag += "</field>\n"
objTag += "</field>\n"
skillTag += "</field>\n"
personalTag += "</field>\n"
experienceTag += "</field>\n"
interestTag += "</field>\n"
certifTag += "</field>\n"
refTag += "</field>\n"
content = idTag + personalTag + objTag + skillTag + eduTag + experienceTag + interestTag + certifTag + refTag
__xmlfile = "<add>\n<doc>\n" + content + "</doc>\n</add>"

# remove ampersands as XML file will be invalid otherwise
amp = re.compile('&')
_xmlfile = amp.sub('and', __xmlfile)

# remove empty fields
empty_field=re.compile('<field name=\"[a-z]+\"></field>\n')
xmlfile = empty_field.sub('', _xmlfile)

# remove '\r's - optional
# cr=re.compile('\r')
# ascii_text = cr.sub('\n', xmlfile)
out = open(sys.argv[3], 'w')
out.write(codecs.BOM_UTF8)
out.write(xmlfile)
out.close()

