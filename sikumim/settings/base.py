"""
Django settings for sikumim project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CKEDITOR_UPLOAD_PATH = "uploads/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'website',
    'ckeditor',
    'widget_tweaks',
    'website.templatetags.website_extras',
    'adminsortable',
    # The Django sites framework is required
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Login via Google
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'debug_toolbar',
    'captcha',
)

SITE_ID = 1


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware.'
)

ROOT_URLCONF = 'sikumim.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.core.context_processors.static',
                'website.context_processors.search_form',
                'website.context_processors.subjects',
            ],
        },
    },
]

WSGI_APPLICATION = 'sikumim.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sikumia_db',
        'USER': 'david',
        'PASSWORD': 'david',
        'HOST': '',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Israel'

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

CKEDITOR_CONFIGS = {
    'default': {
         'toolbar': [[ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],
                    [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ],
                    [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
                    [ 'Image','Table','HorizontalRule','Smiley','SpecialChar','PageBreak' ],
                    [ 'Styles','Format','Font','FontSize' ],
                    [ 'TextColor','BGColor' ]],
        'contentsLangDirection': 'rtl',
        'contentsLanguage ': 'heb',
        'width': '100%',
        'extraPlugins': 'autogrow',
        'height': 500,
        'autoGrow_minHeight' : 500,
        'autoGrow_maxHeight' : 1000,
    },
}

#login
LOGIN_REDIRECT_URL = '/s'

AUTHENTICATION_BACKENDS = (
    # Default backend -- used to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = False
LOGIN_REDIRECT_URL = "/"

SOCIALACCOUNT_FORMS = {
    'signup': 'website.forms.CustomSignupForm',
}


# recaptcha

RECAPTCHA_PUBLIC_KEY = '6LczPQsTAAAAAAcdDP36MQ7THJX2cx8zdzpc7sMe'
RECAPTCHA_PRIVATE_KEY = '6LczPQsTAAAAAFrNSDfwpoQYYf_PUzOg6Z2_I45x'
NOCAPTCHA = True

# mailgun
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@sikumia.co.il'
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Sikumia Team <no-reply@sikumia.co.il>'


ADMINS = (
            ('David Griver', 'dgriver@gmail.com'),
)

MANAGERS = (
            ('David Griver', 'dgriver@gmail.com'),
)