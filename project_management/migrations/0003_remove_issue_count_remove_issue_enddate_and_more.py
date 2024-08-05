# Generated by Django 5.0.7 on 2024-08-05 08:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0002_rename_end_date_issue_enddate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='count',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='endDate',
        ),
        migrations.AlterField(
            model_name='issue',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]