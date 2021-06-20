# Generated by Django 2.2 on 2021-06-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users_reviewed', models.ManyToManyField(related_name='Books', to='dojo_app.User')),
            ],
        ),
    ]
