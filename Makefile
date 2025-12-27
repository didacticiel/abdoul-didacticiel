# ===========================================================
# VARIABLES GLOBALES
# ===========================================================
# Nom de ton application (utilisé pour les images docker si besoin)
APP_NAME = abdoul-didacticiel
PYTHON = python3
MANAGE = $(PYTHON) manage.py
# On détecte si on est sur Render ou en local
SETTINGS_DEV = src.settings.development
SETTINGS_TEST = src.settings.testing
SETTINGS_PROD = src.settings.production

.PHONY: help install migrate test run ci static clean

help:
	@echo ""
	@echo "📘 Abdoul Didacticiel Makefile — Mode Production Ready"
	@echo ""
	@echo "COMMANDES LOCALES :"
	@echo "  make install      → Installe les dépendances"
	@echo "  make migrate      → Applique les migrations (Dev)"
	@echo "  make run          → Lance le serveur de développement"
	@echo "  make static       → Collecte les fichiers statiques"
	@echo ""
	@echo "COMMANDES CI/CD & QUALITÉ :"
	@echo "  make test         → Lance les tests unitaires (via Testing Settings)"
	@echo "  make ci           → Pipeline complet (Install + Test)"
	@echo "  make lint         → Vérifie la qualité du code (Flake8)"
	@echo ""

# ===========================================================
# INSTALLATION & SETUP
# ===========================================================
install:
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt

migrate:
	@echo "🗄️ Application des migrations..."
	$(MANAGE) migrate --settings=$(SETTINGS_DEV)

static:
	@echo "🎨 Collecte des fichiers statiques..."
	$(MANAGE) collectstatic --no-input --settings=$(SETTINGS_PROD)

run:
	@echo "🚀 Démarrage du serveur..."
	$(MANAGE) runserver --settings=$(SETTINGS_DEV)

# ===========================================================
# TESTS & CI (Utilisé par GitHub Actions)
# ===========================================================
test:
	@echo "🧪 Exécution des tests (Environnement de Test)..."
	# On force l'usage de SQLite en mémoire via testing.py
	$(MANAGE) test --settings=$(SETTINGS_TEST)

ci: install test
	@echo "✅ Pipeline CI terminé avec succès !"

lint:
	@echo "🔍 Analyse statique du code..."
	# Nécessite 'pip install flake8'
	flake8 apps src

# ===========================================================
# NETTOYAGE
# ===========================================================
clean:
	@echo "🧹 Nettoyage des fichiers temporaires..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf staticfiles/