# Generated by Django 4.2.4 on 2023-10-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hydrants", "0002_alter_hydrant_options_alter_owner_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hydrant",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="hydrants/images/", verbose_name="Фото"
            ),
        ),
    ]
