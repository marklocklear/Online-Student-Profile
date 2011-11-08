# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PersonalityTypeResult'
        db.create_table('assessments_personalitytyperesult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('personality_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('first_category_score', self.gf('django.db.models.fields.IntegerField')()),
            ('second_category_score', self.gf('django.db.models.fields.IntegerField')()),
            ('third_category_score', self.gf('django.db.models.fields.IntegerField')()),
            ('fourth_category_score', self.gf('django.db.models.fields.IntegerField')()),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('assessments', ['PersonalityTypeResult'])

        # Adding model 'LearningStyleResult'
        db.create_table('assessments_learningstyleresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('learning_style', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kinesthetic_score', self.gf('django.db.models.fields.IntegerField')()),
            ('visual_score', self.gf('django.db.models.fields.IntegerField')()),
            ('auditory_score', self.gf('django.db.models.fields.IntegerField')()),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('assessments', ['LearningStyleResult'])


    def backwards(self, orm):
        
        # Deleting model 'PersonalityTypeResult'
        db.delete_table('assessments_personalitytyperesult')

        # Deleting model 'LearningStyleResult'
        db.delete_table('assessments_learningstyleresult')


    models = {
        'assessments.learningstyleresult': {
            'Meta': {'object_name': 'LearningStyleResult'},
            'answers': ('django.db.models.fields.TextField', [], {}),
            'auditory_score': ('django.db.models.fields.IntegerField', [], {}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kinesthetic_score': ('django.db.models.fields.IntegerField', [], {}),
            'learning_style': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'visual_score': ('django.db.models.fields.IntegerField', [], {})
        },
        'assessments.personalitytyperesult': {
            'Meta': {'object_name': 'PersonalityTypeResult'},
            'answers': ('django.db.models.fields.TextField', [], {}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_category_score': ('django.db.models.fields.IntegerField', [], {}),
            'fourth_category_score': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'personality_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'second_category_score': ('django.db.models.fields.IntegerField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'third_category_score': ('django.db.models.fields.IntegerField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assessments']
