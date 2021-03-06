"""
Django settings for E_Tech project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku
import dj_database_url
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-575rbk*tw5=*4gqq$-lj3hz!2#u)n=-(f(0^r6w-vl0c7t0ll+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  


ALLOWED_HOSTS = ["localhost","127.0.0.1","pc-puzzle.herokuapp.com"]


# Application definition  
   
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',   
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #myapps
    "Tech_Parts",
    'crispy_forms',
    'django_filters',
    'tinymce',
    #my lib
    'allauth',   
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'E_Tech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'E_Tech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     } 
# }              
   
# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': "d84157ac50tjvp",

#         'USER': 'obyidxalwosihe',

#         'PASSWORD': '20261adbae0585b0bfe99a6da4e1b13203f63bfe1f33da62a05a446a22022851',

#         'HOST': 'ec2-34-195-233-155.compute-1.amazonaws.com',

#         'PORT': '5432',

#     }

# }

DATABASES = {   

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': "d3bqc429mgi72n",

        'USER': 'hminyworkrvlwz',

        'PASSWORD': '29be365dd16e88e044b38ecfffc447beb8fca8ecb15e823c9a6934b1e4dc2ada',

        'HOST': 'ec2-52-23-45-36.compute-1.amazonaws.com',

        'PORT': '5432',

    }
      
}

# DATABASE_URL= "postgres://obyidxalwosihe:20261adbae0585b0bfe99a6da4e1b13203f63bfe1f33da62a05a446a22022851@ec2-34-195-233-155.compute-1.amazonaws.com:5432/d84157ac50tjvp"
# DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CRISPY_TEMPLATE_PACK = 'bootstrap4'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pc4puzzle@gmail.com'
EMAIL_HOST_PASSWORD = "modernacademy4"
EMAIL_USE_TLS = True
EMAIL_USE_SSL= False
EMAIL_PORT = '587'
#messgaes Error
from django.contrib.messages import constants as messages        
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}  
# ICONS={
#     "gammer":"ri-gamepad-fill",
#     "engineer":"ri-compasses-2-line",
#     "programmer":"ri-code-box-line",
#     "designer":"ri-paint-brush-line",                    
#     "normal":"ri-database-2-line",
# }
#allauth 

SITE_ID=1
LOGIN_REDIRECT_URL ="/"
ACCOUNT_ADAPTER="allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL =True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_CONFIRMATION_HMAC =True
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX ="Site"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN =60
ACCOUNT_EMAIL_MAX_LENGTH=245
ACCOUNT_MAX_EMAIL_ADDRESSES=1
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =120
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =True
ACCOUNT_LOGIN_ON_PASSWORD_RESET =True
ACCOUNT_LOGOUT_REDIRECT_URL ="/"
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =True
ACCOUNT_SESSION_REMEMBER =None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =True
ACCOUNT_SIGNUP_REDIRECT_URL =LOGIN_REDIRECT_URL
# ACCOUNT_USERNAME_BLACKLIST 
ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_USERNAME_MIN_LENGTH =1
ACCOUNT_USERNAME_REQUIRED =True
SOCIALACCOUNT_AUTO_SIGNUP =True
SOCIALACCOUNT_EMAIL_VERIFICATION =ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_QUERY_EMAIL =ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS =True
# ACCOUNT_FORMS = {'login': 'shop.forms.MyCustomLoginForm'} 

      
AUTHENTICATION_BACKENDS = [
    # ............
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    #      ...
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id':"197694307706-9e3rcck292io9fa55fnsvjlrlvd0m7n7.apps.googleusercontent.com",
            'secret':"0zrFyl4JbA_Uv7r5Ue04_OOD",
            'key': ''
        }
    },

    'facebook': {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'APP': {
        'client_id':"960016038152712",
        'secret':"8b10857d04de0f6c162db27be1fa097c",
        'key': '',
       
    }
}
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT=  BASE_DIR/"static"

STATICFILES_DIRS=[
    BASE_DIR/"static_in_env"
] 

MEDIA_URL="/media/"

MEDIA_ROOT= BASE_DIR/"media"

STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

django_heroku.settings(locals())

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "auto",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "en-EN",  # To force a specific language instead of the Django current language.
}
# TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True
# TINYMCE_EXTRA_MEDIA = {
#     'css': {  
#         'all': [
#             ...
#         ],
#     },
#     'js': [
#         ...
#     ],
# }
