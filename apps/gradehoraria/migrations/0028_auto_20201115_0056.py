# Generated by Django 2.1.2 on 2020-11-15 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradehoraria', '0027_grade_cd_curso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='cd_curso',
        ),
        migrations.AddField(
            model_name='grade',
            name='resultado',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
