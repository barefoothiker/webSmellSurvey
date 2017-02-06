from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from main import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'smellSurvey.views.landing'),
    (r'^smellSurvey/$', 'smellSurvey.views.landing'), 

    (r'^smellSurvey/processLanding/$', 'smellSurvey.views.processLanding'),    

    (r'^smellSurvey/downloadAdministrationPDF/$', 'smellSurvey.views.downloadAdministrationPDF'),    

    (r'^smellSurvey/downloadQuestionnairePDF/$', 'smellSurvey.views.downloadQuestionnairePDF'),    

    (r'^smellSurvey/downloadQuestionnaireCSV/$', 'smellSurvey.views.downloadQuestionnaireCSV'),    

    (r'^smellSurvey/listTesters/$', 'smellSurvey.views.listTesters'),
    
    (r'^smellSurvey/editTester/$', 'smellSurvey.views.editTester'),
    (r'^smellSurvey/submitEditTester/$', 'smellSurvey.views.submitEditTester'),

    (r'^smellSurvey/addTester/$', 'smellSurvey.views.addTester'),
    (r'^smellSurvey/submitAddTester/$', 'smellSurvey.views.submitAddTester'),

    (r'^smellSurvey/listPatients/$', 'smellSurvey.views.listPatients'),
    
    (r'^smellSurvey/addPatient/$', 'smellSurvey.views.addPatient'),
    (r'^smellSurvey/submitAddPatient/$', 'smellSurvey.views.submitAddPatient'),

    (r'^smellSurvey/listAdministrators/$', 'smellSurvey.views.listAdministrators'),
    (r'^smellSurvey/addAdministrator/$', 'smellSurvey.views.addAdministrator'),
    (r'^smellSurvey/submitAddAdministrator/$', 'smellSurvey.views.submitAddAdministrator'),

    (r'^smellSurvey/listSites/$', 'smellSurvey.views.listSites'),
    
    (r'^smellSurvey/listUPINs/$', 'smellSurvey.views.listUPINs'),    
    
    (r'^smellSurvey/listSuperUsers/$', 'smellSurvey.views.listSuperUsers'),
    
    (r'^smellSurvey/listStudies/$', 'smellSurvey.views.listStudies'),

    (r'^smellSurvey/listRoles/$', 'smellSurvey.views.listRoles'),

    (r'^smellSurvey/editSuperUser/$', 'smellSurvey.views.editSuperUser'),
    (r'^smellSurvey/submitEditSuperUser/$', 'smellSurvey.views.submitEditSuperUser'),

    (r'^smellSurvey/addSuperUser/$', 'smellSurvey.views.addSuperUser'),
    (r'^smellSurvey/submitAddSuperUser/$', 'smellSurvey.views.submitAddSuperUser'),
    
    (r'^smellSurvey/editAdministrator/$', 'smellSurvey.views.editAdministrator'),
    (r'^smellSurvey/submitEditAdministrator/$', 'smellSurvey.views.submitEditAdministrator'),

    (r'^smellSurvey/addAdministrator/$', 'smellSurvey.views.addAdministrator'),
    (r'^smellSurvey/submitAddAdministrator/$', 'smellSurvey.views.submitAddAdministrator'),

    (r'^smellSurvey/editSite/$', 'smellSurvey.views.editSite'),
    (r'^smellSurvey/submitEditSite/$', 'smellSurvey.views.submitEditSite'),

    (r'^smellSurvey/addRole/$', 'smellSurvey.views.addRole'),
    (r'^smellSurvey/submitAddRole/$', 'smellSurvey.views.submitAddRole'),

    (r'^smellSurvey/editRole/$', 'smellSurvey.views.editRole'),
    (r'^smellSurvey/submitEditRole/$', 'smellSurvey.views.submitEditRole'),

    (r'^smellSurvey/addSite/$', 'smellSurvey.views.addSite'),
    (r'^smellSurvey/submitAddSite/$', 'smellSurvey.views.submitAddSite'),

    (r'^smellSurvey/editStudy/$', 'smellSurvey.views.editStudy'),
    (r'^smellSurvey/submitEditStudy/$', 'smellSurvey.views.submitEditStudy'),

    (r'^smellSurvey/addStudy/$', 'smellSurvey.views.addStudy'),
    (r'^smellSurvey/submitAddStudy/$', 'smellSurvey.views.submitAddStudy'),

    (r'^smellSurvey/editPatient/$', 'smellSurvey.views.editPatient'),
    (r'^smellSurvey/submitEditPatient/$', 'smellSurvey.views.submitEditPatient'),

    (r'^smellSurvey/selectSiteStudy/$', 'smellSurvey.views.selectSiteStudy'),
    
    (r'^smellSurvey/selectPatient/$', 'smellSurvey.views.selectPatient'),

    
    (r'^smellSurvey/administerQuestionnaire/$', 'smellSurvey.views.administerQuestionnaire'),

    (r'^smellSurvey/submitAdministerQuestionnaire/$', 'smellSurvey.views.submitAdministerQuestionnaire'),

    (r'^smellSurvey/uploadQuestionnaire/$', 'smellSurvey.views.uploadQuestionnaire'),
    (r'^smellSurvey/submitUploadQuestionnaire/$', 'smellSurvey.views.submitUploadQuestionnaire'),    

    (r'^smellSurvey/administerQuestionnaire/$', 'smellSurvey.views.administerQuestionnaire'),
    (r'^smellSurvey/submitAdministerQuestionnaire/$', 'smellSurvey.views.submitAdministerQuestionnaire'),    

    (r'^smellSurvey/addQuestion/$', 'smellSurvey.views.addQuestion'),
    (r'^smellSurvey/submitAddQuestion/$', 'smellSurvey.views.submitAddQuestion'),

    (r'^smellSurvey/addQuestionAnswer/$', 'smellSurvey.views.addQuestionAnswer'),
    (r'^smellSurvey/submitAddQuestionAnswer/$', 'smellSurvey.views.submitAddQuestionAnswer'),
    
    (r'^smellSurvey/listQuestionnaires/$', 'smellSurvey.views.listQuestionnaires'),
    (r'^smellSurvey/displayQuestionnaire/$', 'smellSurvey.views.displayQuestionnaire'), 

    (r'^smellSurvey/deleteQuestionnaire/$', 'smellSurvey.views.deleteQuestionnaire'), 
    (r'^smellSurvey/editQuestion/$', 'smellSurvey.views.editQuestion'),  

    (r'^smellSurvey/deleteQuestion/$', 'smellSurvey.views.deleteQuestion'),  
    (r'^smellSurvey/deleteQuestionAnswer/$', 'smellSurvey.views.deleteQuestionAnswer'),  
    
    (r'^smellSurvey/submitEditQuestion/$', 'smellSurvey.views.submitEditQuestion'),      

    (r'^smellSurvey/listAdministrations/$', 'smellSurvey.views.listAdministrations'),
    (r'^smellSurvey/displayAdministration/$', 'smellSurvey.views.displayAdministration'), 
    

    (r'^smellSurvey/listAdministrations/$', 'smellSurvey.views.listAdministrations'),

    (r'^smellSurvey/displayAdministration/$', 'smellSurvey.views.displayAdministration'), 

    (r'^smellSurvey/administerQuestionnaireWelcome/$', 'smellSurvey.views.administerQuestionnaireWelcome'), 

    (r'^smellSurvey/administerQuestionnaireBackground/$', 'smellSurvey.views.administerQuestionnaireBackground'), 

    (r'^smellSurvey/administerQuestionnaireFirst/$', 'smellSurvey.views.administerQuestionnaireFirst'), 
    (r'^smellSurvey/administerQuestionnaireSecond/$', 'smellSurvey.views.administerQuestionnaireSecond'), 
    (r'^smellSurvey/administerQuestionnaireThird/$', 'smellSurvey.views.administerQuestionnaireThird'), 

    (r'^smellSurvey/administerQuestionnaireLegal/$', 'smellSurvey.views.administerQuestionnaireLegal'), 
    (r'^smellSurvey/administerQuestionnaireConfirmStart/$', 'smellSurvey.views.administerQuestionnaireConfirmStart'),
    
    (r'^smellSurvey/submitRestart/$', 'smellSurvey.views.submitRestart'),        
    
    (r'^smellSurvey/completeAdministration/$', 'smellSurvey.views.completeAdministration'), 

    (r'^smellSurvey/checkComplete/$', 'smellSurvey.views.checkComplete'), 

    (r'^smellSurvey/downloadSessionFile/$', 'smellSurvey.views.downloadSessionFile'), 
    
    (r'^smellSurvey/reloadUPIN/$', 'smellSurvey.views.reloadUPIN'), 

    (r'^smellSurvey/selectParameters/$', 'smellSurvey.views.selectParameters'),     

    (r'^smellSurvey/aggregateReport/$', 'smellSurvey.views.aggregateReport'),     

    (r'^smellSurvey/downloadAggregateReport/$', 'smellSurvey.views.downloadAggregateReport'),     
    
    (r'^smellSurvey/submitDeletePatients/$', 'smellSurvey.views.submitDeletePatients'),     
    
    (r'^smellSurvey/downloadPercentageCompleteReport/$', 'smellSurvey.views.downloadPercentageCompleteReport'),         

    #(r'^smellSurvey/generateSurveyLink/$', 'smellSurvey.views.generateSurveyLink'), 
    
    (r'^admin/', include(admin.site.urls)),

    (r'^register/', 'smellSurvey.views.register'),
    (r'^accounts/', include('registration.urls')),
        
) 
