from rest_framework.decorators import api_view
from rest_framework.response import Response

from modules.core.models import User
from modules.voting.models import Vote, UserVote


@api_view(["GET"])
def stats(request):
    res = {
        "active_users": User.objects.filter(is_active=True).count(),
        "votes_published": Vote.objects.filter(is_published=True).count(),
        "user_votes_count": UserVote.objects.count(),
    }

    return Response(res)
