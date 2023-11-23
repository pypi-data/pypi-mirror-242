from pathlib import Path
from typing import IO, Generator, Optional

from django.http import StreamingHttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.status import HTTP_206_PARTIAL_CONTENT, HTTP_200_OK

from modules.core.models import Video


class VideoService:
    @staticmethod
    def get_by_id(pk: int) -> Video:
        instance = Video.objects.filter(pk=pk).first()
        if not instance:
            raise NotFound()

        return instance

    @staticmethod
    def read_ranged_file(
        file: IO[bytes], start: int = 0, end: int = None, block_size: int = 8192
    ) -> Optional[bytes]:
        consumed = 0

        file.seek(start)
        while True:
            data_length = min(block_size, end - start - consumed) if end else block_size
            if data_length <= 0:
                break

            data = file.read(data_length)
            if not data:
                break

            consumed += data_length
            yield data

        if hasattr(file, "close"):
            file.close()

    @classmethod
    def open_file_from_request(cls, request: Request, pk: int) -> tuple:
        video_instance = cls.get_by_id(pk)

        path = Path(video_instance.file.path)
        file = path.open("rb")
        file_size = path.stat().st_size

        content_length = file_size
        status_code = HTTP_200_OK
        content_range = request.headers.get("range")

        if content_range is not None:
            content_ranges = content_range.strip().lower().split("=")[-1]

            range_start, range_end, *_ = map(
                str.strip, (content_ranges + "-").split("-")
            )
            range_start = max(0, int(range_start)) if range_start else 0
            range_end = (
                min(file_size - 1, int(range_end)) if range_end else file_size - 1
            )

            content_length = (range_end - range_start) + 1
            file = cls.read_ranged_file(file, start=range_start, end=range_end + 1)
            status_code = HTTP_206_PARTIAL_CONTENT
            content_range = f"bytes {range_start}-{range_end}/{file_size}"

        return file, status_code, content_length, content_range

    @classmethod
    def get_stream_response(cls, request: Request, pk: int) -> StreamingHttpResponse:
        file, status_code, content_length, content_range = cls.open_file_from_request(
            request, pk
        )
        response = StreamingHttpResponse(
            file, status=status_code, content_type="video/mp4"
        )

        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = str(content_length)
        response["Cache-Control"] = "no-cache"
        response["Content-Range"] = content_range
        return response
