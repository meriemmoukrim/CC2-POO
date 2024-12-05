from datetime import datetime


# Classe IR
class IR:

    _bareme = [
        [0.00, 2500.00, 0.00, 0.00],
        [2501.00, 4166.00, 0.10, 250.00],
        [4167.00, 5000.00, 0.20, 666.67],
        [5001.00, 6666.00, 0.30, 1166.67],
        [6667.00, 15000.00, 0.34, 1433.33],
        [15001.00, 999999.00, 0.38, 2033.33]
    ]

    @staticmethod
    def MontantIR(salaire):

        for tranche in IR._bareme:
            if salaire > tranche[0] and salaire <= tranche[1]:
                taux_ir = tranche[2]
                deduction = tranche[3]
                montant_ir = (salaire * taux_ir) - deduction
                return montant_ir
        return 0.00  # Si le salaire ne correspond à aucune tranche


# Classe Employe
class Employe:
    matricule_counter = 1

    def __init__(self, nom, date_naissance, date_recrutement, salaire_base):
        self.__matricule = Employe.matricule_counter
        Employe.matricule_counter += 1
        self.__nom = nom
        self.__date_naissance = datetime.strptime(date_naissance, "%d/%m/%Y")
        self.__date_recrutement = datetime.strptime(date_recrutement, "%d/%m/%Y")
        self.__salaire_base = salaire_base

        # Vérification de l'âge minimum de recrutement
        if self.calculer_age() < 18:
            raise ValueError("L'âge minimum de recrutement est 18 ans.")

    @property
    def Matricule(self):
        return self.__matricule

    @property
    def Nom(self):
        return self.__nom

    @property
    def DateNaissance(self):
        return self.__date_naissance

    @property
    def DateRecrutement(self):
        return self.__date_recrutement

    @property
    def SalaireBase(self):
        return self.__salaire_base

    @property
    def age(self):
        return (datetime.now() - self.__date_naissance).days // 365

    def calculer_age(self):
        return (datetime.now() - self.__date_naissance).days // 365

    def SalaireNet(self):
        return self.__salaire_base - IR.MontantIR(self.__salaire_base)

    def DateRetraite(self):
        date_retraite = self.__date_naissance.replace(year=self.__date_naissance.year + 60)
        return date_retraite

    def Anciennete(self):
        return (datetime.now() - self.__date_recrutement).days // 365

    def info(self):
        return f"Matricule: {self.__matricule}, Nom: {self.__nom}, Age: {self.age} ans, Salaire net: {self.SalaireNet()} DH"


# Classe Formateur (hérite de Employe)
class Formateur(Employe):
    def __init__(self, nom, date_naissance, date_recrutement, salaire_base, nbr_heures_supp):
        super().__init__(nom, date_naissance, date_recrutement, salaire_base)
        self.__nbr_heures_supp = nbr_heures_supp
        self.__remuneration_h = 150.00  # valeur par défaut

    @property
    def NbrHeuresSupp(self):
        return self.__nbr_heures_supp

    @NbrHeuresSupp.setter
    def NbrHeuresSupp(self, valeur):
        self.__nbr_heures_supp = valeur

    @property
    def RemunerationH(self):
        return self.__remuneration_h

    @RemunerationH.setter
    def RemunerationH(self, valeur):
        if valeur > 0:
            self.__remuneration_h = valeur
        else:
            raise ValueError("La rémunération horaire doit être positive.")

    def SalaireNet(self):
        salaire_net = (self.SalaireBase + (self.NbrHeuresSupp * self.RemunerationH)) - IR.MontantIR(
            self.SalaireBase + (self.NbrHeuresSupp * self.RemunerationH))
        return salaire_net

    def info(self):
        return f"{super().info()}, Heures Supplémentaires: {self.NbrHeuresSupp}, Salaire Net Formateur: {self.SalaireNet()} DH"


# Classe Agent (hérite de Employe)
class Agent(Employe):
    def __init__(self, nom, date_naissance, date_recrutement, salaire_base, prime_responsabilite):
        super().__init__(nom, date_naissance, date_recrutement, salaire_base)
        self.__prime_responsabilite = prime_responsabilite

    @property
    def PrimeResponsabilite(self):
        return self.__prime_responsabilite

    @PrimeResponsabilite.setter
    def PrimeResponsabilite(self, valeur):
        if valeur >= 0:
            self.__prime_responsabilite = valeur
        else:
            raise ValueError("La prime de responsabilité doit être positive.")

    def SalaireNet(self):
        salaire_net = (self.SalaireBase + self.PrimeResponsabilite) - IR.MontantIR(
            self.SalaireBase + self.PrimeResponsabilite)
        return salaire_net

    def info(self):
        return f"{super().info()}, Prime de Responsabilité: {self.PrimeResponsabilite}, Salaire Net Agent: {self.SalaireNet()} DH"


# Programme principal
def main():
    try:
        # Création d'un formateur
        formateur = Formateur("Mohammed", "15/06/1985", "01/05/2010", 8000.00, 20)
        print(formateur.info())

        # Création d'un agent
        agent = Agent("Fatima", "10/09/1990", "01/06/2015", 7500.00, 2000.00)
        print(agent.info())

    except ValueError as e:
        print(f"Erreur: {e}")


# Exécution du programme principal
if __name__ == "__main__":
    main()
