from modules.subscriptions.services.tracking_by_subscriptions import Subscribe


class SubscribeMixin(object):
    """Миксин подписки
    Очередь использования - в начале
    """

    @Subscribe(events=["publish"])
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
