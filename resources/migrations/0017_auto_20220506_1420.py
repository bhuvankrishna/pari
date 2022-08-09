# Generated by Django 2.2 on 2022-05-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0016_auto_20220505_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('as', 'Assamese'), ('bn', 'Bengali'), ('gu', 'Gujarati'), ('hi', 'Hindi'), ('hin', 'Chhattisgarhi'), ('kn', 'Kannada'), ('ml', 'Malayalam'), ('mr', 'Marathi'), ('lus', 'Mizo'), ('or', 'Odia'), ('pa', 'Punjabi'), ('te', 'Telugu'), ('ta', 'Tamil'), ('ur', 'Urdu'), ('fr', 'French'), ('hne', 'Chhattisgarhi')], max_length=7),
        ),
    ]
