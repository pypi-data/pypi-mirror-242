from django.contrib import admin

import modules.voting.models
from modules.core.models import Category
from config.settings import settings

from .reject_reason_admin import RejectReasonAdmin
from .import_xls_admin import ImportXlsAdmin
from .user_vote_admin import UserVoteAdmin
from .user_municipal_vote_admin import UserMunicipalVoteAdmin
from .category_admin import CategoryAdmin
from .vote_admin import VoteAdmin
from .vote_municipal_admin import VoteMunicipalAdmin
from .vote_regional_admin import VoteRegionalAdmin
from .vote_local_admin import VoteLocalAdmin
from .activation_moderation_mechanism_admin import ActivationModerationMechanismAdmin
from .local_voting_group_admin import LocalVotingGroupAdmin
from .voting_participant_admin import VotingParticipantAdmin

if settings.INVENTORY_STANDALONE:
    admin.site.unregister(modules.voting.models.LocalVotingGroup)
    admin.site.unregister(modules.voting.models.VotingParticipant)
    admin.site.unregister(modules.voting.models.Vote)
    admin.site.unregister(modules.voting.models.UserVote)
    admin.site.unregister(modules.voting.models.ImportXlsModel)
    admin.site.unregister(modules.voting.models.RejectReason)
    admin.site.unregister(Category)

unregister_models = [
    modules.voting.models.LocalVotingGroup,
    modules.voting.models.VoteLocal,
    modules.voting.models.ActivationModerationMechanism,
    modules.voting.models.VoteMunicipal,
    modules.voting.models.UserMunicipalVote,
    modules.voting.models.VoteRegional,
]

for i in unregister_models:
    try:
        admin.site.unregister(i)
    except Exception:
        pass
