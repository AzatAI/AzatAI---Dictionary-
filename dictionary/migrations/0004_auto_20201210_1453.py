# Generated by Django 3.1.4 on 2020-12-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_auto_20201210_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='text_en',
            field=models.TextField(max_length=30000),
        ),
    ]
