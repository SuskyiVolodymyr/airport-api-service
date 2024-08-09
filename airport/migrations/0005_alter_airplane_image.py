# Generated by Django 5.0.8 on 2024-08-09 15:11

import airport.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0004_airplane_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airplane",
            name="image",
            field=models.ImageField(
                null=True, upload_to=airport.models.airplane_image_file_path
            ),
        ),
    ]
