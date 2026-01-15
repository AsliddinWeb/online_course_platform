from .base import *

DEBUG = False

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'http://164.92.240.184:8001',
    'http://courses.asliddin.me',
    'https://courses.asliddin.me',
]

# HTTPS
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')