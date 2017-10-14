# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Autocomplete(models.Model):
    query = models.TextField(primary_key=True, max_length=1024)

    class Meta:
        managed = False
        db_table = 'autocomplete'


'''class CurrentDepth(models.Model):
    link = models.CharField(db_column='Link', primary_key=True, max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'current_depth'


class NextDepth(models.Model):
    link = models.CharField(db_column='Link', primary_key=True, max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'next_depth'

'''
class WebPages(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    link = models.TextField(db_column='Link', unique=True, max_length=1024)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    visited = models.IntegerField(db_column='Visited', blank=True, null=True)  # Field name made lowercase.
    indexed = models.IntegerField(db_column='Indexed', blank=True, null=True)  # Field name made lowercase.
    lastvisited = models.DateTimeField(db_column='LastVisited', blank=True, null=True)  # Field name made lowercase.
    frequency = models.IntegerField(db_column='Frequency', blank=True, null=True)  # Field name made lowercase.
    popularity = models.IntegerField(db_column='Popularity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'web_pages'
