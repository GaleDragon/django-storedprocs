# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StoredProcedure'
        db.create_table('storedprocs_storedprocedure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sql', self.gf('django.db.models.fields.TextField')()),
            ('db', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('primitive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('primitive_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('return_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('storedprocs', ['StoredProcedure'])

        # Adding model 'StoredProcedureArguments'
        db.create_table('storedprocs_storedprocedurearguments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('arg_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('argument_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storedprocs.StoredProcedure'], related_name='arguments')),
        ))
        db.send_create_signal('storedprocs', ['StoredProcedureArguments'])


    def backwards(self, orm):
        # Deleting model 'StoredProcedure'
        db.delete_table('storedprocs_storedprocedure')

        # Deleting model 'StoredProcedureArguments'
        db.delete_table('storedprocs_storedprocedurearguments')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'storedprocs.storedprocedure': {
            'Meta': {'object_name': 'StoredProcedure'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primitive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'primitive_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'return_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sql': ('django.db.models.fields.TextField', [], {})
        },
        'storedprocs.storedprocedurearguments': {
            'Meta': {'object_name': 'StoredProcedureArguments'},
            'arg_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'argument_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storedprocs.StoredProcedure']", 'related_name': "'arguments'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['storedprocs']