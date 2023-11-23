import requests
from config.settings.celery import app

from modules.integration.models.external_system import ExternalSystemToken


@app.task
def send_signal_for_api(data: dict):
    external_system_urls = ExternalSystemToken.objects.values_list("url", "system_token")
    for url, system_token in external_system_urls:
        requests.post(url=url, data=data, headers={'Authorization': f'Token {system_token}'}, verify=False)


@app.task
def send_signal_about_balance(data: dict, external_ids: list):
    external_system_urls = ExternalSystemToken.objects.filter(pk__in=[external_ids]).values_list("url", "system_token")
    for url, system_token in external_system_urls:
        requests.post(url=url, data=data, headers={'Authorization': f'Token {system_token}'})
