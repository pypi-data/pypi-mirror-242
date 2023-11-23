from django.urls import path, include
from rest_framework import routers

from modules.voting.api import (
    VoteOperatorAPI,
    VoteModeratorAPI,
    FileAPI,
    VotingParticipantAPI,
    LocalVotingGroupAPI,
    MunicipalVoteOperatorLKOAPI,
    RegionalVoteOperatorLKOAPI,
    MunicipalVoteModeratorAPI,
    LocalVoteOperatorLKOAPI,
    RegionalVoteModeratorAPI,
    LocalVoteModeratorAPI,
    ActivateModerationMechanismAPI
)

router = routers.DefaultRouter()

router.register("vote-operator", VoteOperatorAPI, basename="vote-operator")
router.register("vote-moderator", VoteModeratorAPI, basename="vote-moderator")
router.register("file", FileAPI, basename="file")
router.register(
    "voting-participant", VotingParticipantAPI, basename="voting-participant"
)
router.register(
    "local-voting-group", LocalVotingGroupAPI, basename="local-voting-group"
)

router.register("municipal_vote", MunicipalVoteOperatorLKOAPI, basename="municipal_vote")
router.register("local_vote", LocalVoteOperatorLKOAPI, basename="local_vote")
router.register("regional_vote", RegionalVoteOperatorLKOAPI, basename="regional_vote")
router.register("municipal_vote_moderator", MunicipalVoteModeratorAPI, basename="municipal-vote-moderator")
router.register("regional_vote_moderator", RegionalVoteModeratorAPI, basename="regional-vote-moderator")
router.register("local_vote_moderator", LocalVoteModeratorAPI, basename="local-vote-moderator")
urlpatterns = [
    path("", include(router.urls), name="api"),
    path("get_opportunities_to_moderate/", ActivateModerationMechanismAPI.as_view())
]
