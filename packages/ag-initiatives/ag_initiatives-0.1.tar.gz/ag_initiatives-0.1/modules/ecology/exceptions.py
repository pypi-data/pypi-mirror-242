class OrganizerError(Exception):
    def __init__(self, message):
        self.message = message


class PartnerError(Exception):
    def __init__(self, message):
        self.message = message


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserParticipationError(UserError):
    pass


class UserPurchaseError(UserError):
    pass


class BalanceOperationError(Exception):
    def __init__(self, message):
        self.message = message
