from decouple import config

print(" ************************** ")
print(" entro al archivo app_config.py ")
print(" ************************** ")

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}