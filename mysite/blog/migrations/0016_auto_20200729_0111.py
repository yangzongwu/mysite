# Generated by Django 2.2 on 2020-07-28 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20200713_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='view_ip',
            name='national',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='view_ip_history',
            name='national',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
