from collections import defaultdict
import io

from django.utils import timezone
from xlsxwriter import Workbook

from modules.voting.models import UserVote


class ReportService:
    def get_vote_data_for_report(self, vote):
        user_votes = (
            UserVote.objects.filter(vote=vote)
            .order_by("locality", "question", "answer_option")
            .select_related(
                "user",
            )
        )
        localiies_map = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
            )
        )

        year_now = timezone.now().date().year
        for user_vote in user_votes:
            locality_id = user_vote.locality.pk
            questions_id = user_vote.question.pk
            answer_id = user_vote.answer_option.pk

            user_age_group = 0
            if user_vote.user.birth_date:
                user_age = year_now - user_vote.user.birth_date.year
                if user_age < 18:
                    user_age_group = 1
                elif user_age < 25:
                    user_age_group = 2
                elif user_age < 35:
                    user_age_group = 3
                elif user_age < 45:
                    user_age_group = 4
                elif user_age < 55:
                    user_age_group = 5
                elif user_age >= 55:
                    user_age_group = 6

            localiies_map[locality_id][questions_id][answer_id][user_vote.user.gender][
                user_age_group
            ] += 1

        return localiies_map

    def create_vote_report2_xlsx(self, vote, vote_results_data):
        wb = Workbook()

        ws = wb.active

        ws.column_dimensions["A"].width = 48

        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        return xlsx_buffer
