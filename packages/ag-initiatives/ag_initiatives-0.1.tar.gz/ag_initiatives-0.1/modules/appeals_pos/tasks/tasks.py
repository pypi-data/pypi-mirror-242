import requests
from celery import shared_task
from django.db.models import Subquery, OuterRef, Q
from django.utils import timezone
from sentry_sdk import capture_exception
from config.settings.celery import app
from modules.appeals_pos.models import Appeal, Settings, SmevLog
from modules.appeals_pos.models.appeal import SmevState, AppealState
from modules.appeals_pos.models.file import File
from modules.appeals_pos.services.smev.pos_smev_client import PosSmevHttpClient
from modules.appeals_pos.services.smev.pos_smev_service import PosSmevService
from modules.appeals_pos.services.smev.smev_response_handler import SmevResponseHandler

service = PosSmevService()


@shared_task
def process_appeal(appeal_id):
    appeal = Appeal.objects.get(pk=appeal_id)

    success = True
    smev_response = None
    try:
        smev_response = service.add_appeal(appeal)
        answer_json = SmevResponseHandler(smev_response).handle_response()
    except Exception as err:
        capture_exception(err)
        success = False
        appeal.smev_status = SmevState.SMEV_ERR
        answer_json = f"Произошла необработанная ошибка: {err}"
    else:
        appeal.smev_status = SmevState.WAITING_RESPONSE
    finally:
        appeal.save()
        SmevLog.objects.create(
            description=f'Ответ на отправку обращения id={appeal.id}',
            xml_data=smev_response.text if smev_response else None
        )

    return {"success": success, "data": answer_json}


@app.task(name="modules.appeals_pos.tasks.send_appeals_task")
def send_appeals_task():
    files_without_pos_id = Subquery(
        File.objects.filter(
            pos_id__isnull=True,
            appeals=OuterRef('pk'),
        ).values_list('appeals', flat=True)
    )
    appeals = Appeal.objects.filter(
        ~Q(pk__in=files_without_pos_id),
        smev_status=SmevState.PREPARING,
    )

    for appeal in appeals:
        process_appeal.delay(appeal.pk)


@app.task(name="modules.appeals_pos.tasks.send_file_task")
def send_file_task():
    success = True
    files = File.objects.filter(
        send_to_pos=False,
        appeals__isnull=False,
    ).distinct()

    if not files:
        return {"success": success, "data": None}

    smev_response = None
    try:
        files = service.send_files(files)
        smev_response = service.send_files_to_pos(files)
        answer_json = SmevResponseHandler(smev_response).handle_response()
    except Exception as err:
        capture_exception(err)
        success = False
        for file in files:
            file.appeals.update(smev_status=SmevState.SMEV_ERR)
        answer_json = f"Произошла необработанная ошибка: {err}"
    finally:
        files.update(send_to_pos=True)
        SmevLog.objects.create(
            description=f'Отправка файлов id={list(files.values_list("id", flat=True))}',
            xml_data=smev_response.text if smev_response else None
        )
    return {"success": success, "data": answer_json}


@shared_task
def process_update_appeal(appeal_id):
    appeal = Appeal.objects.get(pk=appeal_id)
    success = True
    smev_response = None
    try:
        smev_response = service.update_appeal(appeal)
        answer_json = SmevResponseHandler(smev_response).handle_response()
    except Exception as err:
        capture_exception(err)
        success = False
        answer_json = f"Произошла необработанная ошибка: {err}"
    finally:
        if smev_response:
            SmevLog.objects.create(
                description=f'Обновление заявки id={appeal.id}',
                xml_data=smev_response.text
            )
    return {"success": success, "data": answer_json}


@app.task(name="modules.appeals_pos.tasks.update_pos_info")
def update_pos_info():
    # settings: Settings = Settings.load()
    # if settings.update_time.replace(second=0, microsecond=0) != timezone.datetime \
    #         .now().time().replace(second=0, microsecond=0):
    #     return

    appeals = Appeal.objects.exclude(
        status__in=(AppealState.MODERATION_REJECTED, AppealState.RESPONDED),
    ).filter(pos_id__isnull=False)
    for appeal in appeals:
        process_update_appeal.delay(appeal.pk)


@app.task(name="modules.appeals_pos.tasks.get_response_from_queue_task")
def get_response_from_queue_task():
    success = True

    try:
        smev_response = PosSmevHttpClient().get_response_from_queue()
    except requests.exceptions.ConnectionError as err:
        return {"success": False, "data": str(err)}

    # если нужно будет заменить ответ на ответ из файла
    # with open('modules/appeals_pos/smev-answers-examples/pos-create-appelal-response-2.xml', "r") as f:
    #         smev_response = f.read()
    label = "Получен ответ из очереди"
    answer_json = None
    response_handler = SmevResponseHandler(smev_response)

    try:
        answer_json = response_handler.handle_response()
    except Exception as err:
        capture_exception(err)
        success = False
        label = "Получен ответ из очереди (ошибка при обработке)"

    if not answer_json:
        return {"success": success, "data": label}

    try:
        response_handler.ask_response()
    except Exception as err:
        capture_exception(err)
        success = False
        label = "Получен ответ из очереди (ошибка при подтверждении)"

    SmevLog.objects.create(
        description=label,
        xml_data=smev_response.text
    )
    get_response_from_queue_task.delay()

    return {"success": success, "data": label}
