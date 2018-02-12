from envparse import env
import os

HOST = env.str('HOST', default='0.0.0.0')

PORT = env.int('PORT', default=8080)

DEBUG = env.bool('DEBUG', default=True)

MONGO_HOST = env.str('MONGODB_HOST', default='127.0.0.1')

MONGO_PORT = env.int('MONGODB_PORT', default=27017)

MONGO_URI = env.str(
    'MONGODB_URI',
    default='mongodb://%s:%d' % (MONGO_HOST, MONGO_PORT)
)

BASE_DIR = os.path.dirname(__file__)

FIXTURE_DIR_NAME = 'tools'

FIXTURES_PATH = os.path.join(BASE_DIR, FIXTURE_DIR_NAME)

CLEAR_DB = env.bool('CLEAR_DB', default=True)

