import traceback

from django.core.management.base import BaseCommand, CommandError
from elastic_search.collect import collect_data, validate_es_data, check_data


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.stdout.write("Data Mining instantiated.")
            collect_data()

            if not validate_es_data():
                self.stdout.write("Count mismatch. Checking for errors.")
                check_data()

        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("Task Completed.")
