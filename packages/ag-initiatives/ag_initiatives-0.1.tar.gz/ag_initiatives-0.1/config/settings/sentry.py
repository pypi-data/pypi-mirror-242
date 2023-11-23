import os
from datetime import timedelta
from random import random

import sentry_sdk
from dateutil import parser
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration


def before_send(event, hint):
    """
    Защита данных,
    например при попытке отправить пароль он заменится на [Hidden]
    """
    for exception in event.get("exception", {}).get("values", []):
        for frame in exception.get("stacktrace", {}).get("frames", []):
            args = frame.get("vars", {}).get("args", {})
            if isinstance(args, dict):
                for key in args.keys():
                    if "sensitive" in key:
                        frame["vars"]["args"][key] = "[Hidden]"
    if "user" in event:
        # Проверяем, есть ли токен пользователя в информации о пользователе
        if "token" in event["user"]:
            # Заменяем токен на значение "[Hidden]"
            event["user"]["token"] = "[Hidden]"
    if "request" in event:
        # Проверяем, есть ли токен пользователя в информации о пользователе
        if "headers" in event["request"]:
            if "Authorization" in event["request"]["headers"]:
                event["request"]["headers"]["Authorization"] = "[Hidden]"
            if "Cookie" in event["request"]["headers"]:
                event["request"]["headers"]["Cookie"] = "[Hidden]"
    return event


def before_send_transaction(event, hint):
    url_string = event.get("request", {}).get("url")
    if url_string and "decide" in url_string:
        DECIDE_SAMPLE_RATE = 0.00001  # 0.001%
        should_sample = random() < DECIDE_SAMPLE_RATE

        transaction_start_time = event.get("start_timestamp")
        transaction_end_time = event.get("timestamp")
        if transaction_start_time and transaction_end_time:
            try:
                parsed_start_time = parser.parse(transaction_start_time)
                parsed_end_time = parser.parse(transaction_end_time)

                duration = parsed_end_time - parsed_start_time

                if duration >= timedelta(seconds=8):
                    # возвращает все события для транзакций, которые заняли более 8 секунд
                    return event
                elif duration > timedelta(seconds=2):
                    # очень высокая частота дискретизации для транзакций, которые заняли более 2 секунд
                    return event if random() < 0.5 else None

            except Exception:
                return event if should_sample else None

        return event if should_sample else None
    else:
        return event


def sentry_init() -> None:
    sentry_sdk.utils.MAX_STRING_LENGTH = 10_000_000
    sentry_sdk.init(
        send_default_pii=True,
        dsn=os.environ.get("GLITCH_TIP_DSN"),
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
            LoggingIntegration(event_level=None),
        ],
        sample_rate=1.0,
        traces_sample_rate=1.0,
        before_send=before_send,
        before_send_transaction=before_send_transaction,
    )


if os.environ.get("GLITCH_TIP_DSN"):
    sentry_init()
