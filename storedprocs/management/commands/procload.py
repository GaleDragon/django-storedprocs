from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Load stored procedure fixtures into the database if applicable'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='+', type=str)

    def handle(self, *args, **options):
        from storedprocs.models import StoredProcedure
        from django.db import connection
        db_backend = settings.DATABASES['default']['ENGINE'].split('.')[-1]

        call_command('loaddata', 'procedures_%s' % db_backend)

        if db_backend != 'sqlite3':  # Sqlite doesn't do stored procedures
            for procedure in StoredProcedure.objects.all():
                if not procedure.content_type_id:
                    if "." in procedure.return_type:
                        app, model = procedure.return_type.split(".", maxsplit=1)
                        procedure.content_type = ContentType(model=model, app_label=app)
                    else:
                        procedure.content_type = ContentType(model=procedure.return_type)
                    procedure.save()

            cursor = connection.cursor()
            cursor.execute("""
            CREATE OR REPLACE FUNCTION %s RETURNS SETOF %s AS $$
                %s
            $$ LANGUAGE sql;""" % (procedure.attribute, procedure.content_type.model_class()))