import random
import re
import string
from datetime import datetime


def camel_to_snake_case(name: str) -> str:
    """Convert a ``CamelCase`` name to ``snake_case``."""
    name = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", name)
    return name.lower().lstrip("_")


def generate_unique_filename(filename: str):
    return filename.split('.')[0] + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.' + filename.split('.')[-1]


def random_string(len, seed=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choices(seed, k=len))


def random_password(len):
    return random_string(len, string.ascii_uppercase + string.ascii_lowercase + "1234567890" + "!@#^&*()-=?")
