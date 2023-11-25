from django.core.management.base import BaseCommand
from django_model_docs.serializers.app_serializer import (
    AppSerializer,
)


class Command(BaseCommand):
    app_serializer = AppSerializer()

    """
    Generate markdown file from a given django app name
    """

    def add_arguments(self, parser):
        """
        Add arguments for management command
        """

        parser.add_argument("app", type=str, help="Django app module name")
        parser.add_argument(
            "-o",
            "--out-file",
            type=str,
            required=False,
            help="Name of markdown file to create",
        )

    def handle(self, *args, **options):
        """
        Handler for management command
        """

        app_name = options["app"]
        out_file = options["out_file"]

        data_dictionary = self.app_serializer.markdown(app_name)

        if out_file is not None:
            with open(out_file, "w") as fh:
                fh.write(data_dictionary)
        else:
            print(data_dictionary)
