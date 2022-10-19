from django.test import TestCase
from .views import *
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test.utils import setup_test_environment


# Create your tests here.


class ListViewTests(TestCase):
    def test_lista_ricette_with_no_ricette(self):
        """
        No ricette --> "Non ci sono ricette in questa categoria" dovrebbe essere mostrato
        """

        # non creo nessuna ricetta

        response = self.client.get(reverse("listaricette"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non ci sono ricette in questa categoria")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_lista_ricette_with_due_ricetta(self):
        """
        Se c'é piú di una qualsiasi ricetta, dovrebbe essere mostrate tutte
        """

        # creo una ricetta
        r1 = Ricetta.objects.create(nome="r1")
        r2 = Ricetta.objects.create(nome="r2")

        response = self.client.get(reverse("listaricette"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], [r1, r2], ordered=False)

    def test_lista_ricette_with_una_ricetta(self):
        """
        Se c'é una qualsiasi ricetta, dovrebbe essere mostrata
        """

        # creo una ricetta
        r1 = Ricetta.objects.create(nome="Ricetta 1")

        response = self.client.get(reverse("listaricette"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], [r1])


class RicettaDetailViewTests(TestCase):
    def test_funzioni_per_persone_loggate_non_attive_quando_utente_non_loggato(self):
        r1 = Ricetta.objects.create(nome='ricetta 1')

        response = self.client.get(reverse("ricetta", kwargs={"ricetta_id": r1.id}))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Aggiungi ai preferiti")
        self.assertNotContains(response, "Valuta")

    def test_funzioni_per_persone_loggate_attive_quando_utente_e_loggato(self):
        # Creo utente e ricetta dell'utente
        self.user = User.objects.create_user(username='davide', email='davide@prova.it', password='davide')
        r1 = Ricetta.objects.create(nome='ricetta 1', utente=self.user)

        # eseguo il login #
        self.client.login(username="davide", password="davide")

        # tests #
        response = self.client.get(reverse("ricetta", kwargs={"ricetta_id": r1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aggiungi ai preferiti")
        self.assertContains(response, "Valuta")

    def test_modifica_e_cancellazione_se_utente_e_proprietario_ricetta(self):
        # Creo utente e ricetta dell'utente
        self.user = User.objects.create_user(username='davide', email='davide@prova.it', password='davide')
        r1 = Ricetta.objects.create(nome='ricetta 1', utente=self.user)

        # eseguo il login #
        self.client.login(username="davide", password="davide")

        # tests #
        response = self.client.get(reverse("ricetta", kwargs={"ricetta_id": r1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modifica Ricetta")
        self.assertContains(response, "Cancella Ricetta")


    def test_modifica_e_cancellazione_se_utente_non_e_proprietario_ricetta(self):
        # Creo utenti e ricetta dell'utente
        self.user = User.objects.create_user(username='davide', email='davide@prova.it', password='davide')
        self.user_no_proprietario = User.objects.create_user(username='d', email='d@prova.it', password='d')
        r1 = Ricetta.objects.create(nome='ricetta 1', utente=self.user)

        # eseguo il login #
        self.client.login(username="d", password="d")

        # tests #
        response = self.client.get(reverse("ricetta", kwargs={"ricetta_id": r1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Modifica Ricetta")
        self.assertNotContains(response, "Cancella Ricetta")
