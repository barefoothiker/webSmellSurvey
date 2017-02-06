"""
Django settings for rnaseq project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#import pyexcel.ext.xlsx  # This is required for tmp file handlers.

#import pyexcel.ext  # This is required for tmp file handlers.

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#DATA_OUTPUT_FOLDER = "/Users/mitras/projects/data"

DATA_OUTPUT_FOLDER = "."

ROOT_URLCONF = 'urls'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

## Make this unique, and don't share it with anybody.
SECRET_KEY = 'idmm)d5h)kwxcopo%0rirfk@^88xcki4dx#slgp5_v#0)lt7gd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

#ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smellSurvey',
    'registration'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# table prefix name
DB_PREFIX = 'smellSurvey'
# Local time zone for this installation. Choices can be found here:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'smellsurveydb',                      # Or path to database file if using sqlite3.

     
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'admin',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
#        'OPTIONS': {
 #           'init_command': 'SET storage_engine=INNODB',
  #          }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [
     os.path.join(BASE_DIR, './static'),
]

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    '/templates/',
)

#FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        #"django_excel.TemporaryExcelFileUploadHandler", 
                        #"django.core.files.uploadhandler.MemoryFileUploadHandler",
                        #"django.core.files.uploadhandler.TemporaryFileUploadHandler",)

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

LOGIN_REDIRECT_URL = "/smellSurvey/"

