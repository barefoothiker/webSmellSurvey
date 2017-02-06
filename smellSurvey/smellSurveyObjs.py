class QuestionAnswerObj(object):
    def __init__(self):
        self.questionAnswer = ''
        self.displayDisabledFlag = True        
        self.questionAnswerInstance = ''
        self.isAnswered = False
        self.questionAnswerChoiceList = []
        self.questionAnswerTimeUnitList = []        
    def __unicode__(self):
        return str(self.questionAnswer)

class QuestionObj(object):
    def __init__(self):
        self.question = ''
        self.parentQuestionList = ''
        self.questionAnswerObjList = []
    def __unicode__(self):
        return str(self.question)

class UPINObj(object):
    def __init__(self):
        self.upin = ''
        self.administration = ''
        self.columnValueList = []
    def __unicode__(self):
        return str(self.upin)

class SectionObj(object):
    def __init__(self):
        self.section = ''
        self.colorFlag = False
        self.questionObjList = []
    def __unicode__(self):
        return str(self.section)

class QuestionnaireObj(object):
    def __init__(self):
        self.questionnaire = ''
        self.selectedFlag = False
        self.sectionObjList = []
    def __unicode__(self):
        return str(self.section)
    
class StudyObj(object):
    def __init__(self):
        self.study = ''
        self.questionnaireObjList = []
        self.isSelected = False
    def __unicode__(self):
        return str(self.study)
    
class SiteObj(object):
    def __init__(self):
        self.site = ''
        self.isSelected = False
    def __unicode__(self):
        return str(self.site)

class PatientObj(object):
    def __init__(self):
        self.patient = ''
        self.studyObjList = []
    def __unicode__(self):
        return str(self.study)

class AdministratorObj(object):
    def __init__(self):
        self.user = ''
        self.siteObjList = []
        self.studyObjList = []
    def __unicode__(self):
        return str(self.study)

class AdministrationObj(object):
    def __init__(self):
        self.adminsitration = ''
        self.sectionObjList = []
    def __unicode__(self):
        return str(self.adminsitration)

class HeaderObj(object):
    def __init__(self):
        self.sectionName = ''
        self.questionText = ''
        self.questionAnswerText = ''
        self.questionOntologyClassSubClass = ''
        self.questionOntologyIndividual = ''
        self.questionAnswerOntology = ''        
        self.questionAnswerId = ''
    def __unicode__(self):
        return str(self.sectionName)
                        