# Generated by Django 3.1.4 on 2020-12-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20201210_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='text_en',
            field=models.CharField(max_length=300000),
        ),
    ]