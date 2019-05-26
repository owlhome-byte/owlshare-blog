"""
Django settings for typeidea project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+cb%4x6t91et+bp!a2(7e33g7sxlln73#p7m1288uz5mwax!8&'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['39.100.109.147', '127.0.0.1', 'localhost', '.owlshare.top']


# Application definition

INSTALLED_APPS = [
    'typeidea',
    'blog',
    'config',
    'comment',
    'xadmin',
    'crispy_forms',
    'dal',
    'dal_select2',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'gunicorn',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'blog.middleware.user_id.UserIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'typeidea.urls'

THEME = 'bootstrap'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'themes', THEME, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'typeidea.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'themes', THEME, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'themes', THEME, 'static')
]

XADMIN_TITLE = '管理后台'
XADMIN_FOOTER_TITLE = 'power by lighteft@gmail'

CKEDITOR_CONFIGS={
    'default':{
        'toolbar':'full',
        'height':300,
        'width':800,
        'tabSpaces':4,
        'extraPlugins':'codesnippet',
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = 'article_images'

DEFAULT_FILE_STORAGE = 'typeidea.storage.WatermarkStorage'

REST_FRAMEWORK ={
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':2,
}

