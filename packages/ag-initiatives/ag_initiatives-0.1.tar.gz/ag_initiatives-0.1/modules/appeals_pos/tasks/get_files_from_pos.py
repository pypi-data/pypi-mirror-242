from celery import shared_task

from modules.appeals_pos.services.smev.pos_smev_service import PosSmevService


@shared_task
def get_files_from_pos(files_pos_ids: list):
    PosSmevService().get_files_from_pos(files_pos_ids)
