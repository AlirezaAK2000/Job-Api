# Generated by Django 3.1 on 2020-09-25 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200925_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='max_salary',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='min_salary',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='salary',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]