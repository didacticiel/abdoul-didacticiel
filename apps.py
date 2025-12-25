# apps/users/apps.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = _("Gestion des Utilisateurs")
    
    # 💡 La méthode ready() est appelée APRÈS que toutes les applications sont chargées.
    def ready(self):
        try:
            # Importation locale pour éviter les problèmes de chargement circulaire
            from django.contrib import admin
            
            # Application de la personnalisation
            admin.site.site_title = "Abdoul Didacticiel"
            admin.site.site_header = "Administration de Abdoul Didacticiel"
            admin.site.index_title = "Tableau de Bord Administratif"
            
        except ImportError:
            # Si l'environnement de test ou autre n'a pas besoin de l'admin
            pass