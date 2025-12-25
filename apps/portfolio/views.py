# ═══════════════════════════════════════════════════════════════
# apps/portfolio/views.py
# ═══════════════════════════════════════════════════════════════
"""
LOGIQUE DES VIEWS :

Django suit le pattern MTV (Model-Template-View) :
- Model : données (models.py)
- Template : présentation (HTML)
- View : logique métier (views.py)

TYPES DE VIEWS :
1. Function-Based Views (FBV) : fonctions simples
2. Class-Based Views (CBV) : classes réutilisables

HTMX INTEGRATION :
- request.htmx : Django-HTMX middleware détecte les requêtes HTMX
- render() avec template différent si HTMX (partials)
- JsonResponse pour updates dynamiques
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Project, Category, Technology


# ─────────────────────────────────────────────────────────────
# Vue Liste Portfolio (avec filtres HTMX)
# ─────────────────────────────────────────────────────────────
class PortfolioListView(ListView):
    """
    CLASS-BASED VIEW pour lister les projets.
    
    HÉRITAGE DE ListView :
    - model : définit automatiquement le queryset
    - template_name : template à utiliser
    - context_object_name : nom de la variable dans le template
    - paginate_by : active la pagination automatique
    
    MÉTHODES OVERRIDES :
    - get_queryset() : personnalise la requête DB
    - get_context_data() : ajoute des données au contexte template
    """
    model = Project
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'projects'  # Dans le template : {{ projects }}
    paginate_by = 9  # 9 projets par page

    def get_queryset(self):
        """
        PERSONNALISE LA REQUÊTE BASE DE DONNÉES.
        
        LOGIQUE :
        1. Commence avec tous les projets publiés
        2. Applique les filtres si présents dans l'URL (?category=web)
        3. Optimise avec select_related/prefetch_related
        
        OPTIMISATIONS :
        - select_related('category') : JOINture SQL (1 seule requête)
        - prefetch_related('technologies') : requête séparée optimisée (ManyToMany)
        - Sans ces optimisations → N+1 queries problem
        """
        # Queryset de base : projets publiés, triés par ordre
        queryset = Project.objects.filter(is_published=True).select_related('category').prefetch_related('technologies')
        
        # ───── FILTRE PAR CATÉGORIE ─────
        # Récupère le paramètre GET : /portfolio/?category=web
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            # Filtre les projets par slug de catégorie
            queryset = queryset.filter(category__slug=category_slug)
        
        # ───── FILTRE PAR TECHNOLOGIE ─────
        tech_slug = self.request.GET.get('technology')
        if tech_slug:
            # Filtre par technologie (relation ManyToMany)
            queryset = queryset.filter(technologies__slug=tech_slug)
        
        # ───── RECHERCHE TEXTUELLE ─────
        search_query = self.request.GET.get('search')
        if search_query:
            # Q objects : permet des requêtes OR complexes
            # Recherche dans title OU description (icontains = insensible à la casse)
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # ───── TRI ─────
        sort_by = self.request.GET.get('sort', 'order')  # Défaut : par ordre
        if sort_by == 'recent':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-views_count')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        AJOUTE DES DONNÉES AU CONTEXTE DU TEMPLATE.
        
        kwargs contient déjà : 'projects', 'page_obj', 'paginator'
        On ajoute : categories, technologies, filtres actifs
        """
        # Récupère le contexte de base de ListView
        context = super().get_context_data(**kwargs)
        
        # ───── AJOUTE LES CATÉGORIES ACTIVES ─────
        context['categories'] = Category.objects.filter(is_active=True)
        
        # ───── AJOUTE LES TECHNOLOGIES (avec comptage) ─────
        # annotate(project_count=Count('projects')) : ajoute un champ calculé
        context['technologies'] = Technology.objects.annotate(
            project_count=Count('projects')
        ).filter(project_count__gt=0)  # Seulement les technos utilisées
        
        # ───── FILTRES ACTIFS (pour affichage UI) ─────
        context['active_category'] = self.request.GET.get('category', 'all')
        context['active_tech'] = self.request.GET.get('technology', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['active_sort'] = self.request.GET.get('sort', 'order')
        
        # ───── COMPTAGE TOTAL ─────
        context['total_projects'] = self.get_queryset().count()
        
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        GESTION HTMX : retourne un template différent si requête HTMX.
        
        LOGIQUE :
        - Requête normale : retourne la page complète (avec navbar, footer)
        - Requête HTMX : retourne seulement le fragment HTML (grille de projets)
        
        request.htmx : middleware Django-HTMX détecte si requête vient de HTMX
        """
        if self.request.htmx:
            # Template partiel pour HTMX (seulement la grille)
            self.template_name = 'portfolio/partials/project_grid.html'
        
        return super().render_to_response(context, **response_kwargs)


# ─────────────────────────────────────────────────────────────
# Vue Détail Projet
# ─────────────────────────────────────────────────────────────
class ProjectDetailView(DetailView):
    """
    DÉTAIL D'UN PROJET.
    
    DetailView cherche automatiquement par slug grâce à :
    - URL pattern avec <slug:slug>
    - slug_field et slug_url_kwarg
    """
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'  # Champ du model à utiliser
    slug_url_kwarg = 'slug'  # Nom du paramètre dans l'URL

    def get_queryset(self):
        """Optimise la requête avec relations"""
        return Project.objects.select_related('category').prefetch_related('technologies')

    def get_object(self, queryset=None):
        """
        OVERRIDE pour incrémenter les vues.
        
        LOGIQUE :
        1. Récupère l'objet normalement
        2. Incrémente le compteur de vues
        3. Retourne l'objet
        """
        obj = super().get_object(queryset)
        
        # Incrémente seulement si ce n'est pas le propriétaire (optionnel)
        # if not self.request.user.is_staff:
        obj.increment_views()
        
        return obj

    def get_context_data(self, **kwargs):
        """Ajoute les projets similaires au contexte"""
        context = super().get_context_data(**kwargs)
        
        # ───── PROJETS SIMILAIRES ─────
        # Logique : même catégorie, excluant le projet actuel
        context['related_projects'] = Project.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(
            pk=self.object.pk  # Exclut le projet actuel
        ).select_related('category')[:3]  # Limite à 3 projets
        
        # ───── NAVIGATION PRÉCÉDENT/SUIVANT ─────
        # Projet précédent (order inférieur)
        context['previous_project'] = Project.objects.filter(
            order__lt=self.object.order,
            is_published=True
        ).order_by('-order').first()
        
        # Projet suivant (order supérieur)
        context['next_project'] = Project.objects.filter(
            order__gt=self.object.order,
            is_published=True
        ).order_by('order').first()
        
        return context


# ─────────────────────────────────────────────────────────────
# Vue HTMX : Filtre rapide par catégorie
# ─────────────────────────────────────────────────────────────
def filter_projects_htmx(request):
    """
    FUNCTION-BASED VIEW pour filtrage HTMX rapide.
    
    USAGE : appelée par HTMX lors du clic sur un bouton de filtre.
    Retourne uniquement la grille de projets (HTML partiel).
    
    EXEMPLE HTMX dans le template :
    <button hx-get="{% url 'portfolio:filter_projects' %}?category=web"
            hx-target="#projects-grid"
            hx-swap="innerHTML">
        Web Dev
    </button>
    """
    # Récupère les paramètres de filtre
    category_slug = request.GET.get('category', 'all')
    
    # Construit le queryset filtré
    projects = Project.objects.filter(is_published=True).select_related('category').prefetch_related('technologies')
    
    if category_slug != 'all':
        projects = projects.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Contexte pour le template partiel
    context = {
        'projects': page_obj,
        'page_obj': page_obj,
    }
    
    # Retourne SEULEMENT le fragment HTML
    return render(request, 'portfolio/partials/project_grid.html', context)


# ─────────────────────────────────────────────────────────────
# Vue HTMX : Charger plus de projets (pagination infinie)
# ─────────────────────────────────────────────────────────────
def load_more_projects_htmx(request):
    """
    PAGINATION INFINIE avec HTMX.
    
    LOGIQUE :
    1. Récupère la page demandée
    2. Retourne les projets de cette page
    3. HTMX les ajoute à la suite (hx-swap="beforeend")
    
    EXEMPLE HTMX :
    <button hx-get="{% url 'portfolio:load_more' %}?page={{ page_obj.next_page_number }}"
            hx-target="#projects-grid"
            hx-swap="beforeend">
        Charger plus
    </button>
    """
    page_number = request.GET.get('page', 1)
    category_slug = request.GET.get('category', 'all')
    
    # Queryset filtré
    projects = Project.objects.filter(is_published=True).select_related('category').prefetch_related('technologies')
    
    if category_slug != 'all':
        projects = projects.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(projects, 9)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'page_obj': page_obj,
    }
    
    # Template partiel : seulement les cards de projets
    return render(request, 'portfolio/partials/project_cards.html', context)


# ─────────────────────────────────────────────────────────────
# Vue API JSON : Comptage projets par catégorie (pour UI)
# ─────────────────────────────────────────────────────────────
def projects_count_api(request):
    """
    API JSON pour mettre à jour dynamiquement le compteur.
    
    USAGE : appelée par HTMX ou JavaScript
    Retourne : { "count": 12, "category": "Web Dev" }
    """
    category_slug = request.GET.get('category', 'all')
    
    if category_slug == 'all':
        count = Project.objects.filter(is_published=True).count()
        category_name = "Tous les projets"
    else:
        category = get_object_or_404(Category, slug=category_slug)
        count = Project.objects.filter(is_published=True, category=category).count()
        category_name = category.name
    
    return JsonResponse({
        'count': count,
        'category': category_name,
        'slug': category_slug
    })
