# Generated by Django 3.1.4 on 2020-12-10 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_auto_20201210_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='pronunciation',
            new_name='pronunciation_en',
        ),
    ]