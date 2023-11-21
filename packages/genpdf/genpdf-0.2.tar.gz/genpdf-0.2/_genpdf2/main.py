from deposit.pdfgen import PDFGenerator


# Page main

def tester_pdf_generator(chemin_dossier, nom_fichier, contenu_principal, contenu_supplementaire):
    # Génération du PDF
    pdf_generator = PDFGenerator(chemin_dossier + '/' + nom_fichier)
    pdf_generator.ajouter_texte(contenu_principal)
    pdf_generator.ajouter_texte(contenu_supplementaire)
    pdf_generator.generer_pdf()


# Exemple d'utilisation

# test en utilisateur
if __name__ == "__main__":
    tester_pdf_generator(
        input("Entrez le chemin du dossier : "),
        input("Entrez le nom du fichier (avec l'extension .pdf) : "),
        input("Entrez le contenu principal du PDF : "),
        input("Entrez le contenu supplémentaire du PDF : ")
    )

# Test en version developpeur
#  if __name__ == "__main__":
#     tester_pdf_generator(r"C:\Users\HP\Downloads\GENPDF2\genpdf2\_genpdf2", "test1.pdf", "bonjour sak pase", "")
    