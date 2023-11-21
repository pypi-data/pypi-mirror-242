



class PDFGenerator:
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        self.contenu = []

    def ajouter_texte(self, texte):
        self.contenu.append(texte)

    def generer_pdf(self):
        try:
            with open(self.nom_fichier, 'wb') as f:
                f.write(self._generer_contenu_pdf().encode('utf-8'))
            print(f"Le fichier PDF a été généré avec succès : {self.nom_fichier}")
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")

    def _generer_contenu_pdf(self):
        contenu_pdf = f"%PDF-1.4\n\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n\n5 0 obj\n<< /Length 57 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n({self.contenu[0]}) Tj\nET\nendstream\nendobj\n\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000055 00000 n \n0000000110 00000 n \n0000000185 00000 n \n0000000271 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n351\n%%EOF"
        return contenu_pdf
