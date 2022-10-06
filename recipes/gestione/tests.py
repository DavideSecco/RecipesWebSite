from django.test import TestCase
from .views import *
from django.urls import reverse_lazy
from django.urls import reverse

# Create your tests here.

##### funzioni di servizio #####
def create_ricetta(nome):
    return Ricetta.objects.create(nome=nome)

# teestare il comportamento della view "lista ricette" se non ci sono ricette
class ListViewTests(TestCase):
    def test_lista_ricette_with_no_ricette(self):
        """
        No ricette --> "Non ci sono ricette in questa categoria"
        dovrebbe essere mostrato
        """

        # non creo nessuna ricetta
        response = self.client.get(reverse("listaricette"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non ci sono ricette in questa categoria")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_lista_ricette_with_una_ricetta(self):
        """
        Se c'é una qualsiasi ricetta, dovrebbe essere mostrata
        """

        # creo una ricetta
        r1 = create_ricetta("Ricetta 1")

        response = self.client.get(reverse("listaricette"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], [r1])




