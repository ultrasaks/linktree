# Generated by Django 4.1.2 on 2022-10-09 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'пользователя', 'verbose_name_plural': 'пользователи'},
        ),
    ]