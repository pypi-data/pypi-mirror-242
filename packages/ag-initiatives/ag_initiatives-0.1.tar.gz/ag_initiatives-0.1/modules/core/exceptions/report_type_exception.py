from rest_framework.exceptions import ValidationError


class ReportTypeError(ValidationError):
    """
    === Исключение по типу отчёта

    Поля:

    * message - информационное сообщение;
    +
    форматируется при инициализации по значению
    +
    ****
    `report_type`
    ****
    """

    message: str = "Type `{report_type}` does not exist."

    def __init__(self, report_type):
        self.report_type = report_type
        self.message = self.message.format(
            report_type=self.report_type,
        )
        super().__init__(self.message)


class EmptyVoteError(ValidationError):
    message: str = "Vote filter is empty. Use ?vote=<int:pk>"

    def __init__(self):
        super().__init__(self.message)


class RegionalReportTypeError(ReportTypeError):

    message = "Type `{report_type}` is not intended for a regional report"
