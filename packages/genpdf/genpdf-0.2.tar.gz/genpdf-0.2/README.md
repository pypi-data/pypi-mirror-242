
# Générateur PDF Dynamique

## Description

Le Générateur PDF Dynamique est un outil Python permettant de créer des fichiers PDF à partir de données dynamiques.

## Fonctionnalités Principales

- Génération de fichiers PDF à partir de données dynamiques.
- Personnalisation du contenu PDF.
- Support de l'installation via pip.



## Installation

Utilisez la commande suivante pour installer le générateur PDF dynamique:

```bash
pip install genpdf
```

## Configuration

Aucune configuration spéciale n'est requise. Vous pouvez personnaliser le contenu du PDF dans votre code.

## Utilisation

Exemple d'utilisation:

```python
from generateur_pdf import PDFGenerator

# Création d'une instance PDFGenerator
pdf_generator = PDFGenerator("chemin/vers/fichier.pdf")

# Ajout de texte au PDF
pdf_generator.ajouter_texte("Contenu principal du PDF")
pdf_generator.ajouter_texte("Contenu supplémentaire du PDF")

# Génération du PDF
pdf_generator.generer_pdf()
```


## Auteurs

- Arbens VITAL & Heraldy DEBROSSE

## Licence

Ce projet n'est pas sous licence