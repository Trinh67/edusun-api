import re

from pydantic import BaseModel

from app.config.field_name_mapping import data_mapping
from app.helper.enum import Language, ObjectNotFoundType
from starlette_context import context

from setting import setting


def get_accept_language() -> str:
    try:
        languages = context.data.get("lang", "").split(",")
        for language in languages:
            lang = language.split(";")[0].strip()
            if lang[:2] in [Language.VI.value, Language.EN.value]:
                return lang[:2]
        return Language.EN.value
    except Exception:
        return Language.EN.value


def translate_message(code: str, params: [str] = []) -> str:
    lang = get_accept_language()
    if data_mapping[lang].get(code):
        text = data_mapping[lang][code]
        pattern = re.compile('{{[a-zA-Z0-9_-]*}}')
        for param in params:
            if data_mapping[lang].get(param):
                text = pattern.sub(data_mapping[lang][param], text, 1)
            else:
                text = pattern.sub(param, text, 1)
        return text
    return code


class CommonException(Exception):
    http_code: int
    code: int
    message: str

    def __init__(self, http_code: int = None, code: int = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else self.http_code
        self.message = message

    def __str__(self):
        return str(self.message)

    def __iter__(self):
        yield from (self.code, self.message)


class RequiredFile(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=402,
                         message="RequiredFile")


class NotSupportFileType(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=415,
                         message="NotSupportFileType")


class FileTooLarge(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=413,
                         message="FileTooLarge")


class FileEmpty(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=413,
                         message="FileEmpty")


class InvalidFileFormat(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=413,
                         message="InvalidFileFormat")


class ObjectNotFound(CommonException):
    def __init__(self, obj: ObjectNotFoundType):
        super().__init__(http_code=400, code=404,
                         message=f"Object {obj} Not Found")


class ExistedFile(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=404,
                         message="ExistedFile")


class FieldIsRequired(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=402,
                         message=f"Required Field {field_name}")


class InvalidJson(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=400, message="InvalidJson")


class InvalidField(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=406,
                         message="InvalidField")


class InvalidFieldFormat(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=407,
                         message="InvalidFieldFormat")


class InvalidMinLength(CommonException):
    def __init__(self, field_name: str, limit: int):
        super().__init__(http_code=400, code=412,
                         message="InvalidMinLength")


class InvalidMaxLength(CommonException):
    def __init__(self, field_name: str, limit: int):
        super().__init__(http_code=400, code=413,
                         message=f"Invalid {field_name} Max Length {limit}")


class InvalidMinValue(CommonException):
    def __init__(self, field_name: str, limit: int):
        super().__init__(http_code=400, code=410,
                         message=f"Invalid {field_name} Min Value {limit}")


class InvalidMaxValue(CommonException):
    def __init__(self, field_name: str, limit: int):
        super().__init__(http_code=400, code=411,
                         message=f"Invalid {field_name} Max Value {limit}")


class ExistedObject(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=408,
                         message=f"Existed {field_name}")


class InternalServerError(CommonException):
    def __init__(self):
        super().__init__(http_code=500, code=500,
                         message="ServerError")


def request_get_message_validation(exc) -> (int, object):
    # print(json.dumps(exc.errors(), indent=2))
    types = [error.get('type') for error in exc.errors()]
    messages = [error.get("loc")[len(error.get("loc")) - 1] for error in exc.errors()]
    limit_value = [error.get('ctx').get('limit_value') if error.get('ctx') else '' for error in exc.errors()]
    for err_type, field, limit in zip(types, messages, limit_value):
        if err_type == "value_error.missing":
            return FieldIsRequired(field)
        elif err_type == "value_error.jsondecode":
            return InvalidJson()
        elif err_type == "value_error.number.not_le" or err_type == "value_error.number.not_lt":
            return InvalidMinValue(field, limit)
        elif err_type == "value_error.number.not_ge" or err_type == "value_error.number.not_gt":
            return InvalidMaxValue(field, limit)
        elif err_type in ["type_error.number", "type_error.str", "type_error.string", "type_error.list",
                          "type_error.integer",
                          "type_error.bool", "value_error.invalid_field_format"]:
            return InvalidFieldFormat
        elif err_type == "value_error.any_str.min_length":
            return InvalidMinLength(field, limit)
        elif err_type == "value_error.any_str.max_length":
            return InvalidMaxLength(field, limit)
        else:
            return InvalidField(field)
