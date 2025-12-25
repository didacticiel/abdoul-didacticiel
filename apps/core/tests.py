from django.test import TestCase
from django.urls import reverse
from apps.portfolio.models import Project # Imaginons que tu as un modèle Project

class PortfolioTests(TestCase):
    
    # LOGIQUE : Préparer des données fictives pour les tests
    def setUp(self):
        self.project = Project.objects.create(
            title="Mon Super Projet",
            description="Une description courte",
            technologies="Django, Tailwind"
        )

    # LOGIQUE : Test de l'affichage de la liste des projets
    def test_portfolio_list_view(self):
        response = self.client.get(reverse('portfolio:list'))
        self.assertEqual(response.status_code, 200)
        # On vérifie si le titre de notre projet est bien présent dans le HTML
        self.assertContains(response, "Mon Super Projet")

    # LOGIQUE : Test de sécurité du formulaire de contact
    def test_contact_form_invalid_email(self):
        url = reverse('core:contact')
        data = {
            'name': 'Abdoul',
            'email': 'mauvais-email', # Email invalide
            'message': 'Hello!'
        }
        response = self.client.post(url, data)
        # Si l'email est invalide, Django doit renvoyer une erreur (souvent reste sur la page)
        self.assertFormError(response, 'form', 'email', 'Saisissez une adresse électronique valide.')