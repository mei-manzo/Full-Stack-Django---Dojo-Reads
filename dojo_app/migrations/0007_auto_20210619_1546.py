# Generated by Django 2.2 on 2021-06-19 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_app', '0006_auto_20210619_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='User',
            new_name='user',
        ),
    ]