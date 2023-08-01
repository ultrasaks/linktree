# Generated by Django 4.2.1 on 2023-07-31 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customing_app', '0012_colorscheme_avatar_shape_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название шрифта')),
                ('img_name', models.CharField(max_length=40, verbose_name='картинка')),
            ],
            options={
                'verbose_name': 'шрифт',
                'verbose_name_plural': 'шрифты',
                'db_table': 'Fonts',
            },
        ),
        migrations.AlterField(
            model_name='colorscheme',
            name='avatar_shape',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
