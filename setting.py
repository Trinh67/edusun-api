import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)


class Setting(BaseSettings):
    ROOT_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__)
    ))

    SLOW_SQL_THRESHOLD_MS: int = os.getenv('SLOW_SQL_THRESHOLD', 10000)
    ENV: str = os.getenv('ENV', 'local')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    PROJECT_TITLE: str = 'EduSun Service'
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Jaeger
    JAEGER_ENABLED: int = os.getenv('JAEGER_ENABLED', 0)
    JAEGER_AGENT_HOST: str = os.getenv('JAEGER_HOST', "localhost")
    JAEGER_AGENT_PORT: int = os.getenv('JAEGER_PORT', 6831)
    JAEGER_SAMPLING_RATE: float = os.getenv('JAEGER_SAMPLING_RATE', 1 / 2)

    DEFAULT_MAX_UPLOAD_IMPORT_SIZE: int = os.getenv('DEFAULT_MAX_UPLOAD_IMPORT_SIZE', 10)
    DATA_STORAGE: str = os.getenv('DATA_STORAGE', '')

    @property
    def is_testing(self):
        return self.ENV == 'test'


setting = Setting()
