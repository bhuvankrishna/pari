# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20170124_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='modular_content',
            field=wagtail.wagtailcore.fields.StreamField([('image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image')), (b'caption', wagtail.wagtailcore.blocks.CharBlock())]))], null=True, blank=True),
        ),
    ]
