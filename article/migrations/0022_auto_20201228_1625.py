# Generated by Django 2.2 on 2020-12-28 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0021_auto_20201204_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleauthors',
            name='role',
            field=models.CharField(blank=True, choices=[('Photo', 'Photo'), ('Text', 'Text'), ('Illustration', 'Illustration'), ('Video editor', 'Video editor')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='articleauthors',
            name='show_in_beginning',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='articleauthors',
            name='show_in_end',
            field=models.BooleanField(default=True),
        ),
    ]
