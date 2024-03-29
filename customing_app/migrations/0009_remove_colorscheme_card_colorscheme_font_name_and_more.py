# Generated by Django 4.2.1 on 2023-05-21 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customing_app', '0008_remove_colorscheme_button_click_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colorscheme',
            name='card',
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='font_name',
            field=models.CharField(default='#FFFFFF', max_length=8, verbose_name='font name'),
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='outline',
            field=models.CharField(default='#172C38', max_length=8, verbose_name='outline'),
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='shadow',
            field=models.CharField(default='#FFFFFF', max_length=8, verbose_name='shadow'),
        ),
    ]
