from rest_framework import routers

from .opinion import OpinionModeratorAPI
from .voting import VotingModeratorAPI
from .initiative import InitiativeModeratorAPI
from .moderator_info import ModeratorInfoAPI

router = routers.SimpleRouter()

router.register("initiatives", InitiativeModeratorAPI, basename="moderator_initiatives")

router.register("info", ModeratorInfoAPI, basename="moderator_info")

router.register("voting", VotingModeratorAPI, basename="moderator_voting")

router.register("opinions", OpinionModeratorAPI, basename="moderator_opinions")
