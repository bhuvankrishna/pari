# Generated by Django 2.2 on 2021-06-09 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0023_auto_20210519_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='translators',
        ),
    ]
