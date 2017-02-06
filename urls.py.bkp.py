from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', 'smellingDisorder.views.landing'),
    (r'^processLanding/$', 'smellingDisorder.views.processLanding'),

    (r'^smellingDisorder/$', 'smellingDisorder.views.landing'),
    (r'^smellingDisorder/processLanding/$', 'smellingDisorder.views.processLanding'),

    (r'^smellingDisorder/listOntologies/$', 'smellingDisorder.views.listOntologies'),  
    (r'^smellingDisorder/displayOntology/$', 'smellingDisorder.views.displayOntology'), 

    (r'^smellingDisorder/listQuestions/$', 'smellingDisorder.views.listQuestions'),  
    (r'^smellingDisorder/displayQuestion/$', 'smellingDisorder.views.displayQuestion'), 
    
    (r'^smellingDisorder/listQuestionnaires/$', 'smellingDisorder.views.listQuestionnaires'),  
    (r'^smellingDisorder/displayQuestionnaire/$', 'smellingDisorder.views.displayQuestionnaire'), 
    
    (r'^smellingDisorder/questionnaireFileSubmit/$', 'smellingDisorder.views.questionnaireFileSubmit'),

    (r'^smellingDisorder/visualize/$', 'smellingDisorder.views.visualize'),
    
    (r'^accounts/', include('registration.urls')),
) 

urlpatterns += staticfiles_urlpatterns()

#print str(urlpatterns)
