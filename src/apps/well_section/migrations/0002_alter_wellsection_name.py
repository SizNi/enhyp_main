# Generated by Django 4.2.4 on 2023-12-05 22:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("well_section", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wellsection",
            name="name",
            field=models.TextField(),
        ),
    ]
