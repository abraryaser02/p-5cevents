# services/backend/project/config.py


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")

class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
