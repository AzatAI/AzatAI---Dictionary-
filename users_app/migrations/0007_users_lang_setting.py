# Generated by Django 3.1.4 on 2020-12-18 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0006_users_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='lang_setting',
            field=models.CharField(default='en', max_length=5),
        ),
    ]