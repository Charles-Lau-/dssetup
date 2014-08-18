"""
Django settings for dssetuppj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from dssetup.staticVar import SESSION_EXPIRATION

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yak6$c5(efb^sqv$o%wx=&kc_%wr$9p8%th*dx-2qga$6kotf*'

# SECURITY WARNING: don't run with debug turned on in production!
 

TEMPLATE_DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_E_COOKIE_AGE = SESSION_EXPIRATION
PJ_ROOT= os.path.abspath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '../'))

DEBUG = True

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dssetup',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dssetup.ware.LoginWare.LoginWare',
    'dssetup.ware.PermissionWare.PermissionWare', 
)

ROOT_URLCONF = 'dssetuppj.urls'
TEMPLATE_DIRS = (
                 os.path.join(os.path.dirname(__file__)[:-10],"dssetup\\templates").replace("\\","/"),
                 os.path.join(os.path.dirname(__file__)[:-10],"dssetup\\templates\\base").replace("\\","/"),
                 os.path.join(os.path.dirname(__file__)[:-10],"dssetup\\templates\\admin").replace("\\","/"),
                 os.path.join(os.path.dirname(__file__)[:-10],"dssetup\\templates\\form").replace("\\","/")
                 ) 
WSGI_APPLICATION = 'dssetuppj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
 
     'django.core.context_processors.request',
  
 )
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__),"../static").replace("\\","/")

APPEND_SLASH = True

#login part
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','all.log'),  
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'dssetup_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'view_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup_view.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'action_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup_action.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'service_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup_service.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup_request.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'ware_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','dssetup_ware.log'),   
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },                                                    
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PJ_ROOT+'/logs/','script.log'),  
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'dssetup':{
            'handlers': ['dssetup_handler'],
            'level': 'DEBUG',
            'propagate': False         
        },
         
        'dssetup.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'dssetup.view': {
            'handlers': ['view_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'dssetup.action': {
            'handlers': ['action_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'dssetup.service': {
            'handlers': ['service_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'dssetup.ware': {
            'handlers': ['ware_handler'],
            'level': 'DEBUG',
            'propagate': True
        },                                 
        'scripts': {  
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}