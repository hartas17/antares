from .base import *

DEBUG = False

SECRET_KEY = get_env_variable('SECRET_KEY')

EMAIL_HOST = 'smtp.production.com'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'send.email@production.com'
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
