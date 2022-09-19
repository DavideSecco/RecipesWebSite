from gestione.models import Ricetta
from django.utils import timezone
from datetime import datetime

def erase_db():
    print("cancello il db")
    Ricetta.objects.all().delete()


def init_db():
    if len(Ricetta.objects.all()) != 0:
        return

    ricettedict = {
        "nome" : ['provaaaa', "Lasagne", "Tigelle"],
        "difficoltá" : ["bassa", "bassa", "bassa"],
        "regime_alimentare" : ["vegetariano", "vegetariano", "vegetariano"],
        "portata" : ["primo", "primo", "primo"],
        "costo" : [20,20,20],
        # "porzioni" : [20,20,20],
        #"tempo_preparazione" : ["20","30","40"],
        #"tempo_cottura" : ["20","30","40"],
    }

    for k in ricettedict:
        print(str(ricettedict[k]))

    for i in range(3):
        print("salvo ricetta " + str(i))
        r = Ricetta()
        for k in ricettedict:
            print("K = " + k + " i = " + str(i) + " quindi: " + str(ricettedict[k][i]))
            if k == "nome":
                r.nome = ricettedict[k][i],
                # print("trovato nome")
            if k == "difficoltá":
                r.difficoltá = ricettedict[k][i],
                # print("trovato difficoltá")
            if k == "tempo_preparazione":
                r.tempo_preparazione = ricettedict[k][i],
                # print("trovato tempo prep")
            if k == "tempo_cottura":
                r.tempo_cottura = ricettedict[k][i],
            if k == "porzioni":
                r.porzioni = ricettedict[k][i],
            if k == "costo":
                r.costo = ricettedict[k][i]
                print("trovato costo")
            if k == "regime_alimentare":
                r.regime_alimentare = ricettedict[k][i],
                # print("trovato reg alimentare")
            if k == "portata":
                r.portata = ricettedict[k][i],
        r.save()

    print("DUMP DB")
    # print(Ricetta.objects.all())