class SignalsEventType:
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PUBLISH = "PUBLISH"
    UNPUBLISH = "UNPUBLISH"

    RESOLVER = {
        CREATE: "Добавление",
        UPDATE: "Обновление",
        DELETE: "Удаление",
        PUBLISH: "Публикация",
        UNPUBLISH: "Снятие с публикации",
    }

    CHOICES = RESOLVER.items()
