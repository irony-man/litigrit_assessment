# Generated by Django 5.1.7 on 2025-03-19 22:55

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Summary",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("extracted_text", models.TextField()),
                ("attachment", models.FileField(upload_to="attachments/")),
                ("title", models.CharField(max_length=255)),
                ("summary", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Summaries",
            },
        ),
    ]
