# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-08 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTagRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('tag_id', models.IntegerField()),
            ],
        ),
    ]