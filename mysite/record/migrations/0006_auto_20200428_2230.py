# Generated by Django 2.2 on 2020-04-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0005_auto_20200428_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='feed_back',
            field=models.TextField(blank=True, default='unfinished'),
        ),
    ]
