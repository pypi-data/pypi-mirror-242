import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from modules.appeals_pos.models import Appeal
from modules.appeals_pos.models.subcategory import Subcategory
from modules.appeals_pos.serializers import AppealWriteSerializer


@pytest.mark.django_db
def test_appeal_write_serializer():
    # Создаем пользователя и подкатегорию для теста
    user = User.objects.create(username="testuser")
    subcategory = Subcategory.objects.create(name="Test Subcategory")

    # Подготовим данные для сериализации
    data = {
        "text": "Test appeal",
        "subcategory_id": subcategory.id,
        "coordinates": {"latitude": 42.123, "longitude": 23.456},
        "address": "Test address",
        "files": [1, 2, 3],
        "to_publish": True,
    }

    # Создаем экземпляр сериализатора
    serializer = AppealWriteSerializer(data=data, context={"user": user})

    # Проверяем, что данные проходят валидацию
    assert serializer.is_valid()

    # Создаем обращение
    appeal = serializer.save()

    # Проверяем, что обращение было успешно создано
    assert Appeal.objects.filter(id=appeal.id).exists()

    # Попробуем создать обращение с несуществующей подкатегорией
    data["subcategory_id"] = 999  # ID, которого точно нет в базе
    serializer = AppealWriteSerializer(data=data, context={"user": user})

    # Проверяем, что валидация выдает ValidationError
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    # Попробуем создать обращение с неправильными координатами
    data["coordinates"] = {"invalid_key": "invalid_value"}
    serializer = AppealWriteSerializer(data=data, context={"user": user})

    # Проверяем, что валидация выдает ValidationError
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)