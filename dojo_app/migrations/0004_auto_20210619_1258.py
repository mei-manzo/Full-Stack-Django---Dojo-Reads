# Generated by Django 2.2 on 2021-06-19 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_app', '0003_book_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='alias',
        ),
    ]