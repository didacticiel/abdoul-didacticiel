# ═══════════════════════════════════════════════════════════════
# apps/portfolio/urls.py
# ═══════════════════════════════════════════════════════════════
"""
LOGIQUE DES URLs :

ROUTING : Définit les URL patterns et les lie aux views.

SYNTAXE :
- path('url/', view, name='name')
- <type:name> : paramètre dynamique (ex: <slug:slug>)

TYPES DE PARAMÈTRES :
- <int:id> : entier
- <slug:slug> : slug (lettres, chiffres, tirets, underscores)
- <str:text> : chaîne
- <uuid:uuid> : UUID

NAME : permet d'inverser l'URL dans les templates
Template : {% url 'portfolio:project_detail' slug='mon-projet' %}
Python : reverse('portfolio:project_detail', kwargs={'slug': 'mon-projet'})
"""

from django.urls import path
from . import views

# NAMESPACE : préfixe pour éviter les conflits
# Usage : {% url 'portfolio:list' %} au lieu de {% url 'list' %}
app_name = 'portfolio'

urlpatterns = [
    # ───── PAGE LISTE PORTFOLIO ─────
    # URL : /portfolio/
    # View : Class-Based View (utilise .as_view())
    path('', 
         views.PortfolioListView.as_view(), 
         name='list'),
    
    # ───── PAGE DÉTAIL PROJET ─────
    # URL : /portfolio/nexus-bank/
    # Paramètre : slug (capturé et passé à la view)
    path('<slug:slug>/', 
         views.ProjectDetailView.as_view(), 
         name='project_detail'),
    
    # ───── ENDPOINTS HTMX ─────
    # Ces URLs sont appelées par HTMX, pas directement par l'utilisateur
    
    # Filtrage dynamique
    # URL : /portfolio/filter/?category=web
    path('htmx/filter/', 
         views.filter_projects_htmx, 
         name='filter_projects'),
    
    # Pagination infinie
    # URL : /portfolio/htmx/load-more/?page=2
    path('htmx/load-more/', 
         views.load_more_projects_htmx, 
         name='load_more'),
    
    # ───── API JSON ─────
    # Comptage de projets (pour mise à jour UI)
    # URL : /portfolio/api/count/?category=web
    path('api/count/', 
         views.projects_count_api, 
         name='projects_count'),
]
