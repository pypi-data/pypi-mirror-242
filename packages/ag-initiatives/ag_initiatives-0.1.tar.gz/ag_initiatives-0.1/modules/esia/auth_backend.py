import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from modules.core.models import Locality, LocalityType, User, UserRole


class EsiaDataStruct:
    def __init__(self, esia_data):
        self.oid = None
        self.email = None
        self.phone = None
        self.person_passport = None
        self.snils = None
        self.person_first_name = None
        self.person_middle_name = None
        self.person_last_name = None
        self.person_inn = None
        self.person_birth_date = None
        self.person_gender = None
        self.person_registration_region = None
        self.person_registration_city = None
        self.person_registration_area = None
        self.person_registration_settlement = None
        self.person_residential_region = None
        self.person_residential_city = None
        self.person_residential_area = None
        self.person_residential_settlement = None
        self.trusted = None

        self._fill_details_from_data(esia_data)

    def _fill_details_from_data(self, esia_data):
        contacts = esia_data.get("ctts", {}) or {}
        info = esia_data.get("info", {}) or {}
        docs = esia_data.get("docs", {}) or {}
        addrs = esia_data.get("addrs", {}) or {}

        self.oid = esia_data.get("oid", None)
        self.snils = info.get("snils", None)
        self.person_first_name = info.get("firstName", None)
        self.person_middle_name = info.get("middleName", None)
        self.person_last_name = info.get("lastName", None)
        self.person_inn = info.get("inn", None)
        self.person_birth_date = info.get("birthDate", None)
        self.person_gender = info.get("gender", None)
        self.trusted = info.get("trusted", None)

        for c in contacts.get("elements", []):
            if c.get("type", None) == "EML":
                self.email = c.get("value", None)
            if c.get("type", None) == "MBT":
                self.phone = c.get("value", None)

        for d in docs.get("elements", []):
            if d.get("type", None) == "RF_PASSPORT":
                self.person_passport = (
                    "{series} {number}/{issueDate}/{issueId}/{issuedBy}".format(
                        series=d.get("series", ""),
                        number=d.get("number", ""),
                        issueDate=d.get("issueDate", ""),
                        issueId=d.get("issueId", ""),
                        issuedBy=d.get("issuedBy", ""),
                    )
                )

        for a in addrs.get("elements", []):
            if a.get("type", None) == "PLV":
                self.person_residential_region = a.get("region", None)
                self.person_residential_city = a.get("city", None)
                self.person_residential_area = a.get("area", None)
                self.person_residential_settlement = a.get("settlement", None)
            if a.get("type", None) == "PRG":
                self.person_registration_region = a.get("region", None)
                self.person_registration_city = a.get("city", None)
                self.person_registration_area = a.get("area", None)
                self.person_registration_settlement = a.get("settlement", None)


def find_locality(city_name: str, region_name: str, area: str, settlement: str):
    for locality in Locality.objects.all():
        if city_name is None:
            continue
        if locality.name in city_name:
            return locality

    try:
        return Locality.objects.get(name=region_name)
    except:
        pass

    try:
        return Locality.objects.get(name=settlement)
    except:
        pass

    try:
        return Locality.objects.get(name=area)
    except:
        pass

    try:
        if city_name is not None:
            localities = Locality.objects.filter(name__icontains=city_name)

            if len(city_name) != 0 and localities.count() > 0:
                return localities.first()
            else:
                city_names = [c for c in city_name.split(" ") if len(c) > 2]
                for c in city_names:
                    localities = Locality.objects.filter(name__icontains=c)
                    if localities.count() > 0:
                        return localities.first()

        if area is not None:
            areas = [a for a in area.split(" ") if len(a) > 2]
            for a in areas:
                localities = Locality.objects.filter(name__icontains=a)
                if localities.count() > 0:
                    return localities.first()
    except:
        pass

    return None


class EsiaAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        create_user = kwargs.get("create_user", False)
        is_staff = kwargs.get("is_staff", False)
        esia_data = EsiaDataStruct(kwargs.get("esia_data", {}))

        if esia_data.oid is None:
            return None

        username = f"esia_{esia_data.oid}"
        birth_date = None
        try:
            birth_date = datetime.datetime.strptime(
                esia_data.person_birth_date, "%d.%m.%Y"
            ).date()
        except:
            pass

        user: User = None

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            pass
        pass

        if user is not None:
            user.snils = esia_data.snils
            user.email = esia_data.email or ""
            user.phone = (esia_data.phone or "").replace("(", "").replace(")", "")
            user.first_name = esia_data.person_first_name
            user.last_name = esia_data.person_last_name
            user.patronymic_name = esia_data.person_middle_name
            user.gender = esia_data.person_gender
            user.birth_date = birth_date
            user.registration_locality = find_locality(
                esia_data.person_registration_city,
                esia_data.person_registration_region,
                esia_data.person_registration_area,
                esia_data.person_registration_settlement,
            )
            user.residential_locality = find_locality(
                esia_data.person_residential_city,
                esia_data.person_residential_region,
                esia_data.person_residential_area,
                esia_data.person_residential_settlement,
            )
            user.esia_verified = esia_data.trusted
            if not user.roles:
                user.roles = UserRole.USER
            user.save(
                update_fields=[
                    "snils",
                    "email",
                    "phone",
                    "first_name",
                    "last_name",
                    "patronymic_name",
                    "gender",
                    "birth_date",
                    "registration_locality",
                    "residential_locality",
                    "esia_verified",
                    "roles",
                ]
            )

            if user.is_active:
                return user
            else:
                return None

        if not create_user:
            return None

        user = UserModel.objects.create_user(
            snils=esia_data.snils,
            username=username,
            email=esia_data.email or "",
            phone=(esia_data.phone or "").replace("(", "").replace(")", ""),
            first_name=esia_data.person_first_name,
            last_name=esia_data.person_last_name,
            patronymic_name=esia_data.person_middle_name,
            gender=esia_data.person_gender,
            birth_date=birth_date,
            is_staff=is_staff,
            registration_locality=find_locality(
                esia_data.person_registration_city,
                esia_data.person_registration_region,
                esia_data.person_registration_area,
                esia_data.person_registration_settlement,
            ),
            residential_locality=find_locality(
                esia_data.person_residential_city,
                esia_data.person_residential_region,
                esia_data.person_residential_area,
                esia_data.person_residential_settlement,
            ),
            esia_verified=esia_data.trusted,
            roles=UserRole.USER,
        )

        return user
