# Generated by Django 4.1.2 on 2022-10-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0041_alter_recensione_punteggio_ricettepreferite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricetta',
            name='difficoltá',
            field=models.CharField(choices=[('0', ''), ('Bassa', 'Bassa'), ('Media', 'Media'), ('Alta', 'Alta')], default='Bassa', max_length=50),
        ),
    ]
