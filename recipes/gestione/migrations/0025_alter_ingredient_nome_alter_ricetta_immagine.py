# Generated by Django 4.1.1 on 2022-09-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestione", "0024_alter_ricetta_immagine"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="nome",
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="ricetta",
            name="immagine",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
