import os
#from decouple import config
from django.urls import reverse_lazy

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Cookie name. This can be whatever you want. 
SESSION_COOKIE_NAME = 'sessionid' 
# The module to store sessions data. 
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
# Age of cookie, in seconds (default: 36 days = 1 year). 
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365
# Whether a user's session cookie expires when the Web browser is closed 
SESSION_EXPIRE_AT_BROWSER_CLOSE = False 
# Whether the session cookie should be secure (https:// only). 
SESSION_COOKIE_SECURE = False 


# Application definition

INSTALLED_APPS = [
    'home',
    #'search',
    #'wagtail_localize',	# Cap 55 of Kalob  DELETE
    #'wagtail_localize.locales',	# Cap 55 of Kalob  DELETE
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.sitemaps',
    'wagtail.contrib.search_promotions', # NEW
    'wagtail.contrib.table_block', # NEW
    'wagtail.contrib.legacy.richtext', # NEW
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2', # Cap-34

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_comments_xtd',
    'django_comments',
# 3rd Parts Apps
    'django_countries',
    'crispy_forms',	# DELETE
    'ckeditor',
    'wagtailfontawesome',
    'rest_framework', # Cap-34
    'rest_framework.authtoken',
    # 'captcha',
    # 'wagtailcaptcha',
# allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.github',
# MINE
    'core.streams',
    'core.blog',
    'core.menus',
    'core.footer',
    'core.contact',
    'core.store',
    'core.site_settings',
    #'core.carousels',
    'core.users',
    'core.newsletter',
    'qrcoder',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Always after Session & Before of Common (COMMENT THIS IF YOU HAVE INSTALLED WAGTAIL-TRANS)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1 # from 'allauth'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Provider specific settings from django-allauth


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    'bmp': 'jpeg',
    'webp': 'webp',
}

WAGTAILIMAGES_FEATURE_DETECTION_ENABLE = True   #Once OpenCV installed
WAGTAILIMAGES_JPEG_QUALITY = 100
WAGTAILIMAGES_WEBP_QUALITY = 100

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WAGTAIL_I18N_ENABLED = True # Cap 55 Kalob. Works changing languages

'''
LANGUAGES = [
    ('en', "English"),
    ('fr', "Français"),
    ('es', "Español"),
    ('de', "Deutsch"),
    ('nl', "Nederlands"),
    ('pt', "Portuguese"),
]
'''
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', "English"),
    ('fr', "Français"),
    ('es', "Español"),
    ('de', "Deutsch"),
    ('nl', "Nederlands"),
    ('pt', "Portuguese"),
]

LOCALE_PATH = (os.path.join(BASE_DIR, 'locale'),)

WAGTAILEMBEDS_RESPONSIVE_HTML = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

WAGTAIL_SITE_NAME = ""


# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# Recaptcha settings
# This key only allows localhost. For production, you'll want your own API keys.
# You can get Recaptcha API key from google.com/recaptcha
RECAPTCHA_PUBLIC_KEY = "6LcNrZcUAAAAAADyWEJTIOXKr6x-8POg3Iqp8rEM"
RECAPTCHA_PRIVATE_KEY = "6LcNrZcUAAAAAPISF06kecWBC4EJPXy2uo_penMC"
NOCAPTCHA = True


# This following, are both from codemy.com, single blog, cap 9

LOGOUT_REDIRECT_URL = '/'

# following works together with login_required()
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
ACCOUNT_AUTHENTICATION_METHOD = "username_email" # "username" | "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = settings.LOGIN_URL #The URL to redirect to after a successful e-mail confirmation, in case no user is logged in
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 # The email confirmation expires in 3 day
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False
ACCOUNT_EMAIL_REQUIRED = True # The user is required to hand over an e-mail address when signing up
ACCOUNT_EMAIL_VERIFICATION = "none" #"mandatory", "optional", or "none" Determines the e-mail verification method during signup
#ACCOUNT_EMAIL_SUBJECT_PREFIX = Site This is default
#ACCOUNT_DEFAULT_HTTP_PROTOCOL = http
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 300 # (in sec, 5 min) You need to disable HMAC
ACCOUNT_EMAIL_MAX_LENGTH = 254
ACCOUNT_MAX_EMAIL_ADDRESSES = 5 #The maximum amount of email addresses a user can associate to his account.
#ACCOUNT_FORMS = {}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = None # Set it to None to ask "Remember me?" Could be None, True, or False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
#ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login'
ACCOUNT_USERNAME_BLACKLIST = ["admin", "god", "django", "wagtail", "python", "from", "select", "*",]
ACCOUNT_UNIQUE_EMAIL = True
#ACCOUNT_USER_DISPLAY = user.username   # (Default)
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_USERNAME_REQUIRED = True
#==========================      Default behaviors      ==================#
SOCIALACCOUNT_ADAPTER = "allauth.socialaccount.adapter.DefaultSocialAccountAdapter" 
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
'''
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        # For each provider, you can choose whether or not the
        # email address(es) retrieved from the provider are to be
        # interpreted as verified.
        "VERIFIED_EMAIL": True
    },
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": "123",
            "secret": "456",
            "key": ""
        },
        # These are provider-specific settings that can only be
        # listed here:
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },
    "linkedin": {
        "SCOPE": [
            "r_basicprofile",
            "r_emailaddress"
        ],
        "PROFILE_FIELDS": [
            "id",
            "first-name",
            "last-name",
            "email-address",
            "picture-url",
            "public-profile-url"
        ]
    }
}
'''


#=============================== from django-comments-xtd Library ==================================#
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_SALT = (b"First Line. "
                    b"Second Line.")
COMMENT_XTD_MODEL = 'blog.models.CustomComment'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2 
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order') 
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'blog.blogsinglepage': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
    }
}
'''
COMMENTS_XTD_FROM_EMAIL = 'yoursite@email.com'
COMMENTS_XTD_CONTACT_EMAIL = 'yoursite@email.com'
'''
#=====================================================================================================#


# Disabling auto update signal handlers for a search backend/whole site
AUTO_UPDATE = False

# Wagtail also provides a command for rebuilding the index from scratch.
# ./manage.py update_index

# Wagtail email notifications from address
# WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

# Wagtail email notification format
WAGTAILADMIN_NOTIFICATION_USE_HTML = True


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/stable/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Uncomment this line to enable template caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, 'cache')
    }
}

AUTH_USER_MODEL = 'users.User'

# For Django-Rest-Framework authentification Tokens (Check it):
# from CodingWithMitch Cap .7

REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': [
#        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
#    ],
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.IsAuthenticated', # See it at CodingWithMitch Cap .8
#    ],

#    'DEFAULT_AUTHENTICATION':[  # From SuperCoders
#        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#    ],
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.AllowAny',
#        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1,
}

# ckeditors configuration
CKEDITOR_CONFIG = {
    'default':{
        'toolbar':'full',
        # 'height': 300,
        # 'width': 300,
    },
}

#######################################     Obviar en (pre) #########################

# Newsletter app tutorial Cap 27
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#############################################
#############################################
#############################################
ROOT_URLCONF = 'lux.urls'
WSGI_APPLICATION = 'lux.wsgi.application'



###############################################     dev.py     ##############################
from .base import *


STRIPE_SECRET_KEY = 'kjnnkjnfsksdgjk'
STRIPE_PUBLIC_KEY = 'kjnnkjnfsncvbgjk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q=-bn^ow0)d2_w$$y=pm(2&(p%az99yv-2s7nv#uh$0369o%he'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    #'debug_toolbar',
    'django_extensions',
    'wagtail.contrib.styleguide',
]

MIDDLEWARE = MIDDLEWARE + [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Django-Debug-Toolbar
#INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")


try:
    from .local import *
except ImportError:
    pass
#############################################   production.py   #####################
from .base import *
from core.site_settings.models import GoogleScripts

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = [config('IP_HOST'), config('HOST_NAME')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('YOUR_DB_NAME'),
        'USER':config('YOUR_DB_USERNAME'),
        'PASSWORD':config('YOUR_DB_PASSWORD'),
        'HOST':config('YOUR_DB_HOST'),
        'PORT':config('YOUR_HOST_PORT')
    }
}




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# To recovering password and send emails:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #'django.core.mail.backends.filebased.EmailBackend'
EMAIL_HOST_USER = GoogleScripts.gmail_user_account
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_PASSWORD = GoogleScripts.gmail_password


STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

try:
    from .local import *
except ImportError:
    pass
