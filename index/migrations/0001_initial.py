# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user1', models.CharField(default='Client', max_length=200)),
                ('user2', models.CharField(default='toComputer', max_length=200)),
                ('query', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]
