# Utiliser une image de base contenant Python
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY . /app

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter l'application
CMD ["streamlit", "run", "app.py"]
