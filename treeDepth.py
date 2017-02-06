import os, shutil, json, re, csv
import sys, traceback, datetime, time, math
from smellSurvey.models import * 

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

        #print ( " @@@@@@@@@@ in navigate questionnaire for question = " + str(question.questionId) + "::" + str(question) )

        questions = Question.objects.filter (questionId__gt = question.questionId, section = section).exclude(parent = question)

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

def getTreeDepth(question, numAnswered, numTotal):
    
    try:    
      
        questionAnswerInstances = QuestionAnswerInstance.objects.filter(question = question)
        
        numTotal += 1

        if len(questionAnswerInstances) > 0: 

            print ( " ----@@@@@@@@@@ --- :::::: add to instance = " + str(len(questionAnswerInstances)) ) 
        
            numAnswered += 1

        childQuestions = Question.objects.filter(parent = question)
        
        nextQuestion = ''
        
        if len ( childQuestions ) > 0 :

            nextQuestion = childQuestions [0]
            
            #print ( " :::::: found child = " + str(nextQuestion) ) 

        ##else:
            
            #nextQuestion = navigateSection (nextQuestion, nextQuestion.section, nextQuestion)  

            print ( " ------- :::::: found next question = " + str(nextQuestion) ) 
            
        #if nextQuestion != '':
            
            return getTreeDepth(nextQuestion, numAnswered, numTotal)
        
        else:
            
            return numAnswered, numTotal

    except:
    
        traceback.print_exc(file=sys.stdout)
    
    return numAnswered, numTotal

def getPercentageComplete(administration):

    ''' Check If Complete
    Input: Request
    Output ErrorReport
    '''

    percentageComplete = 0

    try:

        questionnaire = administration.questionnaire
        
        sections = Section.objects.filter(questionnaire = questionnaire)
        
        numSections = len(sections)

        numerator = 0
        denominator = 0
        
        for section in sections:
            
            print ( " !!!! for section = " + str(section) ) 
            
            questions = Question.objects.filter ( section = section )
            
            for question in questions:
                
                numAnswered, numTotal = 0,0
                
                numAnswered, numTotal = getTreeDepth(question, numAnswered, numTotal)

                print ( " !!!**** for question = " + str(question) + " numAnswered " + str(numAnswered ) + "numTotal " + str(numTotal) ) 

                numerator += numAnswered
                denominator += numTotal
        
            #break

        if denominator > 0:

            print ( " IN PERCENTAGE ^^^ " + str(numerator) + " / " + str(denominator) ) 
            
            percentageComplete = float(numerator) / float(denominator)
            
            percentageComplete = round(percentageComplete*100)
            
    except:

        traceback.print_exc(file=sys.stdout)

    return percentageComplete

ad = Administration.objects.get ( pk = 42 ) 

getPercentageComplete(ad)