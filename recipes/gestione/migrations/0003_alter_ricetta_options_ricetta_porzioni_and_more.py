# Generated by Django 4.1.1 on 2022-09-19 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestione", "0002_ricetta_costo_ricetta_portata_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ricetta", options={"verbose_name_plural": "Ricette"},
        ),
        migrations.AddField(
            model_name="ricetta",
            name="porzioni",
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name="ricetta",
            name="tempo_cottura",
            field=models.CharField(default="10", max_length=4),
        ),
        migrations.AddField(
            model_name="ricetta",
            name="tempo_preparazione",
            field=models.CharField(default="20", max_length=5),
        ),
    ]
