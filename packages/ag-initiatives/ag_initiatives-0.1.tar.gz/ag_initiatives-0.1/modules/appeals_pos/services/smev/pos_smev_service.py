import logging
from pathlib import Path
from typing import Iterable

from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException

from config.settings import BASE_DIR
from modules.appeals_pos.models import Appeal, SmevLog
from modules.appeals_pos.models.file import File
from modules.appeals_pos.services.smev.dto import pos_requests
from modules.appeals_pos.services.smev.pos_smev_client import PosSmevHttpClient

logger = logging.getLogger("POS service")


class TemplatePath:
    CREATE_APPEAL_REQUEST = str(
        Path(BASE_DIR) / "modules" / "appeals_pos" / "xml_templates" / "CreateAppealRequest.xml")
    GET_APPEAL_REQUEST = str(Path(BASE_DIR) / "modules" / "appeals_pos" / "xml_templates" / "GetAppealRequest.xml")
    FILE_UPLOAD_REQUEST = str(Path(BASE_DIR) / "modules" / "appeals_pos" / "xml_templates" / "FileUploadRequest.xml")
    FILE_DOWNLOAD_REQUEST = str(Path(BASE_DIR) / "modules" / "appeals_pos" / "xml_templates" / "FileDownloadRequest.xml")

class PosSmevService:
    """
    Класс, предоставляющий простой интерфейс для работы с интеграцией ПОС.
    Возвращает удобные для работы структуры данных
    """

    http_client = PosSmevHttpClient()

    def add_appeal(
            self, appeal: Appeal
    ):
        files_ids = appeal.files.filter(pos_id__isnull=False).values_list('pos_id', flat=True)
        files_pos_ids = pos_requests.FileStruct(FileId=[str(i) for i in files_ids])
        user = appeal.user

        try:
            epgu_id = int(user.esia_id.split("_")[1])
        except:
            raise APIException("invalid esia id", code=status.HTTP_400_BAD_REQUEST)

        applicant = pos_requests.ApplicantDataStruct(
            EpguId=epgu_id,
            Name=user.first_name,
            Email=user.email if user.email else None,
            Surname=user.last_name if user.last_name else None,
            Patronymic=user.patronymic_name if user.patronymic_name else None,
            Phone=user.phone if user.phone else None,
        )
        appeal_struct = pos_requests.AppealDataStruct(
            Id=appeal.id,
            Description=appeal.text,
            CreatedAt=timezone.now().strftime("%Y-%m-%dT%H:%M:%S.234Z"),
            Applicant=applicant,
            SubjectId=appeal.subcategory.category.pos_id,
            SubsubjectId=appeal.subcategory.pos_id,
            Location=appeal.address,
            AttachmentIds=files_pos_ids,
        )

        template_path = TemplatePath.CREATE_APPEAL_REQUEST
        appeal_xml = appeal_struct.to_xml_by_template(template_path)
        SmevLog.objects.create(
            description=f'Запрос на отправку обращения id={appeal.id}',
            xml_data=appeal_xml.decode()
        )
        response = self.http_client.smev_send_request(appeal_xml)
        return response

    def update_appeal(self, appeal: Appeal):
        appeal_struct = pos_requests.GetAppealRequest(
            AppealId=appeal.pos_id
        )
        template_path = TemplatePath.GET_APPEAL_REQUEST
        appeal_xml = appeal_struct.to_xml_by_template(template_path)
        response = self.http_client.smev_send_request(appeal_xml)
        return response

    def send_files(self, files: Iterable[File]):
        files_ids = []
        for file in files:
            file_data = [('files', (str(file.name), file.file.open("rb")))]
            response = self.http_client.send_file(file_data)
            data_to_update = response.json()
            [smev_adapter_id] = data_to_update.values()
            file.smev_adapter_id = smev_adapter_id
            file.save()
            files_ids.append(file.id)
        return File.objects.filter(id__in=files_ids)

    def send_files_to_pos(self, files):
        attachments = [pos_requests.AttachmentStruct(
            Name=file.name,
            AttachmentUuid=str(file.smev_adapter_id),
        ) for file in files]

        file_upload_struct = pos_requests.FileUploadRequest(
            File=attachments
        )
        template_path = TemplatePath.FILE_UPLOAD_REQUEST
        file_upload_xml = file_upload_struct.to_xml_by_template(template_path)
        response = self.http_client.send_files_to_pos(
            file_upload_xml,
            [str(file.smev_adapter_id) for file in files]
        )
        return response

    def get_files_from_pos(self, files_ids: list):
        file_download_request = pos_requests.FileDownloadRequest(
            FileId=files_ids
        )
        template_path = TemplatePath.FILE_DOWNLOAD_REQUEST
        file_upload_xml = file_download_request.to_xml_by_template(template_path)
        response = self.http_client.smev_send_request(file_upload_xml)
        return response
