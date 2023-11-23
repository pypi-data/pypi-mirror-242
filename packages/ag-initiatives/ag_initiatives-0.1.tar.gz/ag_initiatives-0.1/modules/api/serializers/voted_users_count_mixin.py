from rest_framework import serializers

from modules.voting.models import Vote, VoteQuestion, VoteMunicipal, VoteAnswerOption,\
    VoteMunicipalQuestion, VoteMunicipalAnswer, VoteRegional, VoteRegionalQuestion,\
        VoteRegionalAnswer, VoteLocal, VoteLocalAnswer, VoteLocalQuestion


class VotedUsersCountMixin(serializers.Serializer):
    voted_users_count = serializers.SerializerMethodField()

    def get_voted_users_count(self, instance):
        if isinstance(instance, (Vote, VoteQuestion, VoteAnswerOption)):
            qs = instance.uservote_set.distinct("user")

        elif isinstance(instance, (VoteMunicipal,VoteMunicipalQuestion, VoteMunicipalAnswer,\
        VoteRegional, VoteRegionalQuestion, VoteRegionalAnswer,\
            VoteLocal, VoteLocalAnswer, VoteLocalQuestion)):
            qs = instance.usermunicipalvote_set.distinct("user")

        else:
            raise ValueError("Wrong instance in VotedUsersCountMixin")

        request = self.context.get("request", None)
        if request is None:
            return qs.count()

        locality_id = request.query_params.get("locality", None)
        if locality_id is not None:
            qs = qs.filter(locality__id=locality_id)

        return qs.count()
