# Generated by Django 4.2.1 on 2023-05-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customing_app', '0009_remove_colorscheme_card_colorscheme_font_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorscheme',
            name='button_shape',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='colorscheme',
            name='button_type',
            field=models.IntegerField(default=1),
        ),
    ]
