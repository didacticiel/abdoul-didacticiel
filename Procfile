# 'web:' définit le type de processus (serveur HTTP).
# 'gunicorn' est le serveur de production (plus solide que runserver).
# 'src.wsgi:application' pointe vers ton point d'entrée Django.
web: gunicorn src.wsgi:application --log-file -