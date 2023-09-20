from enum import Enum


class Language(str, Enum):
    VI = 'vi'
    EN = 'en'


class ObjectNotFoundType(Enum):
    USER = 'User'
    CUSTOMER = 'Customer'
    CONFIG = 'Config'


class ImportFileType(str, Enum):
    IMPORT_CUSTOMER = 'import_customer'


class ConfigValueType(str, Enum):
    COUNTRY = 'country'
