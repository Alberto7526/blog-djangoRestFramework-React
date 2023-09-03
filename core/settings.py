from pathlib import Path
import os 
import environ


# creamos la variable de entorno para leer nuestos datos del archivo env
env = environ.Env()
environ.Env.read_env()
Enviroment = env

# configuraciones basicas 
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY') ## leemos la clave secreta
SITE_NAME = "MiSitio"
DEBUG = True

# Acá podemos colcoar los sitios que pueden acceder a mi sitio (en producción)
if not DEBUG:
    ALLOWED_HOSTS = [
    "www.midominio",
    ".solopython.com"
    ]
else:
    ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1"
    ]
    
# Esto es para desplegar el proyecto 
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# para las aplicaciones django lee la lista INSTALLED_APPS por tanto la vamor a armar de 3 listas 

# 1. listas por defecto que trae django 

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 2. Las apps que nosotros hagamos en nuestro proyecto las agregamos en la siguiente lista 

PROJECT_APPS = [
    
]

# 2. Aplicaciones de terceros instaladas

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'ckeditor',
    'ckeditor_uploader'
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# luego configuramos ckeditor para crear blogs 

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'autoParagraph': False
    }
}
CKEDITOR_UPLOAD_PATH = "/media/"


# configuramos los middleware 
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # permite que una url acceda a la inrmación de nuestra  api
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Gestiona los archivos estaticos de nuestra web
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# configuramos la conexión con React en la clave DIRS  para indicar a django donde estan mis templates 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'dist')],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# esta part3e me permite controlar quienes hacen request a nuestra base de datos
CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173',
    'http://localhost:8000',
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:8000',
]

if not DEBUG:
    CORS_ORIGIN_WHITELIST = [
        'https://solopython.com',
        'https://admin.solopython.com',
        'https://blog.solopython.com',
    ]

    CSRF_TRUSTED_ORIGINS = [
        'hhttps://solopython.com',
        'https://admin.solopython.com',
        'https://blog.solopython.com',
    ]

# protección adicional a la base de datos
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# archivos estaticos 

STATIC_ROOT = os.path.join(BASE_DIR, 'static') # ejecutamos el comando python manage.py collectstatic para crear la carpeta static
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# configuramos la ruta de medias 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# configuramos la ruta que apunta a react 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'dist/assets')
]
 
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ahora configuramos nuestro django rest framework 

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny' # cualquier permina sin permisos desde nuestro dominio puede acceder a nuestra api
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination', # la paginación de nuestro sitio
    'PAGE_SIZE': 16,
}

# agregamos nuestro token de autentuicación

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


FILE_UPLOAD_PERMISSIONS = 0o640

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

if not DEBUG:
    DEFAULT_FROM_EMAIL="Uridium <mail@uridium.network>"
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS')

    
    # django-ckeditor will not work with S3 through django-storages without this line in settings.py
    AWS_QUERYSTRING_AUTH = False

    # aws settings
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')


    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'

    # s3 static settings

    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # s3 public media settings

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'core.storage_backends.MediaStore'
    
    # creamos en el core el archivo storage_backends.py para que aws se conecte con django correctamente 


