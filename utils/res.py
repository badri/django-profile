#!/usr/bin/python
from pyparsing import *
import sys, re
import codecs

from elementtree import ElementTree as ET
from demo.settings import KEYWORDS_XML

usage = """\
./res.py <filename>.txt
"""

"""
TODO:
1. from a given resume, extract only educational info - done
2. from edu info, extract only a list of shools or colleges
	- have an xml file for key terms for schools and colleges. Ex: for school - sch, school, secondary, for college - university, institution, insitute, univ etc

	- a script which will use the terms, look into the user data and extract the information
	- another script whihc will normalize the seacrh results(optional)
          Ex. grouping of NE univs in US, normalizing Carnige Mellon univ, Carnige Mellonuniversity into 1 form.
	- dynamically create your attribute file in flamenco.
 Publications
 Internships
 3. add a settings variable for keywords.xml - done
 4. add filter.xml in accordance with requirement #2.

"""


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

        # contains catchwords
        self.root = ET.parse(KEYWORDS_XML).getroot()
        
        # open the resume
        _whole_test = resume

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
        
        edu_keywords = self.returnKeywords('education')
        eduRe = re.compile(r'\n('+edu_keywords+')', re.IGNORECASE)
        edu_whole_test = eduRe.sub('-EDUCATION-',_whole_test)

        skill_keywords = self.returnKeywords('skills')
        skillRe = re.compile(r'\n('+skill_keywords+')', re.IGNORECASE)
        skill_whole_test = skillRe.sub('-SKILLS-', edu_whole_test)

        exp_keywords = self.returnKeywords('experience')
        expRe = re.compile(r'\n('+exp_keywords+')', re.IGNORECASE)
        exp_whole_test = expRe.sub('-EXPERIENCE-', skill_whole_test)

        obj_keywords = self.returnKeywords('objective')
        objRe = re.compile(r'\n('+obj_keywords+')', re.IGNORECASE)
        obj_whole_test = objRe.sub('-OBJECTIVE-', exp_whole_test)

        personal_keywords = self.returnKeywords('personal')
        personalRe = re.compile(r'\n('+personal_keywords+')', re.IGNORECASE)
        pers_whole_test = personalRe.sub('-PERSONAL-', obj_whole_test)

        interest_keywords = self.returnKeywords('interests')
        interestRe = re.compile(r'\n('+interest_keywords+')', re.IGNORECASE)
        interest_whole_test = interestRe.sub('-INTERESTS-', pers_whole_test)

        certif_keywords = self.returnKeywords('certifications')
        certifRe = re.compile(r'\n('+certif_keywords+')', re.IGNORECASE)
        certif_whole_test = certifRe.sub('-CERTIF-', interest_whole_test)

        ref_keywords = self.returnKeywords('references')
        refRe = re.compile(r'\n('+ref_keywords+')', re.IGNORECASE)
        
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
    @property
    def education(self):
        return self.eduTag.strip()

    @property
    def objective(self):
        return self.objTag.strip()

    @property
    def skills(self):
        return self.skillTag.strip()

    @property
    def personal(self):
        return self.personalTag.strip()

    @property
    def experience(self):
        return self.experienceTag.strip()

    @property
    def interests(self):
        return self.interestTag.strip()

    @property
    def certifications(self):
        return self.certifTag.strip()

    @property
    def references(self):
        return self.refTag.strip()

    def returnKeywords(self, attribute):
        keywords = ''
        for x in self.root.getiterator(attribute):
            for word in x.text.strip().split('\n'):
                keywords+=word+'|'

        return keywords[:-1]
        

if __name__=='__main__':

    if len(sys.argv) < 2:
	print usage
	sys.exit()

    print sys.argv

    p = ResumeParser(open(sys.argv[1]).read())

    print p.skills

    print p.personal

    print p.education
