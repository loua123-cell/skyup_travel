"""
Paramètres Django pour le projet skyup_travel.

Généré par 'django-admin startproject' utilisant Django 6.0.1.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Construction des chemins à l'intérieur du projet (BASE_DIR / 'sous-dossier')
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURATION DE SÉCURITÉ ---

# ATTENTION : gardez la clé secrète utilisée en production confidentielle !
SECRET_KEY = 'django-insecure-h0f)6t+(0_aegn^+)dpzdg((os-zy-_tet&s5@k*be%$0)&y9y'

# ATTENTION : ne pas activer le mode debug en production !
DEBUG = True

ALLOWED_HOSTS = []

# --- DÉFINITION DES APPLICATIONS ---

INSTALLED_APPS = [
    # Applications par défaut de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications locales du projet
    'users',
    'flights',
    'hotels',
    'cars',
    'bookings',
    'core',
    'tours',

]

# Modèle d'utilisateur personnalisé
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Indispensable pour la traduction
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skyup_travel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Chemin vers les templates globaux
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n', # Pour gérer les langues dans les templates
            ],
        },
    },
]

WSGI_APPLICATION = 'skyup_travel.wsgi.application'

# --- BASE DE DONNÉES ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- VALIDATION DES MOTS DE PASSE ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALISATION (i18n) ---

LANGUAGE_CODE = 'fr' # Langue par défaut

TIME_ZONE = 'Africa/Tunis'

USE_I18N = True
USE_TZ = True

# Chemins vers les fichiers de traduction (.po / .mo)
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Langues disponibles dans l'interface
LANGUAGES = [
    ('ar', _('Arabe')),
    ('en', _('Anglais')),
    ('fr', _('Français')),
]

# --- FICHIERS STATIQUES ET MÉDIAS ---

# Configuration CSS, JavaScript et Images de design
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Configuration des fichiers téléchargés par les utilisateurs
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- PARAMÈTRES DE CONNEXION ET SÉCURITÉ ---

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

# Type de champ de clé primaire par défaut pour Django 6.0
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'