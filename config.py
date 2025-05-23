# DB설정 

import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) #DB접속 주소, 설정에 의해 SQLite DB가 사용되고,DB파일은 프로젝트 홈 디렉터리 바로밑 pybo.db파일로 저장된다.
SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy의 이벤트를 처리하는 옵션, 해당 프로젝트에는 필요하지 않음

SECRET_KEY = "dev"
