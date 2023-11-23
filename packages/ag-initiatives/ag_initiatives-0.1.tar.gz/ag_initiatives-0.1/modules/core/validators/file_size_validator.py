from django.core.exceptions import ValidationError


class FileSizeValidator(object):
    def __init__(self, limit_size):
        self.limit_size = limit_size

    def __call__(self, value):
        if self.limit_size is not None and value.size > self.limit_size:
            raise ValidationError(f'Файл превышает допустимый размер ({self.limit_size})')