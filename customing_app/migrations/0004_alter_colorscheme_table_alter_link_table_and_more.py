# Generated by Django 4.1.2 on 2022-10-09 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customing_app', '0003_alter_profile_colors'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='colorscheme',
            table='ColorScheme',
        ),
        migrations.AlterModelTable(
            name='link',
            table='Links',
        ),
        migrations.AlterModelTable(
            name='profile',
            table='Profiles',
        ),
    ]
