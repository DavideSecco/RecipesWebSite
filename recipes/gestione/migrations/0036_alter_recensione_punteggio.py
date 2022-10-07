# Generated by Django 4.1.1 on 2022-10-02 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestione", "0035_alter_recensione_punteggio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recensione",
            name="punteggio",
            field=models.IntegerField(
                choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")], default="1"
            ),
        ),
    ]