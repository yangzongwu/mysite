# Generated by Django 2.2 on 2020-07-13 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0006_auto_20200428_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ('-updated_time',)},
        ),
    ]
