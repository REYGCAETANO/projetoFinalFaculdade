# Generated by Django 2.1.2 on 2020-10-15 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradehoraria', '0008_auto_20201015_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrosgrade',
            name='taxaMutacao',
            field=models.FloatField(verbose_name='Taxa de Mutação'),
        ),
    ]
