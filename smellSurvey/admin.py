from django.contrib import admin
from smellSurvey.models import *
from django.contrib.auth.models import User

from .models import *

admin.site.register(Ontology)
admin.site.register(Question)
admin.site.register(Questionnaire)

