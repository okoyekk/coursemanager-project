# Generated by Django 3.1.4 on 2021-07-07 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classmanager', '0004_course_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='credits',
            field=models.PositiveIntegerField(default=2),
        ),
    ]