import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SESSION_TYPE = 'filesystem'

config = Config()
