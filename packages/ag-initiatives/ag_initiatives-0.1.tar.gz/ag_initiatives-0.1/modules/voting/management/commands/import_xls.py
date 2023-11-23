from django.core.management import BaseCommand

from modules.core.services import import_xls


class Command(BaseCommand):
    help = "import xls file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        file = options.get("file", None)

        if file is None:
            print("invalid filename")
            return

        with open(file, "rb") as f:
            import_xls(f.read())
