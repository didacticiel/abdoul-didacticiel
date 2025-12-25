# ═══════════════════════════════════════════════════════════════
# apps/portfolio/models.py
# ═══════════════════════════════════════════════════════════════
"""
LOGIQUE DES MODELS :
Les models Django sont des classes Python qui représentent vos tables de base de données.
Chaque attribut de classe = une colonne dans la table.
Django génère automatiquement le SQL pour créer ces tables.

HÉRITAGE : 
- models.Model : classe de base obligatoire
- TimeStampedModel : mixin personnalisé pour created_at/updated_at

RELATIONS :
- ForeignKey : relation Many-to-One (plusieurs projets → une catégorie)
- ManyToManyField : relation Many-to-Many (un projet peut avoir plusieurs technos)

MÉTHODES SPÉCIALES :
- __str__() : représentation textuelle de l'objet (dans l'admin Django)
- get_absolute_url() : URL canonique de l'objet
- @property : transforme une méthode en attribut (pas besoin de parenthèses)
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# ─────────────────────────────────────────────────────────────
# Mixin pour timestamps automatiques
# ─────────────────────────────────────────────────────────────
class TimeStampedModel(models.Model):
    """
    MIXIN : Classe abstraite réutilisable qui ajoute created_at et updated_at
    à tous les models qui en héritent.
    
    abstract = True : Django ne créera PAS de table pour ce model,
    il sert uniquement de base pour d'autres models.
    
    auto_now_add=True : Se remplit automatiquement à la création
    auto_now=True : Se met à jour automatiquement à chaque sauvegarde
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        abstract = True  # Ce model ne sera pas une table réelle


# ─────────────────────────────────────────────────────────────
# Model Catégorie
# ─────────────────────────────────────────────────────────────
class Category(TimeStampedModel):
    """
    CATÉGORIES DE PROJETS : Web Dev, IA, Sécurité, DevOps, etc.
    
    CHAMPS :
    - name : nom affiché (ex: "Web Development")
    - slug : version URL-friendly (ex: "web-development")
    - icon : emoji ou classe d'icône (ex: "💻")
    - color : classe Tailwind pour styling (ex: "text-primary")
    - description : texte descriptif optionnel
    - is_active : permet de cacher une catégorie sans la supprimer
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug URL")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji ou classe d'icône", verbose_name="Icône")
    color = models.CharField(
        max_length=50, 
        default="text-primary", 
        help_text="Classe Tailwind (ex: text-primary, text-red-500)",
        verbose_name="Couleur"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']  # Tri alphabétique par défaut

    def __str__(self):
        """Représentation textuelle : utilisé dans l'admin et les templates"""
        return self.name

    def save(self, *args, **kwargs):
        """
        OVERRIDE de la méthode save() :
        Auto-génère le slug à partir du name si non fourni.
        
        slugify() transforme "Web Development" → "web-development"
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────────
# Model Technologie
# ─────────────────────────────────────────────────────────────
class Technology(models.Model):
    """
    TECHNOLOGIES UTILISÉES : Django, React, Docker, etc.
    
    LOGIQUE : Séparées des projets pour réutilisabilité.
    Un projet peut avoir plusieurs technos (ManyToMany).
    Une techno peut être utilisée dans plusieurs projets.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Classe d'icône ou emoji")
    color = models.CharField(max_length=50, default="text-primary", help_text="Classe Tailwind")

    class Meta:
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────────
# Model Projet (principal)
# ─────────────────────────────────────────────────────────────
class Project(TimeStampedModel):
    """
    MODEL PRINCIPAL : Représente un projet du portfolio.
    
    CHAMPS IMPORTANTS :
    - title : titre du projet
    - slug : pour l'URL (ex: /portfolio/nexus-bank/)
    - category : ForeignKey vers Category (un projet = une catégorie)
    - technologies : ManyToMany vers Technology (plusieurs technos)
    - featured_image : image principale (uploadée dans MEDIA_ROOT/projects/)
    - content : description riche (éditeur WYSIWYG CKEditor)
    - is_featured : pour mettre en avant sur la homepage
    - order : tri personnalisé (projets avec order=1 avant order=2)
    
    RELATIONS :
    - ForeignKey : on_delete=models.CASCADE signifie que si on supprime
      la catégorie, tous ses projets seront supprimés aussi
    - ManyToManyField : crée automatiquement une table intermédiaire
    """
    
    # ───── Informations de base ─────
    title = models.CharField(max_length=200, verbose_name="Titre du projet")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="Slug URL")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre court")
    
    # ───── Classification ─────
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,  # Si catégorie supprimée → projets supprimés
        related_name='projects',    # Permet d'accéder aux projets : category.projects.all()
        verbose_name="Catégorie"
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name='projects',
        blank=True,
        verbose_name="Technologies utilisées"
    )
    
    # ───── Contenu ─────
    featured_image = models.ImageField(
        upload_to='projects/%Y/%m/',  # Organisation par année/mois
        blank=True,
        null=True,
        verbose_name="Image principale"
    )
    gallery_images = models.JSONField(
        default=list,  # Stocke une liste d'URLs ou paths
        blank=True,
        help_text="Liste d'images supplémentaires (JSON)",
        verbose_name="Galerie d'images"
    )
    description = models.TextField(verbose_name="Description courte (pour cards)")
    content = RichTextUploadingField(
        blank=True,
        verbose_name="Description détaillée",
        help_text="Contenu complet avec éditeur WYSIWYG"
    )
    
    # ───── Métadonnées projet ─────
    client = models.CharField(max_length=200, blank=True, verbose_name="Client")
    year = models.PositiveIntegerField(verbose_name="Année de réalisation")
    duration = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Ex: '3 mois', '6 semaines'",
        verbose_name="Durée du projet"
    )
    
    # ───── Liens externes ─────
    live_url = models.URLField(blank=True, verbose_name="Lien vers le site live")
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, verbose_name="Lien démo/vidéo")
    
    # ───── SEO ─────
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Description pour moteurs de recherche (160 caractères max)",
        verbose_name="Meta Description"
    )
    
    # ───── Gestion d'affichage ─────
    is_featured = models.BooleanField(
        default=False,
        help_text="Afficher sur la page d'accueil",
        verbose_name="Projet mis en avant"
    )
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    order = models.IntegerField(
        default=0,
        help_text="Ordre d'affichage (0 = premier)",
        verbose_name="Ordre"
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['order', '-created_at']  # Tri par order, puis par date décroissante
        indexes = [
            models.Index(fields=['slug']),  # Index pour recherche rapide par slug
            models.Index(fields=['is_published', 'order']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-génération du slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        URL CANONIQUE du projet.
        Utilisé dans les templates : {{ project.get_absolute_url }}
        Utilisé dans les redirections après création/modification
        """
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    @property
    def tech_tags(self):
        """
        PROPERTY : transforme une méthode en attribut.
        Usage dans template : {{ project.tech_tags }} au lieu de {{ project.tech_tags() }}
        
        Retourne les noms des technologies séparés par des virgules.
        """
        return ", ".join([tech.name for tech in self.technologies.all()])

    def increment_views(self):
        """Méthode pour incrémenter le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])  # Ne met à jour que ce champ (optimisation)
