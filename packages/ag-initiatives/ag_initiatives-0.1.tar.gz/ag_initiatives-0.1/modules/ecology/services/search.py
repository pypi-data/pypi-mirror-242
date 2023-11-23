from django.db.models import Q


def get_search_filter_by_user_fio(FIO: str):
    FIO = FIO.split(" ")
    if len(FIO) == 1:
        return Q(user__last_name__icontains=FIO[0]) | Q(
            user__first_name__icontains=FIO[0]
        )
    else:
        return Q(
            user__last_name__icontains=FIO[0], user__first_name__icontains=FIO[1]
        ) | Q(user__first_name__icontains=FIO[0], user__last_name__icontains=FIO[1])
