"""Quiz 1 - Gestion de casiers (parties B et C)."""
class LocationInvalide(Exception):
    """Levée quand une location est refusée."""


class Casier:
    def __init__(self, numero, pavillon):
        self.__numero = numero
        self.__pavillon = pavillon
        self.__occupe = False

    def get_numero(self):
        return self.__numero

    def get_pavillon(self):
        return self.__pavillon

    def est_occupe(self):
        return self.__occupe

    def occuper(self):
        if self.__occupe:
            raise LocationInvalide(f"Le casier {self.__numero} est déjà occupé.")
        self.__occupe = True

    def liberer(self):
        self.__occupe = False


class Etudiant:
    DUREE_MAX = 8

    def __init__(self, matricule, nom):
        self.__matricule = matricule
        self.__nom = nom
        self.locations = []

    def get_matricule(self):
        return self.__matricule

    def get_nom(self):
        return self.__nom

    def duree_max(self):
        return Etudiant.DUREE_MAX


class EtudiantInternational(Etudiant):
    def __init__(self, matricule, nom, mois_supp=4):
        super().__init__(matricule, nom)
        self.__mois_supp = mois_supp

    def duree_max(self):
        return super().duree_max() + self.__mois_supp


class Location:
    def __init__(self, etudiant, casier, date_debut, nb_mois):
        maximum = etudiant.duree_max()
        if nb_mois <= 0 or nb_mois > maximum:
            raise LocationInvalide(
                f"Durée demandée : {nb_mois} mois, maximum autorisé : {maximum} mois."
            )
        casier.occuper()  # peut lever LocationInvalide (casier déjà occupé)
        self.__etudiant = etudiant
        self.__casier = casier
        self.__date_debut = date_debut
        self.__nb_mois = nb_mois
        etudiant.locations.append(self)

    def resume(self):
        return (f"{self.__etudiant.get_nom()} loue le casier "
                f"{self.__casier.get_numero()} à partir du {self.__date_debut} "
                f"pour {self.__nb_mois} mois.")


def main():
    a12 = Casier("A-12", "Pavillon A")
    b07 = Casier("B-07", "Pavillon B")
    ana = Etudiant("E001", "Ana Tremblay")
    luis = EtudiantInternational("E002", "Luis Ramirez")

    tentatives = [
        (1, ana, a12, 8),
        (2, luis, b07, 12),
        (3, ana, b07, 4),
        (4, luis, a12, 13),
    ]
    for no, etu, casier, mois in tentatives:
        print(f"Tentative {no} : {etu.get_nom()}, {casier.get_numero()}, {mois} mois")
        try:
            location = Location(etu, casier, "2026-09-30", mois)
        except LocationInvalide as e:
            print("  Erreur :", e)
        else:
            print("  OK :", location.resume())
        finally:
            print("  --- demande traitée ---")


if __name__ == "__main__":
    main()
