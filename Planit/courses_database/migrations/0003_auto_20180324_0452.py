# Generated by Django 2.0.1 on 2018-03-24 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_database', '0002_auto_20180324_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='description',
            field=models.CharField(default='penis', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='location',
            field=models.CharField(default='penis2', max_length=200),
            preserve_default=False,
        ),
    ]
