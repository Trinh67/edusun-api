import re
from datetime import datetime

from unidecode import unidecode


def generate_unique_filename(filename: str):
    return filename.split('.')[0] + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.' + filename.split('.')[-1]


def is_phone_number_valid(phone_number: str):
    if not phone_number:
        return False

    is_valid_format = bool(re.match(pattern='^(0|84)?[0-9]{9}$', string=phone_number))
    if is_valid_format:
        try:
            normalize_phone_number(phone_number, raise_error=True)
            return True
        except Exception:
            return False
    return False


def normalize_phone_number(phone_number, prefix='84', raise_error=True):
    """
    Convert all format phone number to prefix+xxx
    :param raise_error:
    :param str phone_number:
    :param str prefix:
    :return:
    """
    # phone = re.search('^(\+84|84|0084|0)(?P<phone>\d{9}$)', phone_number.strip())
    if phone_number:
        phone = ''.join([c for c in phone_number if c.isdigit()])
        if len(phone) >= 9:
            head = phone[:-9]
            tail = phone[-9:]
            if head in ['84', '0084', '0', '']:
                if tail[0] in '35789':
                    return prefix + tail
    if raise_error:
        raise Exception(f'Have phone number invalid format: `{phone_number}`')
    return phone_number


def is_valid_email(email: str) -> bool:
    if not email:
        return False

    email = str(email)
    if email != unidecode(email):
        return False

    pattern = re.compile("^\w+(\.\w+)*@.+\.[a-zA-Z]{2,}$")
    return bool(re.match(pattern, email))
