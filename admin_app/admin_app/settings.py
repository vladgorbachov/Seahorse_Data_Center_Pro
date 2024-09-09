import os
from admin_app.admin_app.settings_loader import load_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cu(ziv_i1!50fg-k=cvml#ip!$0m%=_6x&%65bx(4@&@x*c_zc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_app.deck',
    'admin_app.bridge',
    'admin_app.dashboard',
    'admin_app.catering',
    'admin_app.electrical',
    'admin_app.engine',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_app.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'admin_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'admin_app', 'templates'),
                 os.path.join(BASE_DIR, 'admin_app', 'dashboard'),
                 os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'deck', 'templates'),
                 os.path.join(BASE_DIR, 'bridge', 'templates'),
                 os.path.join(BASE_DIR, 'catering', 'templates'),
                 os.path.join(BASE_DIR, 'electrical', 'templates'),
                 os.path.join(BASE_DIR, 'engine', 'templates'),
                 ],
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

WSGI_APPLICATION = 'admin_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

custom_settings = load_settings()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': custom_settings['DATABASE']['NAME'],
        'USER': custom_settings['DATABASE']['USER'],
        'PASSWORD': custom_settings['DATABASE']['PASSWORD'],
        'HOST': custom_settings['DATABASE']['HOST'],
        'PORT': custom_settings['DATABASE']['PORT'],
    }
}

AUTH_USER_MODEL = 'auth.User'

LOGIN_REDIRECT_URL = '/dashboard/'

LOGIN_URL = '/login/'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'admin_app', 'static'),
    os.path.join(BASE_DIR, 'admin_app', 'deck', 'static'),
    os.path.join(BASE_DIR, 'admin_app', 'bridge', 'static'),
    os.path.join(BASE_DIR, 'admin_app', 'catering', 'static'),
    os.path.join(BASE_DIR, 'admin_app', 'electrical', 'static'),
    os.path.join(BASE_DIR, 'admin_app', 'engine', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Установите максимальный размер загружаемого файла (например, 100 МБ)
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

# Увеличьте таймаут сервера разработки Django
os.environ['DJANGO_SERVER_TIMEOUT'] = '300'  # 5 минут
