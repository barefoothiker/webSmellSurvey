from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  

from io import BytesIO

from reportlab.lib.styles import ParagraphStyle
from smellSurvey.models import *
from smellSurvey.smellSurveyObjs import *
from smellSurvey.smellSurveyConstants import *

from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.http import Http404

import numpy as np

import os, sys, traceback

#from neo4j.v1 import GraphDatabase, basic_auth

from django.conf import settings
import numpy
import datetime

#from reportlab.graphics.barcode import code39, code128, code93

#from datetime import timezone

import os.path

from django.contrib.auth import logout

import csv

import random
from random import randint

from random import choice
from string import ascii_uppercase

from django.contrib import messages

from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

#from django.utils.encoding import smart_unicode

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/registration/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })

#@login_required
def landing(request):

    surveyLink = request.GET.get("surveyLink","" )

    user = ''

    if surveyLink != '':
        
        patients = Patient.objects.filter(surveyLink = surveyLink)
        
        if len(patients) > 0:
            
            patient = patients[0]
            
            user = patient.user

            #urlUsers = User.objects.filter ( username = patient.user.username )
    
            #if len(urlUsers) > 0:
    
                #user = urlUsers[0]
    
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # logout any existing users
            
            logout(request)

            login(request, user)
    else:

        print ( " user = " + str(request.user) + " anonymous " + str(request.user.is_anonymous))

        if request.user and not request.user.is_anonymous():

            user = request.user

        else:

            print ( " *** IN ELSE *** ")

            return HttpResponseRedirect('/accounts/login')
        
    if  user == '':
        
        logout(request)        
        return HttpResponseRedirect('/accounts/login')

    study = ''

    upins = []

    newUPINID = 0

    administrations = []

    superUserRoles = Role.objects.filter(name = SUPER_USER_ROLE_NAME)

    if len(superUserRoles) == 0:

        return render_to_response('smellSurvey/landing.html', {

            "user" : user,

        },  RequestContext(request))

    else:

        superUserRole = superUserRoles[0]

    surveyUsers = SurveyUser.objects.filter(user = user)

    surveyUser = ''

    print ( " num users = " + str(surveyUsers) )

    if len(surveyUsers) > 0:

        surveyUser = surveyUsers[0]

        if surveyUser.role.isAdministrator:

            administrators = Administrator.objects.filter(user = request.user)

            if len(administrators) > 0:

                surveyUser = administrators[0]

                administrations = Administration.objects.filter(administrator = administrators[0])

        elif surveyUser.role.isPatient:

            patients = Patient.objects.filter(user = request.user)

            if len(patients) > 0:

                surveyUser = patients[0]

                patient = surveyUser

                study = ''

                selectedStudyId = request.GET.get('studyId', 0)

                if selectedStudyId != 0:

                    study = Study.objects.get(pk = selectedStudyId)

                else:

                    study = patient.defaultStudy

                study = patient.defaultStudy

                upins = UPIN.objects.filter(patient = patient, study = study)

                administrations = Administration.objects.filter( upin__in = upins)

                notFound = True

                newUPINID = 0

                while notFound:

                    newUPINID = randint(100001, 999999)

                    upinCount = UPIN.objects.filter(upinId = newUPINID).count()

                    if upinCount == 0:

                        notFound = False

    #print ( " surveyUser = " + str(    surveyUser.role   ) )

    return render_to_response('smellSurvey/landing.html', {

        "user" : user,
        "surveyUser" : surveyUser,
        "study" : study,
        "upins" : upins,
        "newUPINID" : newUPINID,
        "administrations" : administrations,

    },  RequestContext(request))


@login_required
def processLanding(request):

    smellSurveyHomeButton = request.POST.get('smellSurveyHomeButton', "0")

    if smellSurveyHomeButton == "0":
        return home( request )
    if smellSurveyHomeButton == "1":
        return uploadQuestionnaire( request )
    elif smellSurveyHomeButton == "2":
        return listQuestionnaires( request )
    elif smellSurveyHomeButton == "3":
        return listSites ( request )
    elif smellSurveyHomeButton == "4":
        return listStudies ( request )
    elif smellSurveyHomeButton == "5":
        return listPatients ( request )
    elif smellSurveyHomeButton == "6":
        return listRoles ( request )
    elif smellSurveyHomeButton == "7":
        return listAdministrators ( request )
    elif smellSurveyHomeButton == "8":
        return selectSiteStudy ( request )
    elif smellSurveyHomeButton == "9":
        return listAdministrations ( request )
    elif smellSurveyHomeButton == "10":
        return listSuperUsers ( request )

@login_required
def uploadQuestionnaire(request):

    try:

        questionnaires = Questionnaire.objects.all()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/uploadQuestionnaire.html', {

        "questionnaires":questionnaires,

    },  RequestContext(request))

@login_required
def submitUploadQuestionnaire(request):

    try:

        questionnaireNameCustom = request.POST.get("questionnaireNameCustom","" )

        errorFile = open("errorUpload.txt","w")

        questionnaireFile = request.FILES["questionnaireName"]

        if questionnaireNameCustom == "":

            questionnaireNameCustom = questionnaireFile

        print ( "questionnaireNameCustom = " + questionnaireNameCustom)

        questionnaires = Questionnaire.objects.filter (name = questionnaireNameCustom)

        allQuestionnaires = Questionnaire.objects.all()

        messages = []

        questionnaire = ""

        if len(questionnaires) > 0:

            messages.append("Questionnaire already exists. Please choose a different name.")

            return render_to_response('smellSurvey/uploadQuestionnaire.html', {

                "questionnaires":questionnaires,

                "messages": messages,

            },  RequestContext(request))

        else:

            questionnaire = Questionnaire (name = questionnaireNameCustom, version = 1)

            questionnaire.save()
    
        questionnaireOutputFile = open(settings.DATA_OUTPUT_FOLDER + "/" + questionnaire.name + ".csv", "w")        

        data = questionnaireFile.read().decode()

        dataLines = data.split("\r")

        sectionSequence = 0

        for index, dataLine in enumerate ( dataLines ) :
            
            questionnaireOutputFile.write(dataLine)            
        
            if index == 0:
                continue
            #if index > 1: 
                #break

            dataValues = dataLine.replace("\t","").replace("\n","").split(",")

            #Question ID        Question Order  Section Question        Question Ontology - class and subclass  Question Ontology - individual  Answer ID       Answer Type (single choice, multiple choice, choice) select column      Answer  Answer Ontology individual      data type (integer, datetime, choice, choice_and_datetime, integer_and_timeunit, text) answer text 3rd column   range   choice  choice ontology Parent Question Parent Answer   required        PHI     Picture

            if len(dataValues) < 19:
                
                print ( " too few data values ")

                break

            questionId = dataValues[0].strip()
            questionOrder = dataValues[1].strip()
            sectionName = dataValues[2].strip()

            questionText = dataValues[3].strip()
            
            print ( " ^^^^^^^^^^ for question ^^^^^^^^ " + str(questionText) )

            questionOntologyClassSubClassName = dataValues[4].strip()
            questionOntologyIndividualName = dataValues[5].strip()

            questionAnswerId = dataValues[6].strip()
            questionAnswerTypeName = dataValues[7].strip()

            questionAnswerText = dataValues[8].strip()

            questionAnswerOntologyName = dataValues[9].strip()

            questionAnswerDataTypeName = dataValues[10].strip()

            questionAnswerTimeUnit = dataValues[11].strip()

            questionAnswerValueRange = dataValues[12].strip()

            questionAnswerChoices = dataValues[13].strip()

            questionAnswerChoiceOntologies = dataValues[14].strip()

            parentQuestionId = dataValues[15].strip()

            parentQuestionAnswerId = dataValues[16].strip()

            requiredFlag = dataValues[17].strip()

            phiFlag = dataValues[18].strip()

            pictureURL = dataValues[19].strip()

            questionAnswerRangeLower = 0
            questionAnswerRangeUpper = 0

            try:

                if questionAnswerValueRange != '':

                    questionAnswerValueRangeLimits = questionAnswerValueRange.split(" ")

                    if len(questionAnswerValueRangeLimits) > 0:

                        questionAnswerRangeLower = int(questionAnswerValueRangeLimits[0])

                        questionAnswerRangeUpper = int(questionAnswerValueRangeLimits[1])

            except:

                #print ( " error getting range values " )

                pass

            requiredFlag = True if requiredFlag == 'Y' else False
            phiFlag =  True if phiFlag == 'Y' else False

            ontologyTypeClassSubClasses = OntologyType.objects.filter ( name = "classSubClass")

            ontologyTypeClassSubClass = ''

            if len(ontologyTypeClassSubClasses) == 0:

                ontologyTypeClassSubClass = OntologyType ( name = "classSubClass", description = "classSubClass description")

                ontologyTypeClassSubClass.save()

            else:

                ontologyTypeClassSubClass = ontologyTypeClassSubClasses[0]

            ontologyTypeIndividuals = OntologyType.objects.filter ( name = "Individual")

            ontologyTypeIndividual = ''

            if len(ontologyTypeIndividuals) == 0:

                ontologyTypeIndividual = OntologyType ( name = "Individual", description = "Individual description")

                ontologyTypeIndividual.save()

            else:

                ontologyTypeIndividual = ontologyTypeIndividuals[0]
                
            questionAnswerTypes = []
            
            questionAnswerType = ''
            
            if questionAnswerTypeName != '':

                questionAnswerTypes = QuestionAnswerType.objects.filter(name = questionAnswerTypeName)
    
                print ( " ::::::: questionAnswerDataTypeName = " + str(questionAnswerDataTypeName))
    
                if len(questionAnswerTypes) > 0:
    
                    questionAnswerType = questionAnswerTypes[0]
    
                else:
    
                    if questionAnswerTypeName != '':
    
                        questionAnswerType = QuestionAnswerType(name = questionAnswerTypeName, description = questionAnswerTypeName)
    
                        questionAnswerType.save()
                        
            print ( " :::::____:: questionAnswerTypeName = " + str(questionAnswerTypeName) + " *&*&*&* " + str(questionAnswerType))

            questionAnswerDataTypes = []
            
            questionAnswerDataType = ''
            
            if questionAnswerDataTypeName != '':

                questionAnswerDataTypes = QuestionAnswerDataType.objects.filter(name = questionAnswerDataTypeName)
    
                print ( " ::::::: questionAnswerDataTypeName = " + str(questionAnswerDataTypeName))
    
                questionAnswerDataType = ''
    
                if len(questionAnswerDataTypes) > 0:
    
                    questionAnswerDataType = questionAnswerDataTypes[0]
    
                else:
    
                    if questionAnswerDataTypeName != '':
    
                        questionAnswerDataType = QuestionAnswerDataType(name = questionAnswerDataTypeName, description = questionAnswerDataTypeName)
    
                        questionAnswerDataType.save()
    
            sections = Section.objects.filter( questionnaire = questionnaire, name = sectionName)

            section = ''

            if len(sections) > 0:

                section = sections[0]

            else:

                section = Section(name = sectionName, questionnaire = questionnaire, sequence = sectionSequence)

                section.save()

                sectionSequence = sectionSequence + 1

            questionOntologyClassSubClasses = Ontology.objects.filter( name = questionOntologyClassSubClassName, ontologyType = ontologyTypeClassSubClass )

            questionOntologyClassSubClass = ''

            if len(questionOntologyClassSubClasses) > 0:

                questionOntologyClassSubClass = questionOntologyClassSubClasses[0]

            else:

                questionOntologyClassSubClass = Ontology(name = questionOntologyClassSubClassName , ontologyType = ontologyTypeClassSubClass)

                questionOntologyClassSubClass.save()

            questionOntologyIndividuals = Ontology.objects.filter( name = questionOntologyIndividualName, ontologyType = ontologyTypeIndividual )

            questionOntologyIndividual = ''

            if len(questionOntologyIndividuals) > 0:

                questionOntologyIndividual = questionOntologyIndividuals[0]

            else:

                questionOntologyIndividual = Ontology(name = questionOntologyIndividualName , ontologyType = ontologyTypeIndividual)

                questionOntologyIndividual.save()

            questionAnswerOntologies = Ontology.objects.filter( name = questionAnswerOntologyName, ontologyType = ontologyTypeIndividual)

            questionAnswerOntology = ''

            if len(questionAnswerOntologies) > 0:

                questionAnswerOntology = questionAnswerOntologies[0]

            else:

                questionAnswerOntology = Ontology(name = questionAnswerOntologyName)

                questionAnswerOntology.save()

            questionAnswerChoiceOntologyNameList = questionAnswerChoiceOntologies.split("**")

            questionAnswerChoiceOntologyList = []

            for questionAnswerChoiceOntologyName in questionAnswerChoiceOntologyNameList:

                questionAnswerChoiceOntologies = Ontology.objects.filter( name = questionAnswerChoiceOntologyName, ontologyType = ontologyTypeIndividual)

                if len(questionAnswerChoiceOntologies) > 0:

                    questionAnswerChoiceOntology = questionAnswerChoiceOntologies[0]

                else:

                    questionAnswerChoiceOntology = Ontology(name = questionAnswerChoiceOntologyName, ontologyType = ontologyTypeIndividual)

                    questionAnswerChoiceOntology.save()

                questionAnswerChoiceOntologyList.append(questionAnswerChoiceOntology)

            parentQuestion = ''
            
            if parentQuestionId != "":

                #print (" @@@@@@@ parentQuestionId = " + str(parentQuestionId))

                parentQuestions = Question.objects.filter(questionId = parentQuestionId, section = section)

                if len(parentQuestions) > 0:

                    parentQuestion = parentQuestions[0]

                    #print (" --- for question --- " + str(question.text) + " !!!! parentQuestion !!!! " + str(parentQuestion) )

            parentQuestionAnswer = ''

            #print ( " ::::::::: parent answer id ::::::::::: " + str(parentQuestionAnswerId) )

            if parentQuestionAnswerId != "" and parentQuestion != '' :

                questionAnswers = parentQuestion.answers.all()

                for questionAnswer in questionAnswers:

                    #print ( " for questionAnswer = " + questionAnswer.text + " answer Id = " + str (questionAnswer.questionAnswerId) )

                    if questionAnswer.questionAnswerId == int(parentQuestionAnswerId):

                        parentQuestionAnswer = questionAnswer

                #print (" ** parentQuestionAnswer ** " + str(parentQuestionAnswer) + " for question " + str(parentQuestion.text))

                #if len(parentQuestionAnswers) > 0:

                    #parentQuestionAnswerIds = [x.questionAnswerId in parentQuestionAnswers]

                    #if parentQuestionAnswerId in parentQuestionAnswerIds:

                        #parentQuestionAnswer = [x if x.questionAnswerId == parentQuestionAnswerId else '' for x in parentQuestionAnswers][0]

            questions = Question.objects.filter(questionId = int(questionId), text = questionText, section = section)

            question = ''

            if len(questions) > 0:

                question = questions[0]

            else:

                if parentQuestion != '':

                    if parentQuestionAnswer == '':

                        #print ( "########## ERROR ########### " + questionText)
                        errorFile.write(questionText + "--" + str(parentQuestion) + "\n")

                    else:

                        #print ( " ****** $$$ for parent subclass = " + str(questionOntologyClassSubClass) + " individual = " + str(questionOntologyIndividual) ) 

                        question = Question(text = questionText, questionId = int(questionId), ontologyClassSubClass = questionOntologyClassSubClass, ontologyIndividual = questionOntologyIndividual, section = section, parent = parentQuestion, parentAnswer = parentQuestionAnswer)

                else:

                    #print ( " IN ELSE **** ")

                    #print ( " **NOT IN parent subclass = " + str(questionOntologyClassSubClass) + " individual = " + str(questionOntologyIndividual) ) 

                    question = Question(text = questionText, questionId = int(questionId) , ontologyClassSubClass = questionOntologyClassSubClass, ontologyIndividual = questionOntologyIndividual, section = section)

                if question != '' :

                    question.save()

                #else:

                    #print ( " !!!!!!!!!!!  Error DID NOT SAVE ####### ")
                    
            if questionAnswerTypeName != '':

                questionAnswers = QuestionAnswer.objects.filter(questionnaire = questionnaire,text = questionAnswerText, questionAnswerId = int(questionAnswerId), questionAnswerType = questionAnswerType)
                
            else:
                
                questionAnswers = QuestionAnswer.objects.filter(questionnaire = questionnaire,text = questionAnswerText, questionAnswerId = int(questionAnswerId))                

            #print ( " **** $$$$$$  for answer **** " + str(questionAnswerText) + " id = " + str(questionAnswerId) )

            if len(questionAnswers) > 0:

                questionAnswer = questionAnswers[0]

                #print ( " ##### *** found answer **** " + str(questionAnswerText)  + " id = " + str(questionAnswerId))

            else:

                questionAnswer = QuestionAnswer(questionnaire = questionnaire, text = questionAnswerText, questionAnswerId = int(questionAnswerId) , questionAnswerOntology = questionAnswerOntology, questionAnswerRangeLower = questionAnswerRangeLower, questionAnswerRangeUpper = questionAnswerRangeUpper, requiredFlag = requiredFlag, phiFlag = phiFlag, pictureURL = pictureURL)

                if questionAnswerTypeName != '':
                    questionAnswer.questionAnswerType = questionAnswerType

                if questionAnswerDataTypeName != '':
                    questionAnswer.questionAnswerDataType = questionAnswerDataType

                print ( " !!!!!!! *** for answer **** " + str(questionAnswerText)  + " type = " + str(questionAnswerType))

                questionAnswer.save()

            question.answers.add(questionAnswer)

            question.save()

            questionAnswerChoiceNameList = questionAnswerChoices.split("**")

            for index, questionAnswerChoiceName in enumerate ( questionAnswerChoiceNameList ) :

                if len(questionAnswerChoiceOntologyList) > index:

                    questionAnswerChoice = QuestionAnswerChoice ( text = questionAnswerChoiceName, questionAnswer = questionAnswer, choiceOntology = questionAnswerChoiceOntologyList[index])

                else:

                    questionAnswerChoice = QuestionAnswerChoice ( text = questionAnswerChoiceName, questionAnswer = questionAnswer)
                
                questionAnswerChoices = QuestionAnswerChoice.objects.filter ( text = questionAnswerChoiceName, questionAnswer = questionAnswer)
                
                if len(questionAnswerChoices) == 0:
                    questionAnswerChoice.save()
                
            questionAnswerTimeUnitList = questionAnswerTimeUnit.split("**")              
    
            for index, questionAnswerTimeUnitName in enumerate ( questionAnswerTimeUnitList ) :
    
                questionAnswerTimeUnit = QuestionAnswerTimeUnit ( text = questionAnswerTimeUnitName, questionAnswer = questionAnswer)
    
                questionAnswerTimeUnits = QuestionAnswerTimeUnit.objects.filter ( text = questionAnswerTimeUnitName, questionAnswer = questionAnswer)
                
                if len(questionAnswerTimeUnits) == 0:    
                    questionAnswerTimeUnit.save()
                
            #if questionText == "When did this problem start?" :
            
                #break

        allQuestionnaires = Questionnaire.objects.all()

        errorFile.close()
        
        questionnaireOutputFile.close()        

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listQuestionnaires.html', {

        "questionnaires":allQuestionnaires,

        "messages": messages,

    },  RequestContext(request))

@login_required
def selectParameters(request):
    
    ''' Display Questionnaire
    Input: Request
    Output QuestionnaireObj for display
    '''

    try:

        surveyUser = ''
        
        administrator = ''
        
        sites = ''
        
        studies = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass
        
        print ( " survey user = " + str(surveyUser))

        if surveyUser.role.isSuperUser or surveyUser.role.isTester:

            sites = Site.objects.all()

            studies = Study.objects.all()
            
            administrators = Administrator.objects.all()            
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user)[0] 
            
            studies = administrator.allowedStudies.all()
            
            sites = administrator.allowedSites.all()   
            
            administrators = [administrator]            
                
    except:

        traceback.print_exc(file=sys.stdout)    

    return render_to_response("smellSurvey/selectParameters.html",{
        "surveyUser" : surveyUser,
        "sites":sites,
        "studies": studies,
        "administrators": administrators,

    }, RequestContext(request))

@login_required
def listQuestionnaires(request):
    questionnaires = Questionnaire.objects.all()
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass     

    return render_to_response("smellSurvey/listQuestionnaires.html",{

        'questionnaires': questionnaires,
        'surveyUser':surveyUser,

    }, RequestContext(request))

@login_required
def displayQuestionnaire(request):

    ''' Display Questionnaire
    Input: Request
    Output QuestionnaireObj for display
    '''

    try:

        questionnaireId = request.POST.get("questionnaireId",0)

        questionnaire = Questionnaire.objects.get(pk=questionnaireId)

        questionnaireObj = QuestionnaireObj()

        questionnaireObj.questionnaire = questionnaire

        sections = Section.objects.filter(questionnaire = questionnaire)

        for section in sections:

            sectionObj = SectionObj()

            sectionObj.section = section

            print ( " !!!!!!!########@@@@@@@ adding section " + str(section.name) )

            questions = Question.objects.filter( section = section ).order_by("questionId")

            for question in questions:

                print ( " **** adding question " + str(question.text) )

                questionObj = QuestionObj()

                questionObj.question = question

                for questionAnswer in question.answers.all():

                    questionAnswerObj = QuestionAnswerObj()

                    questionAnswerObj.questionAnswer = questionAnswer

                    questionObj.questionAnswerObjList.append(questionAnswerObj)

                sectionObj.questionObjList.append(questionObj)

            questionnaireObj.sectionObjList.append(sectionObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response("smellSurvey/displayQuestionnaire.html", {
        "questionnaireObj" : questionnaireObj,

    }, RequestContext(request))

@login_required
def displayAdministration(request):

    ''' Display Administration
    Input: Request
    Output AdministrationObj for display
    '''

    try:

        surveyUser = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        prevQuestion = ''
        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''
        prevSection = ''

        administrationId = request.POST.get('administrationId', 0)

        backToQuestionnaireFlagValue = request.POST.get('backToQuestionnaireFlag', "0")

        backToQuestionnaireFlag = False

        if backToQuestionnaireFlagValue == "1":
        
            backToQuestionnaireFlag = True

        administration = Administration.objects.get(pk=administrationId)

        administrator = administration.administrator

        site = administration.site
        study = administration.upin.study

        patient = administration.upin.patient
        questionnaire = administration.questionnaire

        upinId = administration.upin.upinId

        questionId = request.POST.get('questionId', 0)

        previewFlag = request.POST.get('previewFlag', 0)

        question = ''

        questionAnswers = []

        sectionId = request.POST.get('sectionId', 0)

        currentSection = 0

        if sectionId != 0:

            currentSection = Section.objects.get (pk = sectionId)

        if questionId != 0:
            question = Question.objects.get (pk = questionId)
            questionAnswers = QuestionAnswer.objects.filter( question = question )

            section = question.section

        #print (" ** question ** " + str(question) )

        sections = Section.objects.filter(questionnaire = questionnaire).order_by("sequence")

        #upinId = request.POST.get('upinId', 0)

        #print (" ** section ** " + str(section) )

        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''

        isQuestionAnswered = False

        questionAnswerId = 0

        administrationObj = AdministrationObj()

        administrationObj.administration = administration

        questionnaire = administration.questionnaire

        sections = Section.objects.filter(questionnaire = questionnaire)

        for section in sections:

            sectionObj = SectionObj()

            sectionObj.section = section

            #print ( " adding section " + str(section.name) )

            questions = Question.objects.filter( section = section ).order_by("questionId")

            isSectionAnswered = False

            for question in questions:

                questionObj = QuestionObj()

                questionObj.question = question

                isAnswered = False

                for questionAnswer in question.answers.all():

                    questionAnswerObj = QuestionAnswerObj()

                    questionAnswerObj.questionAnswer = questionAnswer

                    questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)

                    if len ( questionAnswerInstances ) > 0:

                        questionAnswerInstance = questionAnswerInstances[0]

                        #print (" &&&&  for question answer = " + str(questionAnswer) + " is answered ")

                        questionAnswerObj.isAnswered = True
                        questionAnswerObj.questionAnswerInstance = questionAnswerInstance

                    #if not questionAnswerObj.isAnswered and question.parentQuestion and question.parentAnswer != '':

                        #continue

                        questionObj.questionAnswerObjList.append(questionAnswerObj)

                        isAnswered = True

                        isSectionAnswered = True

                if isAnswered:

                    sectionObj.questionObjList.append(questionObj)
                    
                else:
                    
                    #print ( " ** setting color to red **" + str(sectionObj.section.name) )                      
                    
                    if not question.parent: 
                    
                        sectionObj.colorFlag = True

            #if isSectionAnswered:
            
            #print ( " ***** YYYY adding section " + str(sectionObj.section.name) )            

            administrationObj.sectionObjList.append(sectionObj)
            
        percentageComplete = int(getPercentageCompleteTotal(administration))
        showSectionPercentageFlag = False
        
        print ( " percent complete = " + str(percentageComplete) )              

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response("smellSurvey/displayAdministration.html", {
        "administrationObj" : administrationObj,
        "upinId": upinId,

        "site" : site,
        "study" : study,
        "sections" : sections,
        "patient" : patient,
        "questionnaire" : questionnaire,

        "administration" : administration,
        "administrator" : administrator,
        "backToQuestionnaireFlag": backToQuestionnaireFlag ,

        'prevQuestion' : prevQuestion,
        'prevQuestionAnswer': prevQuestionAnswer,
        'prevQuestionAnswerText':prevQuestionAnswerText,
        'prevSection': prevSection,
        
        'percentageComplete':percentageComplete,
        'showSectionPercentageFlag':showSectionPercentageFlag,

        'question': question,
        'questionAnswers':questionAnswers,
        'section':currentSection,
        'previewFlag':previewFlag,
        'surveyUser':surveyUser,        

    }, RequestContext(request))

@login_required
def listQuestions(request):

    questions = Question.objects.all()

    return render_to_response("smellSurvey/listQuestions.html", {

        "questions" : questions,

    },  RequestContext(request))

@login_required
def editQuestion(request):

    questionId = request.POST.get("questionId",0 )

    question = Question.objects.get(pk = questionId)

    questionObj = QuestionObj()

    questionObj.question = question

    for questionAnswer in question.answers.all():

        questionAnswerObj = QuestionAnswerObj()

        questionAnswerObj.questionAnswer = questionAnswer

        #print ( " type = " + str(questionAnswer.questionAnswerType.name) )

        if questionAnswer.questionAnswerType.name != "Boolean" :

            #print ( " ***** in if " )

            questionAnswerObj.displayDisabledFlag = False

        questionObj.questionAnswerObjList.append(questionAnswerObj)

    parentQuestions = Question.objects.exclude(id = question.id)

    ontologies = Ontology.objects.all()

    parentQuestionAnswers = QuestionAnswer.objects.all()

    return render_to_response("smellSurvey/editQuestion.html", {

        "questionObj" : questionObj,

        "parentQuestions" : parentQuestions,

        "parentQuestionAnswers" : parentQuestionAnswers,

        "ontologies" : ontologies,

    },  RequestContext(request))

@login_required
def deleteQuestion(request):

    questionId = request.POST.get("questionId",0 )

    question = Question.objects.get(pk = questionId)

    questionnaire = question.section.questionnaire

    question.delete()

    questionnaireObj = QuestionnaireObj()

    questionnaireObj.questionnaire = questionnaire

    sections = Section.objects.filter(questionnaire = questionnaire)

    for section in sections:

        sectionObj = SectionObj()

        sectionObj.section = section

        print ( " adding section " + str(section.name) )

        questions = Question.objects.filter( section = section )

        for question in questions:

            questionObj = QuestionObj()

            questionObj.question = question

            for questionAnswer in question.answers.all():

                questionAnswerObj = QuestionAnswerObj()

                questionAnswerObj.questionAnswer = questionAnswer

                questionObj.questionAnswerObjList.append(questionAnswerObj)

            sectionObj.questionObjList.append(questionObj)

        questionnaireObj.sectionObjList.append(sectionObj)

    return render_to_response("smellSurvey/displayQuestionnaire.html", {

        "questionnaireObj" : questionnaireObj,

    },  RequestContext(request))

@login_required
def deleteQuestionAnswer(request):

    questionAnswerId = request.POST.get("questionAnswerId",0 )

    questionAnswer = QuestionAnswer.objects.get(pk = questionAnswerId)

    questionId = request.POST.get("questionId",0 )

    question = Question.objects.get(pk = questionId)

    question.answers.remove(questionAnswer)

    question.save()

    questionObj = QuestionObj()

    questionObj.question = question

    for questionAnswer in question.answers.all():

        questionAnswerObj = QuestionAnswerObj()

        questionAnswerObj.questionAnswer = questionAnswer

        #print ( " type = " + str(questionAnswer.questionAnswerType.name) )

        if questionAnswer.questionAnswerType.name != "Boolean" :

            #print ( " ***** in if " )

            questionAnswerObj.displayDisabledFlag = False

        questionObj.questionAnswerObjList.append(questionAnswerObj)

    parentQuestions = Question.objects.exclude(id = question.id)

    ontologies = Ontology.objects.all()

    parentQuestionAnswers = QuestionAnswer.objects.all()

    return render_to_response("smellSurvey/editQuestion.html", {

        "questionObj" : questionObj,

        "parentQuestions" : parentQuestions,

        "parentQuestionAnswers" : parentQuestionAnswers,

        "ontologies" : ontologies,

    },  RequestContext(request))

@login_required
def deleteQuestionnaire(request):

    questionnaireId = request.POST.get("questionnaireId",0 )

    questionnaire = Questionnaire.objects.get(pk = questionnaireId)

    sections = Section.objects.filter(questionnaire = questionnaire)

    for section in sections:

        questions = Question.objects.filter( section = section)

        for question in questions:

            question.delete()

    questionnaire.delete()

    questionnaires = Questionnaire.objects.all()

    return render_to_response("smellSurvey/listQuestionnaires.html", {

        "questionnaires" : questionnaires,

    },  RequestContext(request))

@login_required
def submitEditQuestion(request):

    questionId = request.POST.get("questionId",0 )

    questionText = request.POST.get("questionText",0 )

    parentQuestionId = request.POST.get("parentQuestionId",0 )

    parentQuestionAnswerId = request.POST.get("parentQuestionAnswerId",0 )

    ontologyId = request.POST.get("ontologyId",0 )

    question = Question.objects.get(pk = questionId)

    if parentQuestionId != 0 :

        parentQuestion = Question.objects.get(pk = parentQuestionId)

        question.parent = parentQuestion

    if parentQuestionAnswerId != 0 :

        parentAnswer = QuestionAnswer.objects.get(pk = parentQuestionAnswerId)

        question.parentAnswer = parentAnswer

    ontology = Ontology.objects.get(pk = ontologyId)

    if ontologyId != 0 :

        ontology = Ontology.objects.get(pk = ontologyId)

        question.ontology = ontology

    question.text = questionText

    question.save()

    for questionAnswer in question.answers.all():

        questionAnswerText = request.POST.get("questionAnswer-" + str(questionAnswer.id),"")

        if questionAnswerText!= "":

            questionAnswer.text = questionAnswerText

            questionAnswer.save()

        questionAnswerOntologyId = request.POST.get("questionAnswerOntologyId-" + str(questionAnswer.id),0)

        if questionAnswerOntologyId!= 0:

            questionAnswerOntology = Ontology.objects.get( pk = questionAnswerOntologyId)

            questionAnswer.answerOntology = questionAnswerOntology

            questionAnswer.save()

    questionnaire = question.section.questionnaire

    questionnaireObj = QuestionnaireObj()

    questionnaireObj.questionnaire = questionnaire

    sections = Section.objects.filter(questionnaire = questionnaire)

    for section in sections:

        sectionObj = SectionObj()

        sectionObj.section = section

        print ( " adding section " + str(section.name) )

        questions = Question.objects.filter( section = section )

        for question in questions:

            questionObj = QuestionObj()

            questionObj.question = question

            for questionAnswer in question.answers.all():

                questionAnswerObj = QuestionAnswerObj()

                questionAnswerObj.questionAnswer = questionAnswer

                questionObj.questionAnswerObjList.append(questionAnswerObj)

            sectionObj.questionObjList.append(questionObj)

        questionnaireObj.sectionObjList.append(sectionObj)

    return render_to_response("smellSurvey/displayQuestionnaire.html", {

        "questionnaireObj" : questionnaireObj,

        "questionObj" : questionObj,

    },  RequestContext(request))

@login_required
def addRole(request):

    selectedMenu = "UserManagement"

    return render_to_response('smellSurvey/addRole.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def addSite(request):

    selectedMenu = "UserManagement"
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass    

    return render_to_response('smellSurvey/addSite.html', {

        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,
        'user':request.user,

    },  RequestContext(request))

@login_required
def addStudy(request):

    selectedMenu = "UserManagement"

    questionnaires = Questionnaire.objects.all()
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass      

    return render_to_response('smellSurvey/addStudy.html', {

        'selectedMenu': selectedMenu,
        'questionnaires': questionnaires,
        'user':request.user,
        'surveyUser':surveyUser,        

    },  RequestContext(request))

@login_required
def addTester(request):

    selectedMenu = "UserManagement"
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass      

    return render_to_response('smellSurvey/addTester.html', {

        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,           

    },  RequestContext(request))

@login_required
def addSuperUser(request):

    selectedMenu = "UserManagement"
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass      

    return render_to_response('smellSurvey/addSuperUser.html', {

        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,           

    },  RequestContext(request))

@login_required
def addAdministrator(request):

    selectedMenu = "UserManagement"
    
    surveyUser = ''

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

    except:

        pass      

    try:

        sites = Site.objects.all()
        studies = Study.objects.all()
        roles = Role.objects.all()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/addAdministrator.html', {

        'selectedMenu': selectedMenu,
        'sites': sites,
        'studies': studies,
        'roles': roles,
        'surveyUser':surveyUser,           

    },  RequestContext(request))

@login_required
def addPatient(request):

    selectedMenu = "UserManagement"

    try:
        
        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass 

        studies = Study.objects.all()

        sites = Site.objects.all()

        administrators = Administrator.objects.all()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/addPatient.html', {

        'selectedMenu': selectedMenu,
        'studies': studies,
        'sites': sites,
        'administrators': administrators,
        'user':request.user,
        'surveyUser':surveyUser,           

    },  RequestContext(request))

@login_required
def addQuestion(request):

    selectedMenu = "Question"

    try:

        questionnaireId = request.POST.get("questionnaireId","0")

        questionnaire = Questionnaire.objects.get ( pk = questionnaireId )

        ontologies = Ontology.objects.all()
        sections = Section.objects.filter(questionnaire = questionnaire)
        parentQuestions = Question.objects.all()
        parentQuestionAnswers = QuestionAnswer.objects.all()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/addQuestion.html', {

        'selectedMenu': selectedMenu,
        'sections' : sections,
        'ontologies' : ontologies,
        'parentQuestions' : parentQuestions,
        'parentQuestionAnswers' : parentQuestionAnswers,
        'questionnaire' : questionnaire,
        'user':request.user

    },  RequestContext(request))

@login_required
def addQuestionAnswer(request):

    selectedMenu = "QuestionAnswer"

    try:

        ontologies = Ontology.objects.all()
        questionAnswerTypes = QuestionAnswerType.objects.all()

        questionId = request.POST.get("questionId",0 )

        question = Question.objects.get(pk = questionId)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/addQuestionAnswer.html', {

        'selectedMenu': selectedMenu,
        'ontologies' : ontologies,
        'questionAnswerTypes' : questionAnswerTypes,
        'question' : question,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddSite(request):

    selectedMenu = "SiteList"

    try:

        siteName = request.POST.get('siteName', "0")

        siteDescription = request.POST.get('siteDescription', "0")

        sites = Site.objects.filter(name = siteName)

        if len(sites) == 0:

            site = Site(name = siteName, description = siteDescription)

            site.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddSite.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

        },  RequestContext(request))

@login_required
def submitAddRole(request):

    selectedMenu = "RoleList"

    try:

        roleName = request.POST.get('roleName', "0")

        roleDescription = request.POST.get('roleDescription', "0")

        roleLevel = request.POST.get('roleLevel', "0")

        #print ("roleLevel = " + str(roleLevel))

        isSuperUserFlag = False
        isAdministratorFlag = False
        isPatientFlag = False
        isTesterFlag = False

        if roleLevel == "1":
            isSuperUserFlag = True

        elif roleLevel == "2":
            isAdministratorFlag = True

        elif roleLevel == "3":
            isPatientFlag = True

        elif roleLevel == "4":
            isTesterFlag = True

        roles = Role.objects.filter(name = roleName)

        if len(roles) == 0:

            role = Role(name = roleName, description = roleDescription, isSuperUser = isSuperUserFlag, isAdministrator = isAdministratorFlag, isPatient = isPatientFlag, isTester = isTesterFlag )

            role.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddRole.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddStudy(request):

    selectedMenu = "StudyList"

    try:

        studyName = request.POST.get('studyName', "0")

        studyDescription = request.POST.get('studyDescription', "0")

        studies = Study.objects.filter(name = studyName)

        if len(studies) == 0:

            study = Study(name = studyName, description = studyDescription)

            questionnaireId = request.POST.get('questionnaireId', 0)

            questionnaire = Questionnaire.objects.get ( pk = questionnaireId )

            study.questionnaire = questionnaire

            study.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddStudy.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddTester(request):

    selectedMenu = "StudyList"

    try:

        #userId = request.POST.get('userId', "0")

        testerName = request.POST.get('testerName', "0")
        testerEmail = request.POST.get('testerEmail', "0")
        testerPassword = request.POST.get('testerPassword', "0")

        users = User.objects.filter(username = testerName)

        messages = []

        if len(users) > 0:

            messages.append ("Tester already exists.")

            roles = Role.objects.all()

            return render_to_response('smellSurvey/addTester.html', {

                'selectedMenu': selectedMenu,

                'roles': roles,
                'messages':messages,

            },  RequestContext(request))

        user = User.objects.create_user(username=testerName,
                                         email= testerEmail,
                                         password=testerPassword)

        role = Role.objects.filter(name = TESTER_ROLE_NAME)[0]

        tester = SurveyUser(user = user, role = role)

        tester.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddTester.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddSuperUser(request):

    selectedMenu = "StudyList"

    try:

        #userId = request.POST.get('userId', "0")

        superUserName = request.POST.get('superUserName', "0")
        superUserEmail = request.POST.get('superUserEmail', "0")
        superUserPassword = request.POST.get('superUserPassword', "0")

        users = User.objects.filter(username = superUserName)

        messages = []

        if len(users) > 0:

            messages.append ("Super User already exists.")
            sites = Site.objects.all()
            studies = Study.objects.all()
            roles = Role.objects.all()

            return render_to_response('smellSurvey/addsuperUser.html', {

                'selectedMenu': selectedMenu,
                'sites': sites,
                'studies': studies,
                'roles': roles,
                'messages':messages,

            },  RequestContext(request))

        user = User.objects.create_superuser(username=superUserName,
                                         email= superUserEmail,
                                         password=superUserPassword)

        role = Role.objects.filter(name = SUPER_USER_ROLE_NAME)[0]

        superUser = SurveyUser(user = user, role = role)

        superUser.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddSuperUser.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddAdministrator(request):

    selectedMenu = "StudyList"

    try:

        administratorName = request.POST.get('administratorName', "0")
        administratorEmail = request.POST.get('administratorEmail', "0")
        administratorPassword = request.POST.get('administratorPassword', "0")

        users = User.objects.filter ( username = administratorName)

        messages = []

        if len(users) > 0:

            messages.append ("Administrator already exists.")
            sites = Site.objects.all()
            studies = Study.objects.all()
            roles = Role.objects.all()

            return render_to_response('smellSurvey/addAdministrator.html', {

                'selectedMenu': selectedMenu,
                'sites': sites,
                'studies': studies,
                'roles': roles,
                'messages':messages,

            },  RequestContext(request))

        studyIds = request.POST.get('studyId', "0")
        siteIds = request.POST.get('siteId', "0")

        user = User.objects.create_user(username=administratorName,
                                         email= administratorEmail,
                                         password=administratorPassword)

        role = Role.objects.filter(name = ADMIN_ROLE_NAME)[0]

        administrator = Administrator(user = user, role = role)

        administrator.save()

        for siteId in siteIds:
            site = Site.objects.get ( pk = siteId )
            administrator.allowedSites.add ( site )

        for studyId in studyIds:
            study = Study.objects.get ( pk = studyId )
            administrator.allowedStudies.add ( study )

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddAdministrator.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddQuestion(request):

    selectedMenu = "UserManagement"

    try:

        questionText =  request.POST.get('questionText', "")

        questionId = request.POST.get('questionId', "0")

        sectionId = request.POST.get('sectionId', 0)
        section = Section.objects.get( pk = sectionId)

        ontologyId = request.POST.get('ontologyId', "0")
        ontology = Ontology.objects.get( pk = ontologyId)

        parentQuestionId = request.POST.get('parentQuestionId', "0")
        parentQuestion = Question.objects.get( pk = parentQuestionId)

        parentQuestionAnswerId = request.POST.get('parentQuestionAnswerId', "0")
        parentQuestionAnswer = QuestionAnswer.objects.get( pk = parentQuestionAnswerId)

        question = Question()

        question = Question(text = questionText, questionId = int(questionId), ontology = ontology, section = section, parent = parentQuestion, parentAnswer = parentQuestionAnswer)

        question.save()

        questionAnswerIdList =  request.POST.getlist('questionAnswerId')

        for questionAnswerId in questionAnswerIdList :

            questionAnswer = QuestionAnswer.objects.get(pk = questionAnswerId)

            question.answers.add(questionAnswer)

        questionnaireId = request.POST.get("questionnaireId",0)

        questionnaire = Questionnaire.objects.get(pk=questionnaireId)

        questionnaireObj = QuestionnaireObj()

        questionnaireObj.questionnaire = questionnaire

        sections = Section.objects.filter(questionnaire = questionnaire)

        for section in sections:

            sectionObj = SectionObj()

            sectionObj.section = section

            print ( " adding section " + str(section.name) )

            questions = Question.objects.filter( section = section )

            for question in questions:

                questionObj = QuestionObj()

                questionObj.question = question

                for questionAnswer in question.answers.all():

                    questionAnswerObj = QuestionAnswerObj()

                    questionAnswerObj.questionAnswer = questionAnswer

                    questionObj.questionAnswerObjList.append(questionAnswerObj)

                sectionObj.questionObjList.append(questionObj)

            questionnaireObj.sectionObjList.append(sectionObj)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/displayQuestionnaire.html', {

        'selectedMenu': selectedMenu,
        "questionnaireObj" : questionnaireObj,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitAddQuestionAnswer(request):

    selectedMenu = "UserManagement"

    try:

        questionAnswerText =  request.POST.get('questionAnswerText', "")

        questionAnswerId = request.POST.get('questionAnswerId', "0")

        questionAnswerTypeId = request.POST.get('questionAnswerTypeId', 0)

        questionAnswerType = QuestionAnswerType.objects.get ( pk = questionAnswerTypeId )

        ontologyId = request.POST.get('ontologyId', "0")
        answerOntology = Ontology.objects.get( pk = ontologyId)

        questionAnswer = QuestionAnswer(text = questionAnswerText, questionAnswerId = int(questionAnswerId) , questionAnswerType = questionAnswerType, answerOntology = answerOntology)

        questionAnswer.save()

        questionId = request.POST.get("questionId",0 )

        question = Question.objects.get(pk = questionId)

        question.answers.add(questionAnswer)

        questionObj = QuestionObj()

        questionObj.question = question

        for questionAnswer in question.answers.all():

            questionAnswerObj = QuestionAnswerObj()

            questionAnswerObj.questionAnswer = questionAnswer

            #print ( " type = " + str(questionAnswer.questionAnswerType.name) )

            if questionAnswer.questionAnswerType.name != "Boolean" :

                #print ( " ***** in if " )

                questionAnswerObj.displayDisabledFlag = False

            questionObj.questionAnswerObjList.append(questionAnswerObj)

        parentQuestions = Question.objects.exclude(id = question.id)

        ontologies = Ontology.objects.all()

        parentQuestionAnswers = QuestionAnswer.objects.all()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editQuestion.html', {

        "questionObj" : questionObj,

        "parentQuestions" : parentQuestions,

        "parentQuestionAnswers" : parentQuestionAnswers,

        "ontologies" : ontologies,

    },  RequestContext(request))

@login_required
def submitDeletePatients(request):

    selectedMenu = "UserManagement"
    
    hostName = HOSTNAME

    try:

        selectedPatientIds =  request.POST.getlist('selectedPatientId')
        
        for selectedPatientId in selectedPatientIds:
            
            patient = Patient.objects.get( pk = selectedPatientId) 
            patient.isDeleted = True
            patient.save()

        patientsList = []
        
        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass        

        if surveyUser.role.isSuperUser:

            patientsList = Patient.objects.filter(isDeleted = False)
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user, isDeleted = False)[0] 
            
            patientsList = Patient.objects.filter(defaultAdministrator = administrator)   


    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listPatients.html', {

        'patientsList': patientsList,
        'selectedMenu': selectedMenu,
        'hostName':hostName,
        'user':request.user,
        'surveyUser':surveyUser,

    },  RequestContext(request))

@login_required
def submitAddPatient(request):

    selectedMenu = "StudyList"
    hostname = HOSTNAME

    try:

        patientName = request.POST.get('patientName', "")
        
        patientEmail = "patient@smellSurvey.org"
        patientPassword = ''.join(choice(ascii_uppercase) for i in range(16))  
        
        #patientEmail = request.POST.get('patientEmail', "")
        #patientPassword = request.POST.get('patientPassword', "")

        users = User.objects.filter ( username = patientName)

        messages = []

        if len(users) > 0:

            messages.append ("Link name already exists.")
            sites = Site.objects.all()
            studies = Study.objects.all()
            roles = Role.objects.all()

            return render_to_response('smellSurvey/addPatient.html', {

                'selectedMenu': selectedMenu,
                'sites': sites,
                'studies': studies,
                'roles': roles,
                'messages':messages,

            },  RequestContext(request))

        #studyIds = request.POST.getlist('studyId')

        defaultStudyId = request.POST.get('defaultStudyId', 0)

        defaultSiteId = request.POST.get('defaultSiteId', 0)

        defaultAdministratorId = request.POST.get('defaultAdministratorId', 0)

        if patientName == '' or defaultStudyId == 0 or defaultSiteId == 0 or defaultAdministratorId == 0 :

            messages.append ("Please fill in all fields.")
            sites = Site.objects.all()
            studies = Study.objects.all()
            roles = Role.objects.all()
        
            return render_to_response('smellSurvey/addPatient.html', {
        
                'selectedMenu': selectedMenu,
                'sites': sites,
                'studies': studies,
                'roles': roles,
                'messages':messages,
        
            },  RequestContext(request))
        
        defaultStudy = Study.objects.get ( pk = defaultStudyId )
        defaultSite = Site.objects.get ( pk = defaultSiteId )
        defaultAdministrator = Administrator.objects.get ( pk = defaultAdministratorId )        

        user = User.objects.create_user(username=patientName,
                                         email= patientEmail,
                                         password=patientPassword)

        role = Role.objects.filter(name = PATIENT_ROLE_NAME)[0]
        
        surveyLink = ''

        linkFound = True
        
        while linkFound:
    
            surveyLink = ''.join(choice(ascii_uppercase) for i in range(24))            

            patients = Patient.objects.filter (surveyLink  = surveyLink)
            
            if len( patients ) == 0:
                
                linkFound = False

        patient = Patient(user = user, role = role, defaultStudy = defaultStudy , defaultSite = defaultSite, defaultAdministrator = defaultAdministrator, surveyLink = surveyLink, isDeleted = False )

        patient.save()

        patient.studies.add(defaultStudy)

        #for studyId in studyIds:
            #study = Study.objects.get ( pk = studyId )
            #patient.studies.add ( study )

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmAddPatient.html', {

        'selectedMenu': selectedMenu,
        'patient': patient,
        'hostname':hostname,
        'user':request.user

    },  RequestContext(request))

@login_required
def listStudies(request):

    selectedMenu = "StudyList"
    
    studyList = []    
    
    try:

        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        studyList = Study.objects.all().order_by("name")

        if surveyUser.role.isSuperUser or surveyUser.role.isTester:

            studyList = Study.objects.all()
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user)[0] 
            
            studyList = administrator.allowedStudies.all()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/studyList.html', {

        'studyList': studyList,
        'selectedMenu': selectedMenu,
        'user':request.user,
        'surveyUser':surveyUser,

    },  RequestContext(request))

@login_required
def listAdministrations(request):

    selectedMenu = "AdministrationList"
    try:

        administrations = []
        hostName = HOSTNAME
        
        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass
        
        if surveyUser.role.isSuperUser:

            administrations = Administration.objects.all().order_by("-startTime")
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user)[0] 
            
            administrations = Administration.objects.filter(administrator = administrator).order_by("-startTime")        
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listAdministrations.html', {

        'administrations': administrations,
        'selectedMenu': selectedMenu,
        'user':request.user,
        'hostName':hostName,
        'surveyUser':surveyUser,        

    },  RequestContext(request))

@login_required
def listSites(request):

    selectedMenu = "SiteList"
    
    siteList = []
    try:

        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        if surveyUser.role.isSuperUser or surveyUser.role.isTester:

            siteList = Site.objects.all().order_by("name")
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user)[0] 
            
            siteList = administrator.allowedSites.all()

        #siteList = Site.objects.all().order_by("name")

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/siteList.html', {

        'siteList': siteList,
        'selectedMenu': selectedMenu,
        'user':request.user,
        'surveyUser':surveyUser,

    },  RequestContext(request))

@login_required
def listUPINs(request):

    selectedMenu = "UPINList"
    try:

        upinListAll = UPIN.objects.all()
        
        upinList = []
        surveyUser = ''
        
        upinObjList = []

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass
        
        if surveyUser.role.isAdministrator:
            
            for upin in upinListAll:
                
                if upin.patient.defaultAdministrator.user.id == surveyUser.id:
                    
                    upinObj = UPINObj()
                    upinObj.upin = upin
                    
                    administrations = Administration.objects.filter (upin = upin)
                    if len(administrations) > 0:
                        
                        upinObj.administration = administration
                    
                    upinObjList.append ( upinObj ) 
                    
            #else:
                
                #upinList = upinListAll

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listUPINs.html', {

        'upinObjList': upinObjList,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def listRoles(request):

    selectedMenu = "RoleList"
    try:
        
        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass        

        rolesList = Role.objects.all().order_by("name")

    except:

        traceback.print_exc(file=sys.stdout)
        
    #messages.error(request, 'Somethig horribly wrong happened!')
    #raise Http404("An error occured.")       

    return render_to_response('smellSurvey/listRoles.html', {

        'rolesList': rolesList,
        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def listAdministrators(request):

    selectedMenu = "UserManagement"
    try:

        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass
        
        administratorObjList = []        
        
        if surveyUser.role.isSuperUser or surveyUser.role.isTester:
        
            administrators = Administrator.objects.all()
    
            for administrator in administrators :
    
                administratorObj = AdministratorObj()
    
                administratorObj.administrator = administrator
    
                administratorObjList.append ( administratorObj )
    
        elif surveyUser.role.isAdministrator:  
            
            administratorObj = AdministratorObj()

            administratorObj.administrator = administrator 

            administratorObjList.append ( administratorObj )

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listAdministrators.html', {

        'administratorObjList': administratorObjList,
        'selectedMenu': selectedMenu,
        'user':request.user,
        'surveyUser': surveyUser,

    },  RequestContext(request))

@login_required
def listTesters(request):

    selectedMenu = "UserManagement"
    try:

        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        testerRole = Role.objects.filter( name = TESTER_ROLE_NAME ) [0]

        testers = SurveyUser.objects.filter(role = testerRole)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listTesters.html', {

        'testers': testers,
        'surveyUser':surveyUser,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def listSuperUsers(request):

    selectedMenu = "UserManagement"
    try:
        
        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass        

        superUserRole = Role.objects.filter( name = SUPER_USER_ROLE_NAME ) [0]

        superUsers = SurveyUser.objects.filter(role = superUserRole)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listSuperUsers.html', {

        'superUsers': superUsers,
        'surveyUser':surveyUser,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def listPatients(request):

    selectedMenu = "PatientsList"
    hostname = HOSTNAME
    try:

        patientsList = []
        
        surveyUser = ''
        
        administrator = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass        

        if surveyUser.role.isSuperUser:

            patientsList = Patient.objects.filter(isDeleted = False)
            
        elif surveyUser.role.isAdministrator:
            
            administrator = Administrator.objects.filter( user = surveyUser.user, isDeleted = False)[0] 
            
            patientsList = Patient.objects.filter(defaultAdministrator = administrator)            
        
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/listPatients.html', {

        'patientsList': patientsList,
        'selectedMenu': selectedMenu,
        'hostname':hostname,
        'user':request.user,
        'surveyUser':surveyUser,

    },  RequestContext(request))

@login_required
def displayAdministratorDetailList(request):

    selectedMenu = "UserManagement"

    upinObjList = []
    Administrator = ''

    try:

        batInstrument = Instrument.objects.filter ( title = ISTH_BAT_INSTRUMENT)
        AdministratorId = request.POST.get('AdministratorId', "0")

        Administrator = Administrator.objects.get(pk = AdministratorId)

        upinObjList = []

        administrations = Administration.objects.filter ( Administrator = Administrator , instrument = batInstrument)

        fetchQuestionAnswerFlag = False

        fetchContextsFlag = False

        for administration in administrations:

            upinObj = UPINObj()

            upin = administration.upin

            upinObj.upin = upin

            upinObj.administration = administration

            #print " upin = " + str (upin.id)

            instrumentObj = calcScore(upin.id, fetchQuestionAnswerFlag, fetchContextsFlag)

            upinObj.instrumentObj = instrumentObj

            upinObj.score = sum( [ a.sectionScore for a in instrumentObj.sectionObjList ] )

            upinObjList.append ( upinObj )

        upinObjList.sort(key=lambda x: x.upin.id)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/AdministratorDetail.html', {

        'upinObjList': upinObjList,
        'Administrator': Administrator,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def editStudy(request):

    selectedMenu = "StudyList"

    studyObj = StudyObj()

    try:

        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass  

        studyId = request.POST.get('studyId', "0")

        study = Study.objects.get ( pk = studyId )

        studyObj.study = study

        questionnaires = Questionnaire.objects.all()

        #print " before "

        for questionnaire in questionnaires:

            #print " in adding " + str(questionnaire)

            questionnaireObj = QuestionnaireObj()

            questionnaireObj.questionnaire = questionnaire

            if questionnaire.id == study.questionnaire.id:

                questionnaireObj.selectedFlag = True

            studyObj.questionnaireObjList.append (questionnaireObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editStudy.html', {

        'studyObj': studyObj,
        'surveyUser': surveyUser,        
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def editPatient(request):

    selectedMenu = "patientList"

    patientObj = PatientObj()
    hostname = HOSTNAME

    try:
        
        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass       

        patientId = request.POST.get('patientId', "0")

        patient = Patient.objects.get ( pk = patientId )

        patientObj.patient = patient

        print ( " default admin = " + str ( patientObj.patient.defaultAdministrator.id  ))

        studies = Study.objects.all()

        sites = Site.objects.all()

        administrators = Administrator.objects.all()

        #print " before "

        for study in studies:

            #print " in adding " + str(study)

            studyObj = StudyObj()

            studyObj.study = study

            if study in patient.studies.all():

                studyObj.selectedFlag = True

            patientObj.studyObjList.append (studyObj)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editPatient.html', {

        'patientObj': patientObj,
        'selectedMenu': selectedMenu,
        'studies':studies,
        'sites':sites,
        'administrators':administrators,
        'surveyUser':surveyUser,
        'hostname':hostname,
        'user':request.user

    },  RequestContext(request))

@login_required
def editRole(request):

    selectedMenu = "RoleList"

    try:
        
        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass 

        roleId = request.POST.get('RoleId', "0")

        role = Role.objects.get ( pk = roleId )

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editRole.html', {

        'Role': Role,
        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def editSite(request):

    selectedMenu = "SiteList"

    try:

        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass 

        siteId = request.POST.get('siteId', "0")

        site = Site.objects.get ( pk = siteId )

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editSite.html', {

        'site': site,
        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def editAdministrator(request):

    selectedMenu = "UserManagement"

    administratorObj = AdministratorObj()
    try:
        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass         
        
        administratorId = request.POST.get('administratorId', "0")

        administrator = Administrator.objects.get ( pk = administratorId)

        administratorObj.administrator = administrator

        #roleId = Administrator.role.id

        allowedSites = administrator.allowedSites.all()
        allowedSiteIds = [x.id for x in allowedSites]

        allowedStudies = administrator.allowedStudies.all()
        allowedStudyIds = [x.id for x in allowedStudies]

        #roles = Role.objects.all()

        #for role in roles:
            #roleObj = UserRoleObj()
            #if role.id == roleId:
                #roleObj.isSelected = True
            #roleObj.role = role
            #AdministratorObj.roleObjList.append ( roleObj )

        sites = Site.objects.all()

        for site in sites:
            siteObj = SiteObj()
            if site.id in allowedSiteIds:
                siteObj.isSelected = True
            siteObj.site = site
            administratorObj.siteObjList.append ( siteObj )

        studies = Study.objects.all()

        for study in studies:
            studyObj = StudyObj()
            if study.id in allowedStudyIds:
                studyObj.isSelected = True
            studyObj.study = study
            administratorObj.studyObjList.append ( studyObj )

        #user = User.objects.filter ( username = Administrator.id )[0]

        #AdministratorObj.email = user.email

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editAdministrator.html', {

        'administratorObj': administratorObj,
        'selectedMenu': selectedMenu,
        'surveyUser':surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def editTester(request):

    selectedMenu = "UserManagement"

    try:

        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass 

        testerId = request.POST.get('testerId', "0")

        tester = SurveyUser.objects.get ( pk = testerId)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editTester.html', {

        'tester': tester,
        'surveyUser':surveyUser,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def editSuperUser(request):

    selectedMenu = "UserManagement"

    try:
        
        surveyUser = ''
    
        try:
    
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
    
        except:
    
            pass         

        superUserId = request.POST.get('superUserId', "0")

        superUser = SurveyUser.objects.get ( pk = superUserId)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/editSuperUser.html', {

        'superUser': superUser,
        'surveyUser':surveyUser,
        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitEditStudy(request):

    selectedMenu = "StudyList"

    try:

        studyId = request.POST.get('studyId', "0")

        studyName = request.POST.get('studyName', "0")

        studyDescription = request.POST.get('studyDescription', "0")

        study = Study.objects.get ( pk = studyId)

        study.name = studyName
        study.description = studyDescription

        questionnaireId = request.POST.get('questionnaireId', 0)

        questionnaire = Questionnaire.objects.get ( pk = questionnaireId )

        study.questionnaire = questionnaire
        study.save()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditStudy.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitEditPatient(request):

    selectedMenu = "PatientList"
    
    hostname = HOSTNAME

    try:

        patientId = request.POST.get('patientId', "0")

        patientName = request.POST.get('patientName', "0")

        patient = Patient.objects.get ( pk = patientId)

        patient.name = patientName

        studyIds = request.POST.getlist('studyId')

        patientName = request.POST.get('patientName', "")
        patientEmail = request.POST.get('patientEmail', "")
        patientPassword= request.POST.get('patientPassword', "")

        patient.user.username = patientName
        patient.user.email = patientEmail
        patient.user.password = patientPassword

        patient.save()

        prevstudies = patient.studies.all()
        prevstudyIds = [x.id for x in prevstudies]

        for prevstudyId in prevstudyIds:
            study = Study.objects.get ( pk = prevstudyId )
            patient.studies.remove ( study )

        for studyId in studyIds:
            study = Study.objects.get ( pk = int(studyId) )
            patient.studies.add ( study )

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditPatient.html', {

        'selectedMenu': selectedMenu,
        'hostname':hostname,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitEditSite(request):

    selectedMenu = "SiteList"

    try:

        siteId = request.POST.get('siteId', "0")

        siteName = request.POST.get('siteName', "0")

        siteDescription = request.POST.get('siteDescription', "0")

        site = Site.objects.get ( pk = siteId)

        site.name = siteName
        site.description = siteDescription

        site.save()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditSite.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))


@login_required
def submitEditRole(request):

    selectedMenu = "RoleList"

    try:

        roleId = request.POST.get('roleId', "0")

        roleName = request.POST.get('roleName', "0")

        roleDescription = request.POST.get('roleDescription', "0")

        isSuperUser = request.POST.get('isSuperUser', "0")
        isAdministrator = request.POST.get('isAdministrator', "0")
        isPatient = request.POST.get('isPatient', "0")

        role = Role.objects.get ( pk = RoleId)

        role.name = roleName
        role.description = roleDescription

        role.isSuperUser = isSuperUser
        role.isAdministrator = isAdministrator
        role.isPatient = isPatient

        role.save()

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditRole.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

def submitEditTester(request):

    selectedMenu = "AdministratorList"

    try:

        testerId = request.POST.get('testerId', "0")
        tester = SurveyUser.objects.get ( pk = testerId )

        print ("  ** testerId ** " + str(testerId) )

        #testerName = request.POST.get('testerName', "")
        testerEmail = request.POST.get('testerEmail', "")
        testerPassword= request.POST.get('testerPassword', "")

        #tester.user.username = testerName
        tester.user.email = testerEmail
        tester.user.password = testerPassword

        tester.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEdittester.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitEditSuperUser(request):

    selectedMenu = "AdministratorList"

    try:

        superUserId = request.POST.get('superUserId', "0")
        superUser = SurveyUser.objects.get ( pk = superUserId )

        print ("  ** superUserId ** " + str(superUserId) )

        superUserName = request.POST.get('superUserName', "")
        superUserEmail = request.POST.get('superUserEmail', "")
        superUserPassword= request.POST.get('superUserPassword', "")

        superUser.user.username = superUserName
        superUser.user.email = superUserEmail
        superUser.user.password = superUserPassword

        superUser.save()

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditSuperUser.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitEditAdministrator(request):

    selectedMenu = "AdministratorList"

    try:

        administratorId = request.POST.get('administratorId', "0")

        print ("  ** administratorId ** " + str(administratorId) )

        siteIds = request.POST.getlist('siteId')
        studyIds = request.POST.getlist('studyId')

        administrator = Administrator.objects.get(pk = administratorId)

        administratorName = request.POST.get('administratorName', "")
        administratorEmail = request.POST.get('administratorEmail', "")
        administratorPassword= request.POST.get('administratorPassword', "")

        administrator.user.username = administratorName
        administrator.user.email = administratorEmail
        administrator.user.password = administratorPassword

        administrator.save()

        prevstudies = administrator.allowedStudies.all()
        prevstudyIds = [x.id for x in prevstudies]

        prevsites = administrator.allowedSites.all()
        prevsiteIds = [x.id for x in prevsites]

        prevstudys = administrator.allowedStudies.all()
        prevstudyIds = [x.id for x in prevstudys]

        for prevstudyId in prevstudyIds:
            study = Study.objects.get ( pk = prevstudyId )
            administrator.allowedStudies.remove ( study )

        for studyId in studyIds:
            study = Study.objects.get ( pk = int(studyId) )
            administrator.allowedStudies.add ( study )

        for prevsiteId in prevsiteIds:
            site = Site.objects.get ( pk = prevsiteId )
            administrator.allowedSites.remove ( site )

        for siteId in siteIds:
            site = Site.objects.get ( pk = int(siteId) )
            administrator.allowedSites.add ( site )

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmEditAdministrator.html', {

        'selectedMenu': selectedMenu,
        'user':request.user

    },  RequestContext(request))

@login_required
def selectSiteStudy(request):

    selectedMenu = "AdministratorList"

    administrations = []

    try:

        surveyUser = SurveyUser.objects.filter ( user = request.user)[0]

        print ( " survey user = " + str(surveyUser.role) )

        if surveyUser.role.isPatient:

            patient = Patient.objects.filter(user = request.user)[0]

            study = ''

            selectedStudyId = request.GET.get('studyId', 0)

            if selectedStudyId != 0:

                study = Study.objects.get(pk = selectedStudyId)

            else:

                study = patient.defaultStudy

            site = patient.defaultSite

            study = patient.defaultStudy

            administrator = patient.defaultAdministrator

            questionnaire = study.questionnaire

            upinId = request.POST.get('upinId', 0)

            print ( " upind == " + str(upinId))

            upins = UPIN.objects.filter(patient = patient, study = study)

            administrations = Administration.objects.filter( upin__in = upins)

            print ( " administrations = " + str(administrations))

            return render_to_response('smellSurvey/administerQuestionnaireWelcome.html', {

                #'surveyUser' : surveyUser,
                'site' : site,
                'study' : study,
                'patient' : patient,
                'questionnaire' : questionnaire,
                'upinId' :upinId,
                'administrator' : administrator,
                'administrations': administrations,
                'surveyUser' : surveyUser,
                'user':request.user

            },  RequestContext(request))

        elif surveyUser.role.isAdministrator:

            administrator = Administrator.objects.filter ( user = surveyUser.user)[0]

            administrations = Administration.objects.filter( administrator = administrator)

            print (" *** administrator sites *** " + str(administrator.allowedSites.all))
            print (" *** administrator studies *** " + str(administrator.allowedStudies.all))

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/selectSiteStudy.html', {

        'selectedMenu': selectedMenu,
        'administrator' : administrator,
        'administrations':administrations,
        'surveyUser': surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def selectPatient(request):

    selectedMenu = "AdministratorList"

    try:

        surveyUser = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        questionnaire = study.questionnaire

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        studies = []
        studies.append(study)

        patients = Patient.objects.filter ( studies__in = studies)

        hostname = HOSTNAME
        
        print (str(patients))

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/selectPatient.html', {

        'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,

        'questionnaire': questionnaire,

        'administrator':administrator,
        'hostname' : hostname,
        'patients' : patients,
        'user':request.user,
        'surveyUser':surveyUser

    },  RequestContext(request))

@login_required
def administerQuestionnaire(request):
    
    laptopOrBrowserFlag = False

    try:
        
        prevQuestion = ''        

        laptopOrBrowserFlag = request.POST.get('laptopOrBrowser', "")
        
        if laptopOrBrowserFlag == "true":
            
            laptopOrBrowserFlag = True
            
        else:
            
            laptopOrBrowserFlag = False

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        surveyUser = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        prevQuestionId = request.POST.get('prevQuestionId', "0")

        print ( " ***** #### 1111 prev question id = " + str(prevQuestionId)  )
        
        #navigateSectionFlag = request.POST.get('navigateSectionFlag', "0")   
        #print ( " navigateSectionFlag = --- " + str(navigateSectionFlag))        
        
        prevQuestion = ''
        
        if prevQuestionId != "0" and prevQuestionId.strip() != "":
            prevQuestion = Question.objects.get ( pk = int(prevQuestionId))
            print ( " ***** #### prev question id = " + str(prevQuestionId) + " text = " + str(prevQuestion.text) )

        upinId = request.POST.get('upinId', 0)

        sectionId = request.POST.get('sectionId', "0")

        administrationId = request.POST.get('administrationId', 0)

        print ( " section id = " + str(sectionId) )

        #print ( " administrationId = " + str(administrationId) )

        sections = Section.objects.filter ( questionnaire = questionnaire ).order_by("sequence")

        section = ''

        if sectionId != "0" and sectionId != "":
            
            print ( " section id 222 = " + str(sectionId) )            

            section = Section.objects.get ( pk = int(sectionId))
            
            print ( " got section " + str(section))

        else:

            section = sections[0]
        
        if prevQuestionId != 0 and prevQuestion != '':
            
            question = prevQuestion

            if prevQuestion.parent:
            
                prevQuestion = prevQuestion.parent
                
            else: 
                
                prevQuestion = ''
            
        else:
     
            questions = Question.objects.filter(section = section)
    
            question = questions[0]    
            
            prevQuestion = question.parent

        upin = ''

        administration = ''

        if administrationId == 0 or administrationId == '':
            
            sessionId = request.session.session_key            

            upin = UPIN(upinId = upinId, patient = patient, study = study , sessionId = sessionId)

            upin.save()

            administration = Administration(upin = upin, questionnaire = questionnaire, site = site, administrator = administrator, startTime = datetime.datetime.now())

            administration.save()

        else:

            administration = Administration.objects.get ( pk = administrationId )
            upin = administration.upin

        questionObj = QuestionObj()

        questionObj.question = question

        for questionAnswer in question.answers.all().order_by("questionAnswerId"):

            questionAnswerObj = QuestionAnswerObj()

            questionAnswerObj.questionAnswer = questionAnswer

            questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)

            if len ( questionAnswerInstances ) > 0:

                questionAnswerInstance = questionAnswerInstances[0]

                questionAnswerObj.isAnswered = True
                questionAnswerObj.questionAnswerInstance = questionAnswerInstance

            questionAnswerChoiceList = QuestionAnswerChoice.objects.filter (questionAnswer = questionAnswer)
            questionAnswerObj.questionAnswerChoiceList = questionAnswerChoiceList
            
            #print ( " adding choices " + str(questionAnswerChoiceList) ) 

            questionAnswerTimeUnitList = QuestionAnswerTimeUnit.objects.filter (questionAnswer = questionAnswer)
            questionAnswerObj.questionAnswerTimeUnitList = questionAnswerTimeUnitList

            #print ( " adding time units " + str(questionAnswerTimeUnitList) ) 

            questionObj.questionAnswerObjList.append (questionAnswerObj)
            
        currentDate = datetime.datetime.today().strftime('%m/%d/%Y')
        
        print ( " finally section --- " + str(section))
        
        percentageComplete , percentageCompleteSection = getPercentageComplete(administration, section)
        
        showSectionPercentageFlag = True      
        #percentageCompleteSection = getPercentageComplete(administration, section)        
        print ( " percent complete = " + str(percentageComplete)  + " percent complete section = " + str(percentageCompleteSection)) 

    except:
        traceback.print_exc(file=sys.stdout)
        
    if laptopOrBrowserFlag:        

        return render_to_response('smellSurvey/administerQuestionnaire.html', {
    
            'site' : site,
            'study' : study,
            'patient' : patient,
            'questionnaire' : questionnaire,
    
            'sections' : sections,
    
            'section' : section,
    
            'upinId':upinId,
            'administrator' : administrator,
            'administration' : administration,
            'user':request.user,
            
            'percentageComplete': percentageComplete,
            'percentageCompleteSection': percentageCompleteSection,
            
            'showSectionPercentageFlag':showSectionPercentageFlag,        
            
            'questionObj': questionObj,
            'prevQuestion':prevQuestion,
            'surveyUser':surveyUser,
            
            'currentDate' : currentDate,
    
        },  RequestContext(request))
    
    else:
        
        return render_to_response('smellSurvey/administerQuestionnaire_laptop.html', {
    
            'site' : site,
            'study' : study,
            'patient' : patient,
            'questionnaire' : questionnaire,
    
            'sections' : sections,
    
            'section' : section,
    
            'upinId':upinId,
            'administrator' : administrator,
            'administration' : administration,
            'user':request.user,
            
            'percentageComplete': percentageComplete,
            'percentageCompleteSection': percentageCompleteSection,
            
            'showSectionPercentageFlag':showSectionPercentageFlag,        
            
            'questionObj': questionObj,
            'prevQuestion':prevQuestion,
            'surveyUser':surveyUser,
            
            'currentDate' : currentDate,
    
        },  RequestContext(request))        

#def getPathToQuestion(question):
    #tmp_path =[]
    #path = []
    #tmp_depth = 0
    #depth=0
    #while not question.parent is None:
        #question = question.parent
        #depth +=1
        #tmp_path.append((depth,question))
    #for tmp_depth, question in tmp_path:
        #path.append(((range(0,(depth-tmp_depth+1))),question))
    #path.reverse()
    #return path

def checkIfParentInPath(parentFlag, question, parentQuestion):

    try:

        #print ( " *** &&&&&&  in checkIfParentInPath = " + str(question.questionId) + "::" + str(question) + " parent = " + str(parentQuestion.questionId) + "::" + str(parentQuestion) + " parent flag = " + str(parentFlag) )

        if question.parent is None:

            return parentFlag

        if question.parent.questionId == parentQuestion.questionId:

            parentFlag = True

            return parentFlag

        else:

            question = question.parent

            return checkIfParentInPath(parentFlag, question, parentQuestion)

    except:

        traceback.print_exc(file=sys.stdout)

    return parentFlag

def navigateSection(question, section, originalQuestion):

    try:

        questions = Question.objects.filter (questionId__gt = question.questionId, section = section).exclude(parent = question)

        print ( " @@@@@@@@@@ in navigate questionnaire for question = " + str(question.questionId) + "::" + str(question) + " num " + str(len(questions)))

        if len ( questions ) == 0:

            return ''

        nextQuestion = questions[0]

        parentFlag = False

        parentFlag = checkIfParentInPath(parentFlag, nextQuestion, originalQuestion)

        if not parentFlag:

            return nextQuestion

        else:

            return navigateSection(nextQuestion, section, originalQuestion)

    except:

        traceback.print_exc(file=sys.stdout)

    return nextQuestion

@login_required
def submitAdministerQuestionnaire(request):

    laptopOrBrowserFlag = False

    try:

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        laptopOrBrowserFlag = request.POST.get('laptopOrBrowser', "")
        
        if laptopOrBrowserFlag == "true":
            
            laptopOrBrowserFlag = True
            
        else:
            
            laptopOrBrowserFlag = False

        surveyUser = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        administrationId = request.POST.get('administrationId', 0)
        administration = Administration.objects.get ( pk = administrationId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        questionId = request.POST.get('questionId', 0)
        question = Question.objects.get (pk = questionId)
        
        print ( " question = --- " + str(question))

        #prevQuestionId = request.POST.get('prevQuestionId', 0)
        #prevQuestionFlag = request.POST.get('prevQuestionFlag', "")
        
        sectionId = request.POST.get('sectionId', "0")   

        sections = Section.objects.filter ( questionnaire = questionnaire).order_by("sequence")
        if sectionId != "0" and sectionId != "":        
            section = Section.objects.get ( pk = sectionId)
        else:
            section = sections[0]
        
        allSections = sections
        
        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''
        prevSection = ''        
 
        allSections = Section.objects.filter(questionnaire = questionnaire).order_by("sequence")

        upinId = request.POST.get('upinId', 0)

        #print (" ** section ** " + str(section) )

        questionAnswers = QuestionAnswer.objects.filter( question = question ).order_by("questionAnswerId")

        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''

        isQuestionAnswered = False

        questionAnswerId = 0

        isBooleanQuestionAnswer = False
        
        currentDate = datetime.datetime.today().strftime('%m/%d/%Y')  
        
        deletedOldResponses = False

        for questionAnswer in questionAnswers:

            questionAnswerTypeName = ''

            if questionAnswer.questionAnswerType:

                questionAnswerTypeName = questionAnswer.questionAnswerType.name

            #print ("  ######%%%%%%%%%%%% for question Answer  " + str( questionAnswer.text) + " type = " +  questionAnswerTypeName )

            if questionAnswerTypeName == "single choice" and questionAnswerId != 0:

                break

            questionAnswerId = 0

            if questionAnswerTypeName == "single choice":

                isBooleanQuestionAnswer = True

                questionAnswerId = request.POST.get('questionAnswer-' + str( question.id), 0 )

            else:

                questionAnswerId = request.POST.get('questionAnswer-' + str( questionAnswer.id), 0 )

            answerText = request.POST.get('questionAnswerText-' + str( questionAnswerId) , '')
            answerText2 = request.POST.get('questionAnswerText2-' + str( questionAnswerId) , '')
                 
            if questionAnswerId != 0:

                questionAnswer = QuestionAnswer.objects.get ( pk = questionAnswerId )

                # delete any existing question answer responses, in case people come back to this. Also delete all responses down this tree.
                
                #if questionAnswerTypeName == "multiple choice" and not deletedOldResponses:
                    
                if not deletedOldResponses:

                    deleteRelatedResponses( administration, question)
                    
                    deletedOldResponses = True

                saveResponseFlag = True

                if questionAnswerTypeName != "single choice" and questionAnswerTypeName != "multiple choice" and answerText == "":
                    
                    saveResponseFlag = False
                    
                if saveResponseFlag:

                    questionAnswerInstance = QuestionAnswerInstance(administration = administration, question = question, answer = questionAnswer, answerText = answerText, answerText2 = answerText2, timeStamp = datetime.datetime.now())

                    questionAnswerInstance.save()

                prevQuestionAnswer = questionAnswer

                isQuestionAnswered = True

        prevQuestion = question.parent
        prevSection = section

        completedFlag = False

        questionId = question.id

        sectionSequence = section.sequence

        hasChildQuestions = False

        # check if question and answer has a child question. Else, get the next question.

        if isQuestionAnswered and isBooleanQuestionAnswer:

            questionAnswer = QuestionAnswer.objects.get(pk = questionAnswerId)

            childQuestions = Question.objects.filter ( parent = question, parentAnswer = questionAnswer )

            if len ( childQuestions ) > 0 :

                hasChildQuestions = True
                
                prevQuestion = question
                #print (" ^^^^^^^^ found child question for question ::::: " + str(question.text))
                question = childQuestions [0]
 
                questionAnswers = QuestionAnswer.objects.filter(question = question).order_by("questionAnswerId")

        # if question is not answered or it was answered but there were no child questions
        if not hasChildQuestions:

            nextQuestionInSection = navigateSection (question, question.section, question)
            
            if nextQuestionInSection != '':
                
                prevQuestion = question               
                
                question = nextQuestionInSection
                
                questionAnswers = QuestionAnswer.objects.filter(question = nextQuestionInSection).order_by("questionAnswerId")
            
            else:

                sections = Section.objects.filter (sequence__gt = sectionSequence).order_by("sequence")
                
                if len(sections) > 0:
                    
                    section = sections[0]

                    questions = Question.objects.filter(section = section)
                    prevQuestion = question                   

                    question = questions[0]

                    questionAnswers = QuestionAnswer.objects.filter(question = question).order_by("questionAnswerId")

                else:# if there are no more sections

                    completedFlag = True

        if completedFlag:
            
            print ( " ####### in  !!!! review " ) 
            
            return reviewAdministration(request, completedFlag, surveyUser)

        questionObj = QuestionObj()

        questionObj.question = question

        for questionAnswer in questionAnswers:
            
            print ( " for answer " + str(questionAnswer.id) + " text = " + str(questionAnswer.text))

            questionAnswerObj = QuestionAnswerObj()

            questionAnswerObj.questionAnswer = questionAnswer

            questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)

            if len ( questionAnswerInstances ) > 0:

                questionAnswerInstance = questionAnswerInstances[0]

                questionAnswerObj.isAnswered = True
                questionAnswerObj.questionAnswerInstance = questionAnswerInstance
                
            questionAnswerChoiceList = QuestionAnswerChoice.objects.filter (questionAnswer = questionAnswer)
            questionAnswerObj.questionAnswerChoiceList = questionAnswerChoiceList
            
            #print ( " adding choices " + str(questionAnswerChoiceList) ) 

            questionAnswerTimeUnitList = QuestionAnswerTimeUnit.objects.filter (questionAnswer = questionAnswer)
            questionAnswerObj.questionAnswerTimeUnitList = questionAnswerTimeUnitList

            #print ( " adding time units " + str(questionAnswerTimeUnitList) )                  

            questionObj.questionAnswerObjList.append (questionAnswerObj)
            
        #percentageComplete = getPercentageComplete(administration)
        
        percentageComplete , percentageCompleteSection = getPercentageComplete(administration, section)
        
        showSectionPercentageFlag = True
        #percentageCompleteSection = getPercentageComplete(administration, section)        
        print ( " percent complete = " + str(percentageComplete)  + " percent complete section = " + str(percentageCompleteSection))         
        
        #print ( " percent complete = " + str(percentageComplete) ) 

    except:
        traceback.print_exc(file=sys.stdout)
        
    if laptopOrBrowserFlag:        

        return render_to_response('smellSurvey/administerQuestionnaire.html', {
    
            'site' : site,
            'study' : study,
            'sections' : allSections,
    
            'patient' : patient,
            'questionnaire' : questionnaire,
    
            'administration' : administration,
            'administrator' : administrator,
    
            'prevQuestion' : prevQuestion,
            'prevQuestionAnswer': prevQuestionAnswer,
            'prevQuestionAnswerText':prevQuestionAnswerText,
            'prevSection': prevSection,
    
            "questionObj" : questionObj,
            'section':section,
    
            'upinId':upinId,
            'user':request.user,
            
            'currentDate' : currentDate,
            
            'surveyUser' : surveyUser,  
            
            'percentageComplete':percentageComplete,
            'percentageCompleteSection':percentageCompleteSection,
            
            'showSectionPercentageFlag':showSectionPercentageFlag,        
    
        },  RequestContext(request))
    
    else:
        
        return render_to_response('smellSurvey/administerQuestionnaire_laptop.html', {
    
            'site' : site,
            'study' : study,
            'sections' : allSections,
    
            'patient' : patient,
            'questionnaire' : questionnaire,
    
            'administration' : administration,
            'administrator' : administrator,
    
            'prevQuestion' : prevQuestion,
            'prevQuestionAnswer': prevQuestionAnswer,
            'prevQuestionAnswerText':prevQuestionAnswerText,
            'prevSection': prevSection,
    
            "questionObj" : questionObj,
            'section':section,
    
            'upinId':upinId,
            'user':request.user,
            
            'currentDate' : currentDate,
            
            'surveyUser' : surveyUser,  
            
            'percentageComplete':percentageComplete,
            'percentageCompleteSection':percentageCompleteSection,
            
            'showSectionPercentageFlag':showSectionPercentageFlag,        
    
        },  RequestContext(request))     
            

def deleteRelatedResponses(administration , question ):
    
    print (" ****** IN DELETE ******* administration = " + str(administration) + " question = " + str(question)  )
    
    print ( " found answers " + str(QuestionAnswerInstance.objects.filter (administration = administration , question = question ) ) )
    
    QuestionAnswerInstance.objects.filter (administration = administration , question = question ).delete()
    
    childQuestions = Question.objects.filter (parent = question)
    
    for childQuestion in childQuestions:
    
        questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration , question = childQuestion )
    
        for questionAnswerInstance in questionAnswerInstances:
    
            deleteRelatedResponses(questionAnswerInstance.administration , questionAnswerInstance.question )

#def deleteRelatedResponses(administration , question , answer):
    
    #print (" ****** IN DELETE ******* administration = " + str(administration) + " question = " + str(question) + " answer = " + str(answer) )
    
    #QuestionAnswerInstance.objects.filter (administration = administration , question = question , answer = answer).delete()
    
    #parentQuestions = Question.objects.filter (parent = question, parentAnswer = answer)
    
    #for parentQuestion in parentQuestions:
    
        #questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration , question = parentQuestion )
    
        #for questionAnswerInstance in questionAnswerInstances:
    
            #deleteRelatedResponses(questionAnswerInstance.administration , questionAnswerInstance.question , questionAnswerInstance.answer)

@login_required
def completeAdministration(request):

    try:

        administrationId = request.POST.get('administrationId', 0)
        administration = Administration.objects.get ( pk = administrationId)

        administration.stopTime = datetime.datetime.now()
        administration.save()

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            print (" survey user not found" )
            pass 
        
        logout(request)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/confirmQuestionnaireCompletion.html', {

        'surveyUser':surveyUser,
        'user':request.user,

    },  RequestContext(request))

def fetchQuestionAnswerText(request, questionAnswerId):

    try:

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

        if upinId == 0:

            notFound = True

            while notFound:

                upinId = randint(100001, 999999)

                upinCount = UPIN.objects.filter(upinId = newUPINID).count()

                if upinCount == 0:

                    notFound = False

        print ( " upin == " + str(upinId))

    except:
        traceback.print_exc(file=sys.stdout)

    return answerText, answerText2

@login_required
def administerQuestionnaireWelcome(request):

    try:
        
        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            print (" survey user not found" )
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

        if upinId == 0:

            notFound = True

            while notFound:

                upinId = randint(100001, 999999)

                upinCount = UPIN.objects.filter(upinId = newUPINID).count()

                if upinCount == 0:

                    notFound = False

        print ( " upin == " + str(upinId))

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireWelcome.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser':surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def administerQuestionnaireBackground(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            print (" survey user not found" )
            pass  

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireBackground.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser' : surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def administerQuestionnaireFirst(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireFirst.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser': surveyUser,
        'user':request.user

    },  RequestContext(request))
@login_required
def administerQuestionnaireSecond(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireSecond.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser' : surveyUser,
        'user':request.user

    },  RequestContext(request))
@login_required
def administerQuestionnaireThird(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireThird.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser': surveyUser,
        'user':request.user

    },  RequestContext(request))

#@login_required
#def administerQuestionnaireFourth(request):

    #try:

        #siteId = request.POST.get('siteId', 0)
        #site = Site.objects.get ( pk = siteId )

        #studyId = request.POST.get('studyId', 0)
        #study = Study.objects.get ( pk = studyId)

        #administratorId = request.POST.get('administratorId', 0)
        #administrator = Administrator.objects.get ( pk = administratorId)

        #patientId = request.POST.get('patientId', 0)
        #patient = Patient.objects.get ( pk = patientId)

        #questionnaireId = request.POST.get('questionnaireId', 0)
        #questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

    #except:
        #traceback.print_exc(file=sys.stdout)

    #return render_to_response('smellSurvey/administerQuestionnaireFourth.html', {

        ##'selectedMenu': selectedMenu,

        #'site' : site,
        #'study' : study,
        #'patient' : patient,
        #'questionnaire' : questionnaire,

        #'administrator' : administrator,

        #'user':request.user

    #},  RequestContext(request))

@login_required
def administerQuestionnaireLegal(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireLegal.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser' : surveyUser,
        'user':request.user

    },  RequestContext(request))
@login_required
def administerQuestionnaireConfirmStart(request):

    try:

        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass        

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)

    except:
        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaireConfirmStart.html', {

        #'selectedMenu': selectedMenu,

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,
        'upinId': upinId,
        'administrator' : administrator,
        'surveyUser' : surveyUser,
        'user':request.user

    },  RequestContext(request))

@login_required
def submitRestart(request):

    ''' Display Administration
    Input: Request
    Output AdministrationObj for display
    '''

    try:

        administrationId = request.POST.get("administrationId",0)

        administration = Administration.objects.get(pk=administrationId)

        QuestionAnswerInstance.objects.filter(administration = administration).delete()

        siteId = request.POST.get('siteId', 0)
        site = Site.objects.get ( pk = siteId )

        studyId = request.POST.get('studyId', 0)
        study = Study.objects.get ( pk = studyId)

        administratorId = request.POST.get('administratorId', 0)
        administrator = Administrator.objects.get ( pk = administratorId)

        patientId = request.POST.get('patientId', 0)
        patient = Patient.objects.get ( pk = patientId)

        questionnaireId = request.POST.get('questionnaireId', 0)
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId)

        upinId = request.POST.get('upinId', 0)
        upin = UPIN.objects.get ( pk = upinId)

        sectionId = request.POST.get('sectionId', 0)

        sections = Section.objects.filter ( questionnaire = questionnaire ).order_by("sequence")

        section = ''

        if sectionId != 0:

            section = Section.objects.get ( pk = sectionId)

        else:

            section = sections[0]

        administration = Administration(upin = upin, questionnaire = questionnaire, site = site, administrator = administrator, startTime = datetime.datetime.now())

        administration.save()

        questions = Question.objects.filter(section = section)

        question = questions[0]

        questionAnswers = QuestionAnswer.objects.filter(question = question)

    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response('smellSurvey/administerQuestionnaire.html', {

        'site' : site,
        'study' : study,
        'patient' : patient,
        'questionnaire' : questionnaire,

        'question' : question,
        'questionAnswers' : questionAnswers,
        'section' : section,

        'upinId':upinId,
        'administrator' : administrator,
        'administration' : administration,
        'user':request.user

    },  RequestContext(request))

@login_required
def reloadUPIN(request):

    ''' Display Administration
    Input: Request
    Output AdministrationObj for display
    '''

    try:
        
        surveyUser = ''

        try:

            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]

        except:

            pass        

        prevQuestion = ''
        prevQuestionAnswer = ''
        prevQuestionAnswerText =  ''
        prevSection = ''
        
        sessionFile = request.FILES['sessionFile']

        #if phenotypeFileName == '':

            #phenotypeFileName = request.FILES['datafilePath'].name

        messages = []

        sessionFileData = ''

        sessionFileLines = ''

        try:

            sessionFileData = sessionFile.read().decode()
    
            sessionFileLines = sessionFileData.split("\r")

        except:
            
            messages.append("Invalid Session File.")
            
            logout(request)

            return render_to_response("registration/landing.html", {
                "messages" : messages,
               # "upinId": upinId,

            }, RequestContext(request))
                                      
        for index, line in enumerate ( sessionFileLines ) :
            
            if index == 0:
                
                upinId = line.replace("\n","").strip()
                
            elif index == 1:
        
                sessionId = line.replace("\n","").strip()

        #upinId = request.POST.get('existingUPINID', 0)

        upins = UPIN.objects.filter ( upinId = upinId,sessionId = sessionId )

        upin = 0

        if len (upins) > 0:

            upin = upins[0]

        else:

            messages.append("Invalid Session File.")

            return render_to_response("smellSurvey/landing.html", {
                "messages" : messages,
                "upinId": upinId,

            }, RequestContext(request))

        #administrationId = request.POST.get('administrationId', 0)
        administration = Administration.objects.filter(upin = upin)[0]
        
        #startTime = administration.startTime
        
        #timeDelta = datetime.datetime.now(timezone.utc) - startTime
        
        #if timeDelta.seconds//3600 > MAX_HOURS_VALID_SESSION:
            
            #messages.append("Session file has expired. Please use a valid session file or complete a new survey.")

            #return render_to_response("smellSurvey/landing.html", {
                #"messages" : messages,
                #"upinId": upinId,

            #}, RequestContext(request))            
            

        administrator = administration.administrator
        
        percentageComplete = int(getPercentageCompleteTotal(administration))

        site = administration.site
        study = administration.upin.study

        patient = administration.upin.patient
        questionnaire = administration.questionnaire

        upinId = administration.upin.upinId

        questionId = request.POST.get('questionId', 0)

        previewFlag = False
        
        backToQuestionnaireFlag = True       

        question = ''

        questionAnswers = []

        section = Section.objects.all()[0]

        sectionId = section.id

        currentSection = 0

        if sectionId != 0:

            currentSection = Section.objects.get (pk = sectionId)

        if questionId != 0:
            question = Question.objects.get (pk = questionId)
            questionAnswers = QuestionAnswer.objects.filter( question = question )

            section = question.section

        print (" ** question ** " + str(question) )

        sections = Section.objects.filter(questionnaire = questionnaire).order_by("sequence")

        #upinId = request.POST.get('upinId', 0)

        #print (" ** section ** " + str(section) )

        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''

        isQuestionAnswered = False

        questionAnswerId = 0

        administrationObj = AdministrationObj()

        administrationObj.administration = administration

        questionnaire = administration.questionnaire

        sections = Section.objects.filter(questionnaire = questionnaire)

        for section in sections:

            sectionObj = SectionObj()

            sectionObj.section = section

            print ( " adding section " + str(section.name) )

            questions = Question.objects.filter( section = section )

            isSectionAnswered = False

            for question in questions:

                questionObj = QuestionObj()

                questionObj.question = question

                isAnswered = False

                for questionAnswer in question.answers.all():

                    questionAnswerObj = QuestionAnswerObj()

                    questionAnswerObj.questionAnswer = questionAnswer

                    questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)

                    if len ( questionAnswerInstances ) > 0:

                        questionAnswerInstance = questionAnswerInstances[0]

                        print (" &&&&  for question answer = " + str(questionAnswer) + " is answered ")

                        questionAnswerObj.isAnswered = True
                        questionAnswerObj.questionAnswerInstance = questionAnswerInstance

                    #if not questionAnswerObj.isAnswered and question.parentQuestion and question.parentAnswer != '':

                        #continue

                        questionObj.questionAnswerObjList.append(questionAnswerObj)

                        isAnswered = True

                        isSectionAnswered = True
                        
                if isAnswered:
        
                    sectionObj.questionObjList.append(questionObj)
                    
                else:
                    
                    if not question.parent:                         
                    
                        sectionObj.colorFlag = True
        
            administrationObj.sectionObjList.append(sectionObj)                        
                
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response("smellSurvey/displayAdministration.html", {
        "administrationObj" : administrationObj,
        "upinId": upinId,

        "site" : site,
        "study" : study,
        "sections" : sections,
        "patient" : patient,
        "questionnaire" : questionnaire,
        
        "surveyUser": surveyUser,
        
        "administration" : administration,
        "administrator" : administrator,

        'prevQuestion' : prevQuestion,
        'prevQuestionAnswer': prevQuestionAnswer,
        'prevQuestionAnswerText':prevQuestionAnswerText,
        'prevSection': prevSection,

        'question': question,
        'questionAnswers':questionAnswers,
        'section':currentSection,
        'previewFlag':previewFlag,
        
        'percentageComplete': percentageComplete,

        'backToQuestionnaireFlag': backToQuestionnaireFlag,

    }, RequestContext(request))

#@login_required
def checkComplete(request):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    errorReportObj = AdministrationObj()

    try:

        administrationId = request.POST.get('administrationId', 0)
        administration = Administration.objects.get( pk = administrationId )
        
        questionnaire = administration.questionnaire
        
        sections = Section.objects.filter (questionnaire = questionnaire)

        for section in sections:

            sectionObj = SectionObj()

            sectionObj.section = section

            #print ( " adding section " + str(section.name) )

            questions = Question.objects.filter( section = section ).order_by("questionId")

            isSectionAnswered = False

            for question in questions:

                questionObj = QuestionObj()

                questionObj.question = question

                isAnswered = False

                for questionAnswer in question.answers.all():

                    questionAnswerObj = QuestionAnswerObj()

                    questionAnswerObj.questionAnswer = questionAnswer

                    questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)

                    if len ( questionAnswerInstances ) > 0:

                        questionAnswerInstance = questionAnswerInstances[0]

                        #print (" &&&&  for question answer = " + str(questionAnswer) + " is answered ")

                        questionAnswerObj.isAnswered = True
                        questionAnswerObj.questionAnswerInstance = questionAnswerInstance

                    #if not questionAnswerObj.isAnswered and question.parentQuestion and question.parentAnswer != '':

                        #continue

                        questionObj.questionAnswerObjList.append(questionAnswerObj)

                        isAnswered = True

                        isSectionAnswered = True

                if isAnswered:

                    sectionObj.questionObjList.append(questionObj)
                    
                else:         
                    
                    sectionObj.colorFlag = True

            if isSectionAnswered:

                administrationObj.sectionObjList.append(sectionObj)
                
    except:

        traceback.print_exc(file=sys.stdout)

    return errorReportObj

@login_required
def downloadSessionFile(request):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    try:
        
        upinId = request.POST.get('upinId', 0)
        sessionId = request.session.session_key
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SessionFile.csv"'        

        writer = csv.writer(response,delimiter=",")
        
        writer.writerow([upinId] )
        writer.writerow([sessionId] )

    except:

        traceback.print_exc(file=sys.stdout)

    return response

@login_required
def downloadAdministrationPDF(request):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    try:
        
        administrationId = request.POST.get('administrationId', 0)
        
        administration = Administration.objects.get ( pk = administrationId ) 
        questionnaire = administration.questionnaire
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Questionnaire_response.pdf"'
    
        bufferio = BytesIO()
        
        lineList = []
        
        styles = getSampleStyleSheet()   
        styleN = styles['Normal']        

        styleN.wordWrap = 'CJK'
        
        styleSection = ParagraphStyle(
            name='Normal',
            backColor='#AFA5A8',
            alignment=TA_CENTER,
            textTransform='uppercase',            
       )        

        styleHeader = ParagraphStyle(
            name='Normal',
            #fontSize=18,
            alignment = TA_CENTER,
        ) 

        styleHeaderLeft = ParagraphStyle(
            name='Normal',
            #fontSize=18,
            alignment = TA_LEFT,
        ) 

        styleDetail= ParagraphStyle(
            name='Normal',
            alignment=TA_RIGHT,
        ) 
    
        doc = SimpleDocTemplate(bufferio)
    
        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(bufferio, bottomup = 0)
        
        site = administration.site
        study = administration.upin.study
        patient = administration.upin.patient
        questionnaire = administration.questionnaire
        upinId = administration.upin.upinId

        #barcodeValue = str(administration.upin.upinId) + ' ' + str(request.session.session_key)  
        
        #barcode39 = code39.Extended39(barcodeValue)   
        
        #lineList.append(barcode39) 

        administrationObj = AdministrationObj()

        administrationObj.administration = administration

        questionnaire = administration.questionnaire

        sections = Section.objects.filter(questionnaire = questionnaire).order_by("sequence")
        
        pg = Paragraph(str(questionnaire)  , styleHeader )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))

        pg = Paragraph("UPIN: " + str(administration.upin.upinId)  , styleHeaderLeft )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))

        pg = Paragraph("Assessment Date / Time: " + str(administration.startTime.strftime("%m/%d/%Y %H:%M")) + "", styleN  )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))
        
        pg = Paragraph("First Name: " + str("__________________________________"), styleN  )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))
        
        pg = Paragraph("Last Name: " + str("__________________________________"), styleN  )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))

        endTimeString = ''
        
        if administration.stopTime:
            
            pg = Paragraph("End Date / Time: " + str(administration.stopTime.strftime("%m/%d/%Y %H:%M")) + "", styleN  )    
    
            lineList.append(pg)
            lineList.append(Spacer(1, 12))

        for section in sections:
            
            print ( " for section " + str(section) ) 
            
            pg = Paragraph(str(section) + "", styleSection  )    
    
            lineList.append(pg)
            lineList.append(Spacer(1, 12))

            questions = Question.objects.filter( section = section ).order_by("questionId")

            for question in questions:

                questionPrinted = False

                for questionAnswer in question.answers.all():

                    questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)
                    
                    if len ( questionAnswerInstances ) > 0:

                        questionAnswerInstance = questionAnswerInstances[0]
        
                        if not questionPrinted:
        
                            pg = Paragraph(str(question.questionId) + ". " + str(question), styleN  )    
                    
                            lineList.append(pg)
                            #lineList.append(Spacer(1, 12))
                            
                            questionPrinted = True
                        
                        responseString = str(questionAnswer.text) + "."
                        
                        if questionAnswerInstance.answerText != "":
                            responseString += " " + str(questionAnswerInstance.answerText)
                        
                        if questionAnswerInstance.answerText2 != "":
                            responseString += " : " + str(questionAnswerInstance.answerText2)
                        
                        pg = Paragraph(responseString, styleDetail  )    
                
                        lineList.append(pg)
                        #lineList.append(Spacer(1, 12))
        
        doc.build(lineList)
                    
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = bufferio.getvalue()
        bufferio.close()
        response.write(pdf)

    except:

        traceback.print_exc(file=sys.stdout)

    return response

@login_required
def downloadQuestionnairePDF(request):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    try:
        
        questionnaireId = request.POST.get('questionnaireId', 0)
        
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId ) 
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Questionnaire.pdf"'
    
        bufferio = BytesIO()
    
        lineList = []
        
        styles = getSampleStyleSheet()   
        styleN = styles['Normal']        

        styleN.wordWrap = 'CJK'
        
        styleSection = ParagraphStyle(
            name='Normal',
            backColor='#AFA5A8',
            alignment=TA_CENTER,
            textTransform='uppercase',
       )        

        styleHeader = ParagraphStyle(
            name='Normal',
            #fontSize=18,
            alignment=TA_CENTER,
        ) 

        styleDetail= ParagraphStyle(
            name='Normal',
            alignment=TA_LEFT,
        ) 

        styleDetailRight= ParagraphStyle(
            name='Normal',
            alignment=TA_RIGHT,
        ) 
    
        doc = SimpleDocTemplate(bufferio)    
    
        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(bufferio, bottomup = 0)
        
        pg = Paragraph(str(questionnaire)  , styleHeader )    

        lineList.append(pg)
        lineList.append(Spacer(1, 12))
        
        sections = Section.objects.filter(questionnaire = questionnaire)

        for section in sections:
            
            pg = Paragraph( str(section) + "", styleSection  )    
    
            lineList.append(pg)
            lineList.append(Spacer(1, 12))                     

            questions = Question.objects.filter( section = section ).order_by("questionId")

            for question in questions:

                pg = Paragraph(str(question.questionId) + ". " + str(question) + "", styleDetail )    
        
                lineList.append(pg)
                #lineList.append(Spacer(1, 12))                    
                
                for questionAnswer in question.answers.all():
                    
                    questionAnswerString = questionAnswer.text
                    
                    questionAnswerChoices = QuestionAnswerChoice.objects.filter( questionAnswer = questionAnswer ) 
                    
                    questionAnswerChoices = [x.text for x in questionAnswerChoices]
                    
                    questionAnswerChoices =  ",".join(questionAnswerChoices)
                    
                    if questionAnswerChoices != '':
                    
                        questionAnswerChoiceString = " (" + questionAnswerChoices + ")" 

                        questionAnswerString += questionAnswerChoiceString
                        
                    if questionAnswer.questionAnswerRangeLower and questionAnswer.questionAnswerRangeUpper:
                                              
                        questionAnswerRangeString = "(" + str(questionAnswer.questionAnswerRangeLower) + "-" + str(questionAnswer.questionAnswerRangeUpper) + ")"
                        
                        questionAnswerString += questionAnswerRangeString     
                        
                    questionAnswerTimeUnits = QuestionAnswerTimeUnit.objects.filter( questionAnswer = questionAnswer ) 
                    
                    questionAnswerTimeUnits = [x.text for x in questionAnswerTimeUnits]
                    
                    questionAnswerTimeUnits =  ",".join(questionAnswerTimeUnits)                    
                    
                    if questionAnswerTimeUnits != '':
                    
                        questionAnswerTimeUnitString = " (" + questionAnswerTimeUnits + ")" 

                        questionAnswerString += questionAnswerTimeUnitString                        

                    pg = Paragraph( str(questionAnswerString) , styleDetailRight )    
            
                    lineList.append(pg)
                    #lineList.append(Spacer(1, 12))                         

        doc.build(lineList)
                    
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = bufferio.getvalue()
        bufferio.close()
        response.write(pdf)
                          
    except:

        traceback.print_exc(file=sys.stdout)

    return response

@login_required
def downloadQuestionnaireCSV(request):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    try:
        
        questionnaireId = request.POST.get('questionnaireId', 0)
        
        questionnaire = Questionnaire.objects.get ( pk = questionnaireId ) 
        
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename="Questionnaire.csv"'
        
        questionnaireFile = open(settings.DATA_OUTPUT_FOLDER + "/" + questionnaire.name + ".csv")
        
        writer = csv.writer(response,delimiter=",")

        for index, line in enumerate ( questionnaireFile ):
            
            rowData = line.replace("\n","").split(",") 
            writer.writerow(rowData)
    
        #response.write(csv)
                          
    except:

        traceback.print_exc(file=sys.stdout)

    return response

@login_required
def downloadAggregateReport(request):

    try:
  
        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass      
    
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="AggregateReport.csv"'    
    
        siteId = request.POST.get('siteId', "0")
        studyId = request.POST.get('studyId', "0")

        administratorId = request.POST.get('administratorId', "0")

        questionIds = request.POST.getlist('multipleChoiceId')
        upinIds = request.POST.getlist('reportUpinId')        
        
        #print ( " **** mult choices = " + str(questionIds) ) 

        printSelectionParameters = request.POST.get('printSelectionParameters', "0")
        printCompletedOnly = request.POST.get('printCompletedOnly', "0")
        
        site = ''
        administrator = ''
        
        if siteId != "0" and siteId != "":
            site = Site.objects.get ( pk = int(siteId))
  
        if administratorId != "0" and administratorId != "":
            administrator= Administrator.objects.get ( pk = int(administratorId)) 
            
        study = Study.objects.get ( pk = studyId )
        
        questionnaire = study.questionnaire
        
        sectionIdList = request.POST.getlist('sectionId')  
  
        sections = Section.objects.filter( id__in = sectionIdList )
        
        headerObjList = []
        
        for section in sections:
            
            sectionQuestions = Question.objects.filter ( section = section ) 
            
            for question in sectionQuestions: 
            
                answers = question.answers
                
                multipleChoiceFlag = False  
                
                headerObjTempList = []

                for answer in answers.all():

                    headerObj = HeaderObj()
                    
                    headerObj.sectionName = section.name
                    headerObj.questionText = question.text

                    #print ( " for question = " + str(question.text) + " ontology = " + str(question.ontologyClassSubClass ) + " : " + str(question.ontologyIndividual))
                    if question.ontologyClassSubClass and question.ontologyClassSubClass.name != '':
                        
                        headerObj.questionOntologyClassSubClass = question.ontologyClassSubClass.name

                    if question.ontologyIndividual and question.ontologyIndividual.name != '':
                        headerObj.questionOntologyIndividual = question.ontologyIndividual.name
                    
                    #headerObj.questionOntology = questionOntologyString
                    headerObj.questionAnswerText = answer.text
                    headerObj.questionAnswerOntology = answer.questionAnswerOntology.name

                    headerObj.questionAnswerId = answer.questionAnswerId
                    
                    headerObjTempList.append(headerObj)

                    if answer.questionAnswerType and answer.questionAnswerType.name == "multiple choice" :
                        multipleChoiceFlag = True
                        
                #if multipleChoiceFlag: 
                    
                    #print (" && mult choice " + str(question.text) + " id = " + str(question.id))
                    
                if ( multipleChoiceFlag and str(question.id) in questionIds) or (not multipleChoiceFlag):
                    #print (" && ############### sel mult choice " + str(question.text))

                    headerObjList.extend(headerObjTempList)
        
        questions = []
        
        upinObjList = []
        
        upins = UPIN.objects.filter (study = study)
        
        print ( " *****^^^^ upinIds = " + str(upinIds) )
        
        for upinId in upinIds:
            
            upin = UPIN.objects.get ( pk = upinId )
            
            print ( " %%%%%%%%% for upin = " + str(upin) ) 
            
            upinObj = UPINObj()
            
            upinObj.upin = upin
            
            administrations = Administration.objects.filter (upin = upin)
            
            administration = ''
            
            if len(administrations) > 0:
                
                administration = administrations[0]       

            if printCompletedOnly == "1" and administration == '':
                
                continue
                
            upinObj.administration = administration
            
            for section in sections:
                
                sectionQuestions = Question.objects.filter ( section = section ) 
                
                for question in sectionQuestions: 
                
                    answers = question.answers
                    
                    multipleChoiceFlag = False  
                    
                    columnValueTempList = []                    
    
                    for answer in answers.all():
                        
                        columnValue = ''
                        
                        #columnValue += str(answer.questionAnswerId) + " : " + answer.text
                        
                        if answer.questionAnswerType and answer.questionAnswerType.name == "multiple choice" :
                            multipleChoiceFlag = True                        
    
                        if administration != '':
                            
                            questionAnswerInstances = QuestionAnswerInstance.objects.filter ( administration = administration, question = question, answer = answer )
                            
                            if len ( questionAnswerInstances ) > 0:
                                
                                questionAnswerInstance = questionAnswerInstances[0]
                                
                                columnValue = answer.text
                                
                                if questionAnswerInstance.answerText and questionAnswerInstance.answerText.strip() != '':
                                    
                                    columnValue +=  " " + questionAnswerInstance.answerText
                                    
                                if questionAnswerInstance.answerText2 and questionAnswerInstance.answerText2.strip() != '':                                    
                                    
                                    columnValue +=  " " + questionAnswerInstance.answerText2
                        
                        columnValueTempList.append(columnValue)
                     
                    if ( multipleChoiceFlag and str(question.id) in questionIds) or (not multipleChoiceFlag):
                        upinObj.columnValueList.extend(columnValueTempList)                     
                        
                    #upinObj.columnValueList.append(columnValue)            
            
            upinObjList.append(upinObj)

        writer = csv.writer(response,delimiter=",")

        if printSelectionParameters == "1":

            rowData = ["Date: " + str (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")),"","",""]
            padData = [""]*len(headerObjList)
            
            rowData.extend(padData)
            writer.writerow(rowData)

            rowData = ["Site: " + str ( site),"","",""]
            writer.writerow(rowData)

            rowData = ["Administrator: " + str ( administrator),"","",""]
            writer.writerow(rowData)

            rowData = ["Study: " + str ( study),"","",""]
            writer.writerow(rowData)
            
        rowData = ["","","","","","",""]
    
        sectionNames = [x.sectionName for x in headerObjList] 
    
        #for headerObj in headerObjList:
            
        rowData.extend(sectionNames)   
        writer.writerow(rowData)        
         
        rowData = ["","","","","","",""]
        
        questionTexts = [x.questionText for x in headerObjList]   
        
        rowData.extend(questionTexts)           
        writer.writerow(rowData)   
        
        rowData = ["","","","","","",""]
        
        questionOntologieClassSubClasses = [x.questionOntologyClassSubClass for x in headerObjList]   
        
        rowData.extend(questionOntologieClassSubClasses)           
        writer.writerow(rowData)  
        
        rowData = ["","","","","","",""]
        
        questionOntologieIndividuals = [x.questionOntologyIndividual for x in headerObjList]   
        
        rowData.extend(questionOntologieIndividuals)           
        writer.writerow(rowData) 
        
        rowData = ["","","","","","",""]
        
        questionAnswerTexts = [x.questionAnswerText for x in headerObjList]   
        
        rowData.extend(questionAnswerTexts)           
        writer.writerow(rowData)                   

        rowData = ["","","","","","",""]
        
        questionAnswerOntologies = [x.questionAnswerOntology for x in headerObjList]   
        
        rowData.extend(questionAnswerOntologies)           
        writer.writerow(rowData)  

        rowData = ["","","","","","",""]        
        padData = [""]*len(headerObjList)
        
        rowData.extend(padData)
        writer.writerow(rowData)                   

        rowData = ["UPIN","Site","Administrator","Start", "Stop","Time Taken (minutes)","Percentage Complete"]
        rowData.extend(padData)        
        writer.writerow(rowData)                   
                
        for upinObj in upinObjList:
            
            print ( " %%%%%%%%% for upin = " + str(upinObj.upin) + " completed " + str(printCompletedOnly))            
            
            printData = False

            if upinObj.administration != '':
                
                stopTimeString = ''
                
                timeTaken = ''
                
                if administration.stopTime:
                    
                    stopTimeString = administration.stopTime.strftime("%a, %d %b %Y %H:%M:%S")
                    
                    timeTaken = round(( administration.stopTime - administration.startTime ).total_seconds()/ 60.0 )
                    
                percentageComplete = getPercentageCompleteTotal(administration)

                rowData = [upinObj.upin.upinId,upinObj.administration.site.name,upinObj.administration.administrator.user.username,administration.startTime.strftime("%a, %d %b %Y %H:%M:%S"), stopTimeString, timeTaken, str(percentageComplete)]

                printData = True

            elif printCompletedOnly == "0":
                
                rowData = [upinObj.upin.upinId,"","","",""]
                
                printData = True
    
            if printData:

                for columnValue in upinObj.columnValueList:
                    rowData.append(str(columnValue))
    
                writer.writerow(rowData)
                
        ############

        ## Open BytesIO to grab in-memory ZIP contents
        #s = io.BytesIO()

        ## The zip compressor
        #zf = zipfile.ZipFile(s, "w")
            
        #zf.write(toPath)

        #zf.close()

        #zip_filename = "Project_" + str(analysisDetail.dataFile.project.name) + "_" + str(request.user) + "_Analysis_" + analysisDetail.name + ".zip"

        ## Grab ZIP file from in-memory, make response with correct MIME-type
        #resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        ## ..and correct content-disposition
        #resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename        
        ##############
    
    except:

        traceback.print_exc(file=sys.stdout)
    
    return response


@login_required
def downloadPercentageCompleteReport(request):

    try:
  
        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass      
    
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PercentageCompleteReport.csv"'    
    
        siteId = request.POST.get('siteId', "0")
        studyId = request.POST.get('studyId', "0")

        administratorId = request.POST.get('administratorId', "0")

        questionIds = request.POST.getlist('multipleChoiceId')
        upinIds = request.POST.getlist('reportUpinId')        
        
        #print ( " **** mult choices = " + str(questionIds) ) 

        printSelectionParameters = request.POST.get('printSelectionParameters', "0")
        printCompletedOnly = request.POST.get('printCompletedOnly', "0")
        
        site = ''
        administrator = ''
        
        if siteId != "0" and siteId != "":
            site = Site.objects.get ( pk = int(siteId))
  
        if administratorId != "0" and administratorId != "":
            administrator= Administrator.objects.get ( pk = int(administratorId)) 
            
        study = Study.objects.get ( pk = studyId )
        
        questionnaire = study.questionnaire
        
        sectionIdList = request.POST.getlist('sectionId')  
  
        sections = Section.objects.filter( id__in = sectionIdList )

        writer = csv.writer(response,delimiter=",")

        if printSelectionParameters == "1":

            rowData = ["Date: " + str (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")),"","",""]
            writer.writerow(rowData)

            rowData = ["Site: " + str ( site),"","",""]
            writer.writerow(rowData)

            rowData = ["Administrator: " + str ( administrator),"","",""]
            writer.writerow(rowData)

            rowData = ["Study: " + str ( study),"","",""]
            writer.writerow(rowData)
            
        rowData = ["","","","","","",""]
    
        sectionNames = [x.name for x in sections] 
            
        rowData.extend(sectionNames)   
        writer.writerow(rowData)        
         
        rowData = ["UPIN","Site","Administrator","Start", "Stop", "Time Taken", "Percent Complete"]
        writer.writerow(rowData)
        
        for upinId in upinIds:
            
            upin = UPIN.objects.get ( pk = upinId )
            
            administrations = Administration.objects.filter (upin = upin)
            
            administration = ''
            
            if len(administrations) > 0:
                
                administration = administrations[0]       

            if printCompletedOnly == "1" and administration == '':
                
                continue
                
            if administration != '':
                
                stopTimeString = ''
                
                timeTaken    = ''            
                
                if administration.stopTime:
                    
                    stopTimeString = administration.stopTime.strftime("%a, %d %b %Y %H:%M:%S")
                    
                    timeTaken = round(( administration.stopTime - administration.startTime ).total_seconds()/ 60.0 )
                    
                percentageComplete = getPercentageCompleteTotal(administration)

                rowData = [upin.upinId,administration.site.name,administration.administrator.user.username,administration.startTime.strftime("%a, %d %b %Y %H:%M:%S"), stopTimeString, timeTaken, str(percentageComplete)]                

                #rowData = [upinObj.upin.upinId,upinObj.administration.site.name,upinObj.administration.administrator.user.username,administration.startTime.strftime("%a, %d %b %Y %H:%M:%S"), stopTimeString]

            for section in sections:
                
                if administration != '':
                    
                    percentageComplete, percentageCompleteSection = getPercentageComplete(administration, section)
 
                    rowData.append(str(percentageCompleteSection))
        
            writer.writerow(rowData)

    except:

        traceback.print_exc(file=sys.stdout)
    
    return response

def getTreeDepth(administration, question, numAnswered, numTotal):
    
    try:    
      
        questionAnswerInstances = QuestionAnswerInstance.objects.filter(question = question, administration = administration)
        
        numTotal += 1

        if len(questionAnswerInstances) > 0: 

            print ( " ----@@@@@@@@@@ --- :::::: add to instance = " + str(len(questionAnswerInstances)) + " for question " + str(question)) 
        
            numAnswered += 1
            
            questionAnswerInstance = questionAnswerInstances [0]

            childQuestions = Question.objects.filter(parent = question, parentAnswer = questionAnswerInstance.answer)
            
            nextQuestion = ''
            
            if len ( childQuestions ) > 0 :
    
                nextQuestion = childQuestions [0]
            
                return getTreeDepth(administration, nextQuestion, numAnswered, numTotal)
          
            else:
                
                return numAnswered, numTotal

    except:
    
        traceback.print_exc(file=sys.stdout)
    
    return numAnswered, numTotal

def getPercentageComplete(administration, currentSection):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    percentageComplete = 0
    
    percentageCompleteSection = 0
    
    try:

        questionnaire = administration.questionnaire
        
        sections = Section.objects.filter(questionnaire = questionnaire)
        
        numSections = len(sections)

        numerator = 0
        denominator = 0

        numeratorSection = 0
        denominatorSection = 0
        
        for section in sections:
            
            #questions = Question.objects.filter ( section = section, parent = None )

            questions = Question.objects.filter ( section = section )
            
            #print ( " $$$@@@@@@ $$ for  section  = " + str(section) + " numTotal = " + str(len(questions)) )             
            
            for question in questions:
                
                # check if the parent of this question is answered, and if so, process it further.

                processQuestion = True
               
                if question.parent and question.parentAnswer:
               
                    questionAnswerInstances =  QuestionAnswerInstance.objects.filter(question = question.parent, answer = question.parentAnswer, administration = administration)
                    
                    if len(questionAnswerInstances) == 0:
                        
                        processQuestion = False 
                        
                if processQuestion:
               
                    numAnswered, numTotal = getTreeDepth(administration, question, 0, 0)

                    numerator += numAnswered
                    denominator += numTotal
                    
                    if currentSection.id == section.id:
                        
                        print ( " $$$@@@@@@ $$ for  question  = " + str(question) )       
                    
                        print ( " $$$$$ for current section numAnswered = " + str(numAnswered) + " numTotal = " + str(numTotal) + " numerator = " + str(numerator) + " denominator = " + str(denominator) ) 
                
                        numeratorSection += numAnswered
                        denominatorSection += numTotal     
                    
        if denominator > 0:

            print ( " IN PERCENTAGE ^^ALL in section^ " + str(numerator) + " / " + str(denominator) ) 
            
            percentageComplete = float(numerator) / float(denominator)
            
            percentageComplete = round(percentageComplete*100)
            
        if denominatorSection > 0:

            print ( " IN PERCENTAGE ^^SECTION^ " + str(numeratorSection) + " / " + str(denominatorSection) ) 
            
            percentageCompleteSection = float(numeratorSection) / float(denominatorSection)
            
            print ( " IN PERCENTAGE 4444 ^^SECTION^ " + str(percentageCompleteSection)  ) 
            
            percentageCompleteSection = int(round(percentageCompleteSection*100))

    except:

        traceback.print_exc(file=sys.stdout)

    return percentageComplete, percentageCompleteSection

def getPercentageCompleteTotal(administration):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    percentageComplete = 0
    
    percentageCompleteSection = 0
    
    try:

        questionnaire = administration.questionnaire
        
        sections = Section.objects.filter(questionnaire = questionnaire)
        
        numSections = len(sections)

        numerator = 0
        denominator = 0
        
        for section in sections:
            
            questions = Question.objects.filter ( section = section, parent = None )
            
            for question in questions:
                
                processQuestion = True
               
                if question.parent and question.parentAnswer:
               
                    questionAnswerInstances =  QuestionAnswerInstance.objects.filter(question = question.parent, answer = question.parentAnswer, administration = administration)
                    
                    if len(questionAnswerInstances) == 0:
                        
                        processQuestion = False 
                        
                if processQuestion:                
                
                    numAnswered, numTotal = getTreeDepth(administration, question, 0, 0)
    
                    numerator += numAnswered
                    denominator += numTotal
                        
        if denominator > 0:

            print ( " IN PERCENTAGE ^ TOTAL ^^ " + str(numerator) + " / " + str(denominator) ) 
            
            percentageComplete = float(numerator) / float(denominator)
            
            percentageComplete = int(round(percentageComplete*100))

    except:

        traceback.print_exc(file=sys.stdout)

    return percentageComplete

def reviewAdministration(request,  completedFlag, surveyUser):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    percentageComplete = 0

    try:

        prevQuestion = ''
        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''
        prevSection = ''
        
        administrationId = request.POST.get('administrationId', 0)
        administration = Administration.objects.get(pk=administrationId)
        
        administrator = administration.administrator
        
        site = administration.site
        study = administration.upin.study
        
        patient = administration.upin.patient
        questionnaire = administration.questionnaire
        
        upinId = administration.upin.upinId
        
        questionId = request.POST.get('questionId', 0)
        
        question = ''
        
        questionAnswers = []
        
        sectionId = request.POST.get('sectionId', 0)
        
        currentSection = ''
        
        prevQuestionAnswer = ''
        prevQuestionAnswerText = ''
        
        isQuestionAnswered = False
        
        questionAnswerId = 0
        
        administrationObj = AdministrationObj()
        
        administrationObj.administration = administration
        
        questionnaire = administration.questionnaire
        
        sections = Section.objects.filter(questionnaire = questionnaire).order_by("sequence")
        
        currentSection = sections[0]
        
        for section in sections:
        
            sectionObj = SectionObj()
        
            sectionObj.section = section
        
            print ( " adding section " + str(section.name) )
        
            questions = Question.objects.filter( section = section )
        
            isSectionAnswered = False
        
            for question in questions:
        
                questionObj = QuestionObj()
        
                questionObj.question = question
        
                isAnswered = False
        
                for questionAnswer in question.answers.all():
        
                    questionAnswerObj = QuestionAnswerObj()
        
                    questionAnswerObj.questionAnswer = questionAnswer
        
                    questionAnswerInstances = QuestionAnswerInstance.objects.filter (administration = administration, question = question, answer = questionAnswer)
        
                    if len ( questionAnswerInstances ) > 0:
        
                        questionAnswerInstance = questionAnswerInstances[0]
        
                        #print (" &&&&  for question answer = " + str(questionAnswer) + " is answered ")
        
                        questionAnswerObj.isAnswered = True
                        questionAnswerObj.questionAnswerInstance = questionAnswerInstance
        
                        isAnswered = True
                        isSectionAnswered = True
        
                    questionAnswerChoiceList = QuestionAnswerChoice.objects.filter (questionAnswer = questionAnswer)
                    questionAnswerObj.questionAnswerChoiceList = questionAnswerChoiceList
                    
                    #print ( " adding choices " + str(questionAnswerChoiceList) ) 
        
                    questionAnswerTimeUnitList = QuestionAnswerTimeUnit.objects.filter (questionAnswer = questionAnswer)
                    questionAnswerObj.questionAnswerTimeUnitList = questionAnswerTimeUnitList
        
                    #print ( " adding time units " + str(questionAnswerTimeUnitList) )                         
                    
                    questionObj.questionAnswerObjList.append(questionAnswerObj)
        
                if isAnswered:
        
                    sectionObj.questionObjList.append(questionObj)
                    
                else:
                    
                    if not question.parent:                         
                    
                        sectionObj.colorFlag = True
        
            #if isSectionAnswered:
        
            administrationObj.sectionObjList.append(sectionObj)
            
            percentageComplete = getPercentageCompleteTotal(administration)
            
            showSectionPercentageFlag = False
            
            print ( " percent complete = " + str(percentageComplete) )             
    
    except:

        traceback.print_exc(file=sys.stdout)

    return render_to_response("smellSurvey/displayAdministration.html", {

        "backToQuestionnaireFlag" : True,    
        "previewFlag" : completedFlag,
        "administrationObj" : administrationObj,
        "upinId": upinId,
    
        "surveyUser": surveyUser,
    
        "site" : site,
        "study" : study,
        "sections" : sections,
        "patient" : patient,
        "questionnaire" : questionnaire,
    
        "administration" : administration,
        "administrator" : administrator,
    
        'prevQuestion' : prevQuestion,
        'prevQuestionAnswer': prevQuestionAnswer,
        'prevQuestionAnswerText':prevQuestionAnswerText,
        'prevSection': prevSection,
    
        'percentageComplete': percentageComplete,  
        #'percentageCompleteSection': percentageCompleteSection,
        
        'showSectionPercentageFlag':showSectionPercentageFlag,        
        
        'question': question,
        'questionAnswers':questionAnswers,
        'section':currentSection,
    
    }, RequestContext(request))

def aggregateReport(request):

    try:  
    
        surveyUser = ''
        try:
            surveyUser = SurveyUser.objects.filter ( user = request.user )[0]
        except:
            pass      
    
        siteId = request.POST.get('siteId', "0")
        studyId = request.POST.get('studyId', "0")
        administratorId = request.POST.get('administratorId', "0")
        
        site = ''
        administrator = ''

        if siteId != "0":
            site = Site.objects.get ( pk = siteId)

        if administratorId != "0":
            administrator= Administrator.objects.get ( pk = administratorId)
            
        study = Study.objects.get ( pk = studyId )
        
        questionnaire = study.questionnaire

        sections = Section.objects.filter( questionnaire = questionnaire )
        
        questions = []
        
        upinObjList = []
        
        upins = UPIN.objects.filter (study = study)
        
        for upin in upins:
            
            upinObj = UPINObj()
            
            upinObj.upin = upin
            
            administrations = Administration.objects.filter (upin = upin)
            
            if len(administrations) > 0:
                
                administration = administrations[0]

                upinObj.administration = administration
                
            upinObjList.append(upinObj)
        
        for section in sections:
            
            sectionQuestions = Question.objects.filter ( section = section ) 
            
            for question in sectionQuestions: 
            
                answers = question.answers
                multipleChoiceFlag = False
    
                for answer in answers.all():
                    if answer.questionAnswerType and answer.questionAnswerType.name == "multiple choice" :
                        multipleChoiceFlag = True
                        break
                    
                if multipleChoiceFlag:
                    questions.append(question)
                    
        #print ( " questions = " + str(questions))
        
    except:
        traceback.print_exc(file=sys.stdout)
    
    return render_to_response("smellSurvey/aggregateReport.html", {
    
        "site" : site,
        "administrator" : administrator,
        "study": study,

        "siteId" : siteId,
        "administratorId" : administratorId,

        "sections" : sections,
        "questions" : questions,
        
        "upinObjList" : upinObjList,
    
        "surveyUser": surveyUser,
    
    }, RequestContext(request))      
    