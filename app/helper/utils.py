from datetime import datetime


def generate_unique_filename(filename: str):
    return filename.split('.')[0] + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.' + filename.split('.')[-1]
