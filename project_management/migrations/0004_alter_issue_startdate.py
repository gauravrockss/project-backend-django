# Generated by Django 5.0.7 on 2024-08-05 08:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_remove_issue_count_remove_issue_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='startDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]