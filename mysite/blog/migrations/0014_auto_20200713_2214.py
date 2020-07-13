# Generated by Django 2.2 on 2020-07-13 14:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200713_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAlgorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='algorithm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.BlogAlgorithm'),
        ),
    ]