DEBUG = True
SESSION_COKKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{host}:23306/{db_name}?charset=utf8'.format(**{
    'user': 'sksk_ko',
    'password': 'Ka83hH36',
    'host': '127.0.0.1',
    'db_name': 'sksk_ko'
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True

SECRET_KEY = 'e3f5564f36d0600cc0052d36349bc341e3759c1ed160dc2b59cd4ce8aa0e3d0d'

NAVER_CLIENT_ID = 'PRonhkoW4skaj4NunmCs'
NAVER_CLIENT_SECRET = 'Remr92Eg4L'