from django.db import models
from django.contrib.auth.models import User
    
class OntologyType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name

class Ontology(models.Model):
    name = models.CharField(max_length=512)
    ontologyType = models.ForeignKey(OntologyType, blank = True, null = True )    
    description = models.CharField(max_length=256, blank = True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children') 
    def __str__(self):
        return self.name

class QuestionAnswerType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name

class QuestionAnswerDataType(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    name=models.CharField(max_length=512)
    description=models.CharField(max_length=256, blank=True, null=True)
    version = models.IntegerField()
    language = models.ForeignKey(Language, blank = True, null = True )    
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length = 512)
    questionnaire = models.ForeignKey(Questionnaire)
    sequence = models.IntegerField()
    def __str__(self):
        return self.name
    
class QuestionAnswer(models.Model):

    questionnaire = models.ForeignKey(Questionnaire)

    text = models.CharField(max_length=512)
    questionAnswerId = models.IntegerField()

    questionAnswerType = models.ForeignKey(QuestionAnswerType, blank = True, null = True)  
    questionAnswerDataType = models.ForeignKey(QuestionAnswerDataType, blank = True, null = True)  
    
    questionAnswerRangeLower = models.IntegerField(blank = True, null = True)  
    questionAnswerRangeUpper = models.IntegerField(blank = True, null = True)  

    questionAnswerOntology = models.ForeignKey(Ontology, blank = True, null = True, related_name = "answerOntologyClassSubClass" ) 

    requiredFlag = models.NullBooleanField() 
    phiFlag = models.NullBooleanField()
    
    pictureURL = models.CharField(max_length=256, blank = True, null = True ) 
    def __str__(self):
        return str(self.text)

class QuestionAnswerTimeUnit(models.Model):

    text = models.CharField(max_length=256)
    questionAnswer = models.ForeignKey(QuestionAnswer)  

    def __str__(self):
        return str(self.text)

class QuestionAnswerChoice(models.Model):

    text = models.CharField(max_length=512)
    questionAnswer = models.ForeignKey(QuestionAnswer)  

    choiceOntology = models.ForeignKey(Ontology, blank = True, null = True, related_name = "choiceOntology" ) 

    def __str__(self):
        return str(self.text)

class Question(models.Model):

    text = models.TextField(max_length=1024)

    section = models.ForeignKey(Section)
    questionId = models.IntegerField()
    answers = models.ManyToManyField(QuestionAnswer)

    parent = models.ForeignKey("self", null=True,blank=True, related_name = "parentQuestion")
    parentAnswer = models.ForeignKey(QuestionAnswer, null=True,blank=True, related_name = "parentAnswer")
    #parentAnswerValue = models.CharField(max_length=256, null=True,blank=True)

    ontologyClassSubClass = models.ForeignKey(Ontology, blank = True, null = True, related_name = "questionOntologyClassSubClass"  ) 
    ontologyIndividual = models.ForeignKey(Ontology, blank = True, null = True, related_name = "questionOntologyIndividual" ) 
    
    #isAnswered = models.BooleanField() 

    def __str__(self):
        return self.text    

class Role(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank = True)
    isSuperUser = models.BooleanField()
    isAdministrator = models.BooleanField()    
    isPatient = models.BooleanField()
    isTester = models.BooleanField()    
    def __str__(self):
        return self.name
    class Admin:
        list_display=('id','role_name','description')
        pass

class Site(models.Model):

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    def __str__(self):
        return self.name

class Study(models.Model):

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    #questionnaires = models.ManyToManyField(Questionnaire)
    
    questionnaire = models.ForeignKey(Questionnaire)
    
    def __str__(self):
        return self.name

class SurveyUser(models.Model):
    
    user = models.ForeignKey(User)

    role = models.ForeignKey(Role, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

class Administrator(SurveyUser):

    allowedSites = models.ManyToManyField(Site)
    allowedStudies = models.ManyToManyField(Study)

    def __str__(self):
        return str(self.user.username)

class Patient(SurveyUser):

    studies = models.ManyToManyField(Study)

    defaultStudy = models.ForeignKey(Study, related_name="defaultStudy")
    defaultSite = models.ForeignKey(Site, related_name="defaultSite")
    defaultAdministrator = models.ForeignKey(Administrator, related_name="defaultAdministrator")
    
    surveyLink = models.CharField(max_length=256)
    
    isDeleted = models.BooleanField()

    def __str__(self):
        return str(self.id)

class UPIN(models.Model):

    upinId = models.IntegerField()
    patient = models.ForeignKey(Patient)
    study = models.ForeignKey(Study)
    sessionId = models.CharField(max_length = 512, null=True, blank=True)

    def __str__(self):
        return str(self.upinId)
    
class Administration(models.Model):

    upin = models.ForeignKey(UPIN)

    questionnaire = models.ForeignKey(Questionnaire)
    site = models.ForeignKey(Site)
    administrator = models.ForeignKey(Administrator, related_name = "administrator")
    
    startTime = models.DateTimeField(null=True, blank=True)
    
    stopTime = models.DateTimeField(null=True, blank=True)
    
    #percentageComplete = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
        
class QuestionAnswerInstance(models.Model):
    
    administration = models.ForeignKey(Administration)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(QuestionAnswer)
    timeStamp = models.DateTimeField(null=True,blank=True)

    answerText = models.CharField(max_length = 256, null=True, blank=True)
    answerText2 = models.CharField(max_length = 256, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
#class Survey(models.Model):

    #link = models.CharField(max_length = 1024)
    #patient = models.ForeignKey(Patient)
    #createdOn = models.DateTimeField()

    #def __str__(self):
        #return self.link      
        
