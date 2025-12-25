# ═══════════════════════════════════════════════════════════════
# apps/portfolio/admin.py
# ═══════════════════════════════════════════════════════════════
"""
ADMIN DJANGO : Interface d'administration automatique.

PERSONNALISATION :
- list_display : colonnes affichées dans la liste
- list_filter : filtres latéraux
- search_fields : champs inclus dans la recherche
- prepopulated_fields : auto-remplissage (ex: slug depuis title)
- readonly_fields : champs non modifiables
- inlines : models liés affichés dans le même formulaire
"""

from django.contrib import admin
from .models import Project, Category, Technology


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    ADMIN PERSONNALISÉ pour Category.
    
    prepopulated_fields : auto-génère le slug pendant la saisie du name
    """
    list_display = ['name', 'slug', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}  # Auto-génère slug depuis name
    list_editable = ['is_active']  # Éditable directement dans la liste


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    ADMIN AVANCÉ pour Project.
    
    FONCTIONNALITÉS :
    - Filtres multiples
    - Recherche full-text
    - Édition rapide (list_editable)
    - Tri par drag & drop (grâce à order)
    - Champs readonly (created_at, views_count)
    - Filter horizontal pour ManyToMany (interface améliorée)
    """
    list_display = [
        'title', 
        'category', 
        'year', 
        'is_featured', 
        'is_published', 
        'order', 
        'views_count',
        'created_at'
    ]
    
    list_filter = [
        'is_published', 
        'is_featured', 
        'category', 
        'year',
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'description', 
       # 'content,
        'category__name',
        'technologies__name'
    ]