# Generated by Django 4.2.4 on 2023-08-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zso", "0003_zso_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="zso",
            name="project_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
