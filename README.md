# Litrevu

Ce site permet aux utilisateurs de publier des critiques et des tickets (questions ou commentaires) sur des livres ou articles. Il offre une plateforme pour partager des opinions et discuter autour de la littérature et des articles.

## Installation

Pour installer et exécuter ce projet, suivez ces étapes :

### Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)

### Clonage du dépôt

Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/kenza12/Projet9.git
cd Projet9
```

### Installation des Dépendances

Installez les dépendances nécessaires en utilisant pip :

```bash
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate
pip install -r requirements.txt
```

## Exécution

Pour lancer le serveur de développement :

```bash
cd litrevu
python manage.py runserver
```

## Utilisation

Après avoir lancé le serveur, ouvrez votre navigateur et accédez à `http://localhost:8000` pour commencer à utiliser l'application.


## Fonctionnalités

- Création de Tickets : Les utilisateurs peuvent créer des tickets pour demander des avis (critiques) sur des livres ou articles spécifiques.
- Publication de Critiques : Les utilisateurs peuvent écrire et publier des critiques sur les livres ou articles en répondant à un ticket ou pas.
- Suivi des Utilisateurs : Les utilisateurs peuvent suivre (ou arrêter de suivre) d'autres utilisateurs pour voir leurs tickets et critiques.
- Blocage des Utilisateurs : Les utilisateurs peuvent bloquer (ou débloquer) d'autres utilisateurs pour ne plus voir leurs publications.
- Consulter ses publications : L'utilisateur connecté peut visualiser l'ensemble de ces tickets et critiques dans la page posts.
- Consulter le flux d'activité : L'utilisateur peut visualiser l'ensemble des tickets et critiques publiés par lui ou par d'autres utilisateurs qu'il suit !