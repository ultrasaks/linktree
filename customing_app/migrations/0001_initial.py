# Generated by Django 4.1.2 on 2022-10-09 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorScheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background', models.CharField(default='#15151E', max_length=8)),
                ('font', models.CharField(default='#15151E', max_length=8)),
                ('card', models.CharField(default='#15151E', max_length=8)),
                ('button', models.CharField(default='#15151E', max_length=8)),
                ('button_font', models.CharField(default='#15151E', max_length=8)),
                ('button_hover', models.CharField(default='#15151E', max_length=8)),
                ('button_click', models.CharField(default='#15151E', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=400)),
                ('colors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customing_app.colorscheme')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='link', max_length=100)),
                ('url', models.CharField(max_length=400)),
                ('title', models.CharField(max_length=100)),
                ('solid', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customing_app.profile')),
            ],
        ),
    ]