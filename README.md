# abdoul-didacticiel
mon site pero
abdoul-didacticiel/
├── .github/workflows/       # Tes pipelines (on va les améliorer)
├── src/                     # Code Django
├── static/                  # Fichiers statiques
├── templates/               # Templates HTML
├── docker/                  # Fichiers Docker spécifiques
│   └── prometheus.yml       # Config monitoring
├── .env.example             # Modèle de variables d'env
├── .pre-commit-config.yaml  # Pour la qualité du code (Ruff, Black)
├── Dockerfile               # Ton image pro
├── docker-compose.yml       # Pour le dev local (Django + DB)
├── docker-compose.prod.yml  # Pour le déploiement Swarm/Render
├── Makefile                 # Ton tableau de bord de commandes
├── requirements.txt
└── build.sh                 # Script de build