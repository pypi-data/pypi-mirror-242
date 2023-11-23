from typing import List

from django.core.files.base import ContentFile
from django.utils.dateparse import parse_datetime

from .base_response_strategy import BaseResponseStrategy
from .dto.pos_response import FileUploadResponse, AppealResponse, AppealDTO, FileDownloadResponse, FSAttachmentsList
from .pos_smev_client import PosSmevHttpClient
from .pos_smev_service import PosSmevService
from ..mail_service import MailService
from ..xml_service import XMLService
from ...models import Appeal, AppealStateChange, AppealAnswer, AppealAttachment
from ...models.appeal import AppealState, SmevState
from ...models.file import File
from ...tasks.get_files_from_pos import get_files_from_pos


class PosResponseStrategy(BaseResponseStrategy):
    TAG = "PosEasResponse"

    @classmethod
    def process_response(cls, xml):
        root = cls.get_current_block(xml)
        if FileUploadPosResponseStrategy.is_current(root):
            strategy = FileUploadPosResponseStrategy()
        elif CreateAppealPosResponseStrategy.is_current(root):
            strategy = CreateAppealPosResponseStrategy()
        elif GetAppealPosResponseStrategy.is_current(root):
            strategy = GetAppealPosResponseStrategy()
        elif FileDownloadResponseStrategy.is_current(root):
            strategy = FileDownloadResponseStrategy()
        else:
            return XMLService.xml_to_dict(root)

        result = strategy.process_response(root)
        return result


class FileDownloadResponseStrategy(BaseResponseStrategy):
    TAG = "FileDownloadResponse"

    @classmethod
    def get_fs_attachments_block(cls, xml):
        if block := xml.xpath(f'//*[local-name()="FSAttachmentsList"]'):
            return block[0]
        return None

    def process_response(self, xml):
        block = self.get_current_block(xml)
        raw_data = XMLService.xml_to_dict(block)
        files_data: FileDownloadResponse = FileDownloadResponse(**raw_data)

        fs_attachments_block = self.get_fs_attachments_block(xml)
        fs_attachments_raw = XMLService.xml_to_dict(fs_attachments_block)
        fs_attachments = FSAttachmentsList(**fs_attachments_raw)

        for file in files_data.FileDownloadResult:
            attachment: AppealAttachment = AppealAttachment.objects.filter(pos_id=file.File.Id).first()
            if not attachment:
                continue

            attachment.ftp_uuid = file.File.AttachmentUuid
            for attach in fs_attachments.FSAttachment:
                if attach.uuid == attachment.ftp_uuid:
                    attachment.ftp_password = attach.Password
                    attachment.ftp_username = attach.UserName
                    attachment.file_name = attach.FileName.split("/")[-1]
            attachment.save()
            self.download_appeal_attachment(attachment)
        return files_data.to_dict()

    @staticmethod
    def download_appeal_attachment(attachment: AppealAttachment):
        if not attachment.file and attachment.ftp_username:
            file = PosSmevHttpClient().download_file(
                "",
                attachment.ftp_username,
                attachment.ftp_password,
            )
            if not file:
                return
            content_file = ContentFile(file, name=attachment.file_name)
            attachment.file.save(attachment.file_name, content_file)


class FileUploadPosResponseStrategy(BaseResponseStrategy):
    TAG = "FileUploadResponse"

    def process_response(self, xml):
        block = self.get_current_block(xml)
        raw_data = XMLService.xml_to_dict(block)
        file_data = FileUploadResponse(**raw_data)
        self._update_file_pos_id(file_data)
        return file_data.to_dict()

    @staticmethod
    def _update_file_pos_id(file_response: FileUploadResponse):
        files_ids = {file.AttachmentUuid: file.Id for file in file_response.File}
        files = File.objects.filter(smev_adapter_id__in=files_ids.keys())
        for file in files:
            file.pos_id = files_ids[str(file.smev_adapter_id)]
            file.save()


class CreateAppealPosResponseStrategy(BaseResponseStrategy):
    TAG = "CreateAppealResponse"

    def process_response(self, xml):
        block = self.get_current_block(xml)
        raw_data = XMLService.xml_to_dict(block)
        appeal_data = AppealResponse(**raw_data)
        self._update_appeal_pos_id(appeal_data)
        return appeal_data.to_dict()

    @staticmethod
    def _update_appeal_pos_id(appeal_data: AppealResponse):
        if appeal_data.Status.OperationResult != 'SUCCESS':
            raise Exception(f"Статус сообщения пос: {appeal_data.Status.OperationResult}")
        appeal = Appeal.objects.filter(pk=appeal_data.Appeal.Id).first()
        if not appeal:
            raise Exception(f"Обращение не найдено в системе: {appeal_data}")
        else:
            appeal.status = AppealState.from_pos_status(appeal_data.Appeal.Status)
            appeal.smev_status = SmevState.SUCCESS
            appeal.pos_id = appeal_data.Appeal.PosId
            PosSmevService().update_appeal(appeal)
        appeal.save()


class GetAppealPosResponseStrategy(BaseResponseStrategy):
    TAG = "GetAppealResponse"

    def process_response(self, xml):
        block = self.get_current_block(xml)
        raw_data = XMLService.xml_to_dict(block)
        appeal_data = AppealResponse(**raw_data)
        self._update_appeal(appeal_data)
        return appeal_data.to_dict()

    @staticmethod
    def _appeal_attachment_create(appeal: AppealAnswer):
        if not isinstance(appeal.files, list):
            return
        files_pos_ids = [i.split('/')[-1] for i in appeal.files]
        for pos_id in files_pos_ids:
            AppealAttachment.objects.create(
                appeal_answer=appeal,
                pos_id=pos_id
            )
        get_files_from_pos.delay(files_pos_ids)

    def _update_appeal(self, appeal_struct: AppealResponse):
        """Обновляет историю обращения"""
        appeal_struct: AppealDTO = appeal_struct.Appeal
        appeal = Appeal.objects.filter(pos_id=appeal_struct.PosId).first()
        if not appeal:
            raise Exception(f"Обращение не найдено в системе: {appeal_struct}")

        appeal.status = AppealState.from_pos_status(appeal_struct.Status)
        appeal.pos_id = appeal_struct.PosId
        appeal.save()

        answers_to_create: List[AppealAnswer] = []

        appeal_history = AppealStateChange.objects.filter(appeal=appeal).all()

        appeals_state_change_list = []
        reject_reason = None

        status_histories = appeal_struct.StatusHistory.StatusHistories if appeal_struct.StatusHistory else []
        for history_struct in status_histories:
            if parse_datetime(history_struct.CreatedAt) in list(
                    map(lambda appeal_state_change: appeal_state_change.created_at, appeal_history)
            ):
                continue

            status = AppealState.from_pos_status(history_struct.Status)
            is_hide = False
            if status in [i.status for i in appeal_history] \
                    or status in [i.status for i in appeals_state_change_list]:
                is_hide = True

            created_by = None
            if history_struct.CreatedBy:
                created_by = f"{history_struct.CreatedBy.Surname} {history_struct.CreatedBy.Name} {history_struct.CreatedBy.Patronymic}"
            appeals_state_change = AppealStateChange.objects.create(
                appeal=appeal,
                status=status,
                created_at=history_struct.CreatedAt,
                created_by=created_by,
                pos_status=history_struct.Status,
                pos_status_name=history_struct.StatusText,
                is_hide=is_hide,
            )
            appeals_state_change_list.append(appeals_state_change)
            if history_struct.Answer:
                answer = history_struct.Answer
                answers_to_create.append(
                    AppealAnswer(
                        appeal_state_change=appeals_state_change,
                        answer_type=answer.AnswerType,
                        comment=answer.Comment,
                        reject_reason=answer.RejectReason.Name if answer.RejectReason else None,
                        files=answer.AttachmentIds.FileId if answer.AttachmentIds else None,
                    )
                )
                reject_reason = answer.RejectReason.Name

        appeals_answers = AppealAnswer.objects.bulk_create(answers_to_create)
        for answer in appeals_answers:
            self._appeal_attachment_create(answer)

        appeals_state_change_list = list(filter(lambda x: not x.is_hide, appeals_state_change_list))
        if not appeals_state_change_list:
            return

        appeals_state_change_list = list(sorted(appeals_state_change_list, key=lambda x: x.created_at))

        appeal.refresh_from_db()
        mail_service = MailService(appeal)
        for appeals_state_change in appeals_state_change_list:
            if appeals_state_change.status == AppealState.MODERATION:
                mail_service.notify_user_moderation()
            if appeals_state_change.status == AppealState.MODERATION_REJECTED:
                mail_service.notify_user_rejected(reject_reason if reject_reason else "")
            if appeals_state_change.status == AppealState.MODERATION_ACCEPTED:
                mail_service.notify_user_accepted()
            if appeals_state_change.status == AppealState.IN_PROGRESS:
                mail_service.notify_user_in_progress()
            if appeals_state_change.status == AppealState.RESPONDED:
                mail_service.notify_user_responded()
