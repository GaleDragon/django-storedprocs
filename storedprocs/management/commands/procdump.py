from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Dumps current stored procedures into a fixture'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='+', type=str)

    def handle(self, *args, **options):
        for app in options['app']:
            pass