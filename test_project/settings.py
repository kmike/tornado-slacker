# Django settings for test project.
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
join = lambda p: os.path.abspath(os.path.join(PROJECT_ROOT, p))

sys.path.insert(0, join('..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join('db.sqlite'),

        # :memory: databases cause obscure bugs in multithreaded environment
        # and django uses :memory: as TEST_NAME by default so it is necessary
        # to make test database real file.
        'TEST_NAME': join('db-test.sqlite'),
    }
}

SECRET_KEY = '5mcs97ar-(nnxhfkx0%^+0^sr!e(ax=x$2-!8dqy25ff-l1*a='
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    join('templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS=(
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'testapp',
)
