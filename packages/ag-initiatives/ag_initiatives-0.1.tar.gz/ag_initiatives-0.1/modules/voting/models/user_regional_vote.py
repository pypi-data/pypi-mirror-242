# from django.conf import settings
# from django.db import models


# class UserRegionalVote(models.Model):
#     """
#     Отчёт по региональному голосованию конкретного пользователя.
#     """

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name="Пользователь",
#     )
#     vote = models.ForeignKey(
#         "voting.VoteRegional",
#         on_delete=models.CASCADE,
#         verbose_name="Голосование",
#     )
#     question = models.ForeignKey(
#         "voting.VoteRegionalQuestion",
#         on_delete=models.CASCADE,
#         verbose_name="Вопрос голосования",
#     )
#     answer_option = models.ForeignKey(
#         to="voting.VoteRegionalAnswer",
#         on_delete=models.CASCADE,
#         verbose_name="Вариант ответа",
#         blank=True,
#         null=True,
#     )
#     custom_answer = models.TextField(
#         verbose_name="Вариант пользователя",
#         blank=True,
#         null=True,
#     )
#     municipality = models.ForeignKey(
#         to="core.Municipality",
#         verbose_name="Населенный пункт",
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#     )  

#     class Meta:
#         indexes = [
#             models.Index(fields=["user", "vote"]),
#             models.Index(fields=["user", "vote", "question"]),
#         ]
#         verbose_name = "Ответ пользователя по региональному голосованию"
#         verbose_name_plural = "Ответы пользователей по региональному голосованиям"
