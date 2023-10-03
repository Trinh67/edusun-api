from enum import Enum


class Enums(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Language(str, Enum):
    VI = 'vi'
    EN = 'en'


class ObjectNotFoundType(str, Enum):
    USER = 'User'
    CUSTOMER = 'Customer'
    CONFIG = 'Config'


class ImportFileType(str, Enum):
    IMPORT_CUSTOMER = 'import_customer'


class ConfigValueType(str, Enum):
    COUNTRY = 'country'


class UserType(str, Enums):
    COLLABORATOR = 'collaborator'
    STAFF = 'staff'


class UserStatus(str, Enums):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class UserRole(str, Enums):
    SUPER_ADMIN = 'super'
    ADMIN = 'admin'


class Gender(str, Enums):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class PostStatus(str, Enums):
    DRAFT = 'draft'
    PUBLISH = 'publish'
    ARCHIVE = 'archive'
    DELETE = 'delete'


class PostType(str, Enums):
    STUDY_ABROAD = 'study_abroad'
    JOB = 'job'
    SETTLED = 'settled'
    TRAVEL_VISA = 'travel_visa'


class Currency(str, Enums):
    VND = 'VND'
    USD = 'USD'


class UploadFileType(str, Enums):
    IMAGE = 'image'
    ATTACHMENT = 'attachment'


class CandidateStatus(str, Enums):
    WAITTING = 'waitting'
    PROFILE_REVIEW = 'profile_review'
    INTERVIEW = 'interview'
    ADMISSION = 'admission'
    TRAINING = 'training'
    WORKING = 'working'

