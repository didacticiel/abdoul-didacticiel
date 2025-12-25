#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def get_settings_module():
    """
    Détermine le module de paramètres (settings) à charger 
    en fonction de la variable d'environnement DJANGO_ENVIRONMENT.
    """
    # 1. Cas spécifique : Tests
    if 'test' in sys.argv or 'pytest' in sys.modules:
        # Pointez vers un fichier settings/testing.py si vous en avez un.
        return 'src.settings.testing'
    
    # 2. Cas standard : Environnement défini
    environment = os.environ.get('DJANGO_ENVIRONMENT', 'development').lower()
    
    settings_map = {
        'development': 'src.settings.development',
        'dev': 'src.settings.development',
        'staging': 'src.settings.staging',
        'stage': 'src.settings.staging',
        'production': 'src.settings.production',
        'prod': 'src.settings.production',
        # Si vous n'utilisez pas de settings spécifiques pour un environnement, 
        # celui-ci héritera de 'development'
    }
    
    # Retourne le module de paramètres correspondant, sinon 'development' par défaut.
    return settings_map.get(environment, 'src.settings.development')

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    # Met à jour la variable d'environnement pour que Django sache quel fichier settings utiliser
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_settings_module())

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()