

class Utilitaires:
    @staticmethod
    def split_path(chemin):
        
        dossier, nom_fichier = chemin.rsplit('/', 1)
        return dossier, nom_fichier

    @staticmethod
    def dossier_existe(dossier):
        
        try:
            # open le dossier
            with open(dossier):
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def creer_dossier(dossier):
        
        # kreye fichier vide
        with open(dossier, 'w'):
            pass


