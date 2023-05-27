# Generated by Django 4.1.2 on 2023-05-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customing_app', '0007_link_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colorscheme',
            name='button_click',
        ),
        migrations.RemoveField(
            model_name='colorscheme',
            name='button_hover',
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='button_shape',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='button_type',
            field=models.IntegerField(default=0),
        ),
    ]