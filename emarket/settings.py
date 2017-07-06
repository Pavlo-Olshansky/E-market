import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable!!!" % var_name
        raise ImproperlyConfigured(error_msg)

# Get ENV VARIABLES key
ENV_ROLE = get_env_variable("ENV_ROLE")

#SECURITY WARNING: don't run with debug turned on in production!
if ENV_ROLE=='development':
    DEBUG = True
    SECRET_KEY = get_env_variable('SECRET_KEY_emarket')
else:
    from decouple import config
    SECRET_KEY = config('SECRET_KEY_emarket')
    DEBUG = config('DEBUG', default=False, cast=bool)


# ALLOWED_HOSTS = ['***heroku-app-link***', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'accounts',
    'disqus',
    'products',
    'django.contrib.sites',
    'widget_tweaks',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates'), ],
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

WSGI_APPLICATION = 'emarket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if ENV_ROLE == 'development':
    DB_PASS_emarket = get_env_variable("DB_PASS_emarket")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'e_market_website_db',
            'USER': 'postgres',
            'PASSWORD': DB_PASS_emarket,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    from decouple import config
    import dj_database_url
    DATABASES = {
    'default': dj_database_url.config(
        
        )
    }



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'accounts/login'
LOGOUT_URL = 'accounts/logout'
LOGIN_REDIRECT_URL = '/accounts/profile'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



if ENV_ROLE=='development':

    DISQUS_API_KEY = get_env_variable("DISQUS_API_KEY")

    GMAIL_PASS = get_env_variable("GMAIL_PASS")
    GMAIL_MAIL = get_env_variable("GMAIL_MAIL")
else:
    from decouple import config
    DISQUS_API_KEY = config("DISQUS_API_KEY")

    GMAIL_PASS = config("GMAIL_PASS")
    GMAIL_MAIL = config("GMAIL_MAIL")

DISQUS_WEBSITE_SHORTNAME = 'buyandplay'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = GMAIL_MAIL
EMAIL_HOST_PASSWORD = GMAIL_PASS
 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

