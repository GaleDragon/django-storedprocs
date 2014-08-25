from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db.utils import DatabaseError
# Create your models here.

class StoredProcedureManager(models.Manager):

    def __init__(self):
        self._procedures = []
        try:
            self._procedures = list(StoredProcedure.objects.all())
        except DatabaseError:
            # This probably means that we're in the middle of a syncdb
            # In this case we DON'T try to load procedures,
            # because the table does not exist yet.
            pass

        for p in self._procedures:
            setattr(self, p.attribute, self._wrapper(p))
            setattr(self, '_%s' % p.attribute, p.sql)

        super(StoredProcedureManager, self).__init__()

    def _wrapper(self, procedure):
        db_backend = settings.DATABASES['default']['ENGINE'].split('.')[-1]

        def execute_proc(*args, **kwargs):
            if args and kwargs:
                raise StoredProcedureConflictException("""Choose either positional
                or keyword arguments.""")

            cursor = connection.cursor()

            # Sqlite does not support stored procedures,
            # so we simulate the behavior by just running the SQL in the model
            if not db_backend == 'sqlite3':
                cursor.execute("SELECT %s()" % procedure.attribute)
            else:
                cursor.execute(getattr(self, "_%s" % procedure.attribute))

            if not procedure.primitive:
                returned_model = procedure.content_type.model_class()
                results = []
                for row in cursor.fetchall():
                    q = returned_model(text=row[0])
                    results.append(q)
                return results
            else:
                return cursor.fetchall()[0][0]

        return execute_proc


class StoredProcedureConflictException(Exception):
    pass


class StoredProcedure(models.Model):
    attribute = models.CharField(max_length=255)
    sql = models.TextField()
    db = models.CharField(max_length=100)

    primitive = models.BooleanField(default=True)
    primitive_type = models.CharField(max_length=30)

    return_type = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.primitive and not self.return_type:
            raise StoredProcedureConflictException("""You need to set
            whether the procedure returns a primitive or what model the QuerySet is.""")
        return super(StoredProcedure, self).save(force_insert=force_insert,
                                                 force_update=force_update,
                                                 using=using,
                                                 update_fields=update_fields)


class StoredProcedureArguments(models.Model):
    name = models.CharField(max_length=255)
    arg_type = models.CharField(max_length=10)
    argument_for = models.ForeignKey(StoredProcedure, related_name='arguments')