# Generated by Django 2.2 on 2022-11-07 07:05

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0014_album_freedom_fighters_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumslide',
            name='embed',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]