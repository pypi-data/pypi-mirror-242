import collections

from modules.ecology.models import UserProfile, Settings


class EcologyStatus(object):
    BEGINNER = "BEGINNER"
    DWELLER = "DWELLER"
    CITY_EXPERT = "CITY_EXPERT"
    ACTIVE_CITIZEN = "ACTIVE_CITIZEN"

    RESOLVER = collections.OrderedDict(
        [
            (BEGINNER, "Новичок"),
            (DWELLER, "Житель"),
            (CITY_EXPERT, "Городской эксперт"),
            (ACTIVE_CITIZEN, "Активный гражданин"),
        ]
    )

    CHOICES = RESOLVER.items()


def get_ecology_status(user_profile: UserProfile):
    settings: Settings = Settings.load()
    user_earned_bonuses = user_profile.earned_bonuses

    if user_earned_bonuses < settings.min_dweller_bonuses:
        return EcologyStatus.BEGINNER
    elif user_earned_bonuses < settings.min_city_expert_bonuses:
        return EcologyStatus.DWELLER
    elif user_earned_bonuses < settings.min_active_citizen_bonuses:
        return EcologyStatus.CITY_EXPERT
    else:
        return EcologyStatus.ACTIVE_CITIZEN
