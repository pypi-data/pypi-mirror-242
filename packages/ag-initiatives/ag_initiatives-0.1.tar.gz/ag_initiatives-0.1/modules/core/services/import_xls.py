import xlrd
from django.db import transaction
from django.utils import timezone

from modules.core.models import Locality, Category
from modules.voting.models import Vote, VoteQuestion, VoteAnswerOption


@transaction.atomic
def import_xls(file_contents):

    book = xlrd.open_workbook(file_contents=file_contents)

    sheet = book.sheet_by_index(0)

    vote = None
    current_vote_id = None

    for rownum in range(sheet.nrows):
        if rownum < 1:  # skip table header
            continue

        row = sheet.row_values(rownum)

        vote_id = int(row[0])
        category_name = row[1].strip()
        vote_name = row[2].strip()
        question_name = row[3].strip()
        answers_texts = [s.strip() for s in row[4].split(";")]
        locality_names = [s.strip() for s in row[5].split(";")]

        if vote_id != current_vote_id:
            current_vote_id = vote_id
            vote = None

        if not vote:
            current_vote_id = vote_id
            vote_category = Category.objects.get(name=category_name)
            vote_localities = Locality.objects.filter(name__in=locality_names)

            vote = Vote.objects.create(
                name=vote_name,
                category=vote_category,
                start_date=timezone.now().date(),
                end_date=timezone.now().date(),
                # is_published=True,
            )
            for locality in vote_localities:
                vote.locality.add(locality)

        vote_question = VoteQuestion.objects.create(
            vote=vote,
            brief=question_name,
        )

        for answers_text in answers_texts:
            VoteAnswerOption.objects.create(
                vote_question=vote_question, brief=answers_text
            )
