from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(8udh@l59q2t6$oaaq#c2o+r#-tgbjph)(8+d7u%)kxq%v(zys'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'gestion',
    'inventario',
    'operaciones',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'config.middleware.RestringirAccesoAdminMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

USE_L10N = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# Le decimos a Django que busque imágenes en la carpeta "static"
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# A dónde ir después de iniciar sesión con éxito
LOGIN_REDIRECT_URL = 'gestion:dashboard'

# A dónde ir después de cerrar sesión
LOGOUT_REDIRECT_URL = 'login' 

# A dónde enviar a los intrusos que intenten entrar sin sesión
LOGIN_URL = 'login'

# Duración de la sesión en segundos (86400 = 24 horas)
SESSION_COOKIE_AGE = 86400 

# Asegura que la sesión se guarde en cada petición (útil si notas que se cierra sola)
SESSION_SAVE_EVERY_REQUEST = True

# Asegura que el motor de sesiones sea el estándar de base de datos
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

#Es donde tú trabajas los archivos (el taller).
STATIC_ROOT = BASE_DIR / 'staticfiles'

#Es donde el sistema entrega los archivos al usuario (la vitrina).
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'