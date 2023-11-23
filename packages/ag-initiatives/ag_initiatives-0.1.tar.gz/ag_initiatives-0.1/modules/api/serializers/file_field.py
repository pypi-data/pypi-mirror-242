from rest_framework import serializers


class FileField(serializers.Field):
    def to_representation(self, value):
        try:
            return serializers.FileField().to_representation(value.file)
        except IndexError:
            return None
