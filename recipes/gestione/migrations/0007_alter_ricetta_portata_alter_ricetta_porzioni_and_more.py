# Generated by Django 4.1.1 on 2022-09-23 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestione", "0006_alter_ricetta_utente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ricetta",
            name="portata",
            field=models.CharField(
                choices=[
                    ("1", "Antipasto"),
                    ("2", "Primo"),
                    ("3", "Secondo"),
                    ("4", "Dolce"),
                ],
                default="primo",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="ricetta", name="porzioni", field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name="ricetta",
            name="regime_alimentare",
            field=models.CharField(
                choices=[("1", "Vegetariano"), ("2", "Vegano"), ("3", "Nessuno")],
                default="veg",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="ricetta",
            name="tempo_cottura",
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="ricetta",
            name="tempo_preparazione",
            field=models.IntegerField(default=20),
        ),
    ]
