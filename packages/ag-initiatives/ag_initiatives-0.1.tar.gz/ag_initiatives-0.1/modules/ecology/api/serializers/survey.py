from rest_framework import serializers

from modules.ecology.models import Survey, SurveyQuestion, SurveyQuestionAnswer


class SurveyQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionAnswer
        fields = [
            "id",
            "text",
            "group",
            "order",
        ]


class SurveyQuestionSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    def get_groups(self, instance):
        result = []

        answers = instance.answers.all()
        groups = (
            answers.exclude(group__exact="")
            .filter(group__isnull=False)
            .values_list("group", flat=True)
            .distinct()
        )

        for group in groups:
            result.append(
                {
                    "type": "GROUP",
                    "answers": [
                        SurveyQuestionAnswerSerializer(answer).data
                        for answer in answers.filter(group=group)
                    ],
                }
            )

        for answer in answers.exclude(group__in=groups):
            result.append(
                {
                    "type": "SINGLE",
                    "answer": SurveyQuestionAnswerSerializer(answer).data,
                }
            )

        return result

    class Meta:
        model = SurveyQuestion
        fields = [
            "id",
            "text",
            "order",
            "groups",
        ]


class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ["id", "name", "description", "questions"]
