#환경변수 모아두는 곳(서버환경)

from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x8d\xc6\xa8\r\xcf\xeeR\xba}\x00k\x98\xbe\xd6K8'