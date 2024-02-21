

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name="Notes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("noteText", models.TextField()),
            ],
        ),
    ]
