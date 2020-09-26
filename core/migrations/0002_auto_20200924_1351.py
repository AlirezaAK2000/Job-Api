# Generated by Django 3.1 on 2020-09-24 13:51

import core.models
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empolyee',
            name='fields',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dev', 'development'), ('des', 'design'), ('fam', 'farming'), ('ter', 'translating'), ('tra', 'transformation'), ('con', 'content management'), ('led', 'leading'), ('acc', 'accounting'), ('ins', 'insurance')], max_length=3),
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ex_date', models.DateField(blank=True, default=core.models.one_month_from_today, null=True, verbose_name='Expiration Date')),
                ('field', models.CharField(choices=[('dev', 'development'), ('des', 'design'), ('fam', 'farming'), ('ter', 'translating'), ('tra', 'transformation'), ('con', 'content management'), ('led', 'leading'), ('acc', 'accounting'), ('ins', 'insurance')], max_length=3)),
                ('salary', models.FloatField()),
                ('hw', models.SmallIntegerField(verbose_name='hours of work')),
                ('requierments', models.TextField()),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.employer')),
            ],
        ),
    ]