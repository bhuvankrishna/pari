# Generated by Django 2.2 on 2022-05-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0017_auto_20220506_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('as', 'Assamese'), ('bn', 'Bengali'), ('gu', 'Gujarati'), ('hi', 'Hindi'), ('kn', 'Kannada'), ('ml', 'Malayalam'), ('mr', 'Marathi'), ('lus', 'Mizo'), ('or', 'Odia'), ('pa', 'Punjabi'), ('te', 'Telugu'), ('ta', 'Tamil'), ('ur', 'Urdu'), ('fr', 'French'), ('ge', 'German'), ('hne', 'Chhattisgarhi')], max_length=7),
        ),
    ]
