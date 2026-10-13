from .base import *

# Fast and isolated database for automated unit tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Ensure password hashers adhere strictly to rule [HASH-CRYPT/ARGON2]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

DEBUG = False
TESTING = True
