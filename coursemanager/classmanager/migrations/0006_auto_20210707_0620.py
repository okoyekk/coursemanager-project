# Generated by Django 3.1.4 on 2021-07-07 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classmanager', '0005_course_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='date_joined',
            field=models.DateField(auto_now_add=True),
        ),
    ]
