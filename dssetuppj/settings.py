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
