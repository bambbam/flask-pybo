import os

Base_Dir = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(Base_Dir,"pybo.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev"