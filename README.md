from datetime import date

class IR:
    __bareme = [
        [0.00, 2500.00 ,0.00 , 0.00],
        [2501.00 , 4166.00 ,0.10 , 250.00],
        [4167.00 , 5000.00 , 0.20 , 666.67],
        [5001.00 , 6666.00 , 0.30 , 1166.67],
        [6667.00 , 15000.00 , 0.34 , 1433.33],
        [15001.00 , 999999.00 , 0.38 , 2033.33]
    ]

    @staticmethod
    def MontantIR(salaire):
        for min_val, max_val, taux, deduction in IR.__bareme:
            if min_val <= salaire <= max_val:
                return (salaire * taux) - deduction
        return 0.0

    # @staticmethod
    # def MontantIR(salaire):
    #   for m in IR.__bareme :
    #      if  m[0] < salaire <= m[1]:
    #         Taux = m[2]
    #         Deduction = m[3]
    #         IR.MontantIR = (salaire * Taux ) - Deduction
    #      return  IR.MontantIR
    #   return 0.00

class Employe:
    __auto = 0

    def __init__(self, nom, prenom, date_Naissance, date_Recrutement, salaire_Base):
        Employe.__auto += 1
        self.__matricule = Employe.__auto
        self.__nom = nom
        self.__prenom = prenom
        self.__dateNaissance = date_Naissance
        self.__dateRecrutement = date_Recrutement
        self.__salaireBase = salaire_Base

    @property
    def matricule(self):
        return self.__matricule

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, nouveauNom):
        self.__nom = nouveauNom

    @property
    def prenom(self):
        return self.__prenom

    @prenom.setter
    def prenom(self, nouveauPrenom):
        self.__prenom = nouveauPrenom

    @property
    def dateNaissance(self):
        return self.__dateNaissance

    @dateNaissance.setter
    def dateNaissance(self, nouvelleDateNaissance):
        if isinstance(nouvelleDateNaissance, date):
            self.__dateNaissance = nouvelleDateNaissance
        else:
            raise ValueError("La date de naissance est invalide !!!!")

    @property
    def dateRecrutement(self):
        return self.__dateRecrutement

    @dateRecrutement.setter
    def dateRecrutement(self, nouvelleDateRecrutement):
        if isinstance(nouvelleDateRecrutement, date) and self.CalculerAge() > 18:
            self.__dateRecrutement = nouvelleDateRecrutement
        else:
            raise ValueError("La date de recrutement est invalide !!")

    @property
    def salaireBase(self):
        return self.__salaireBase

    @salaireBase.setter
    def salaireBase(self, nouveauSalaire):
        if nouveauSalaire > 0:
            self.__salaireBase = nouveauSalaire
        else:
            raise ValueError("Le salaire doit être positif.")


    def CalculerAge(self):
        return date.today().year - self.__dateNaissance.year


    def SalaireNet(self):
        if IR.MontantIR(self.__salaireBase) > self.__salaireBase:
            return "L'impôt sur le revenu ne peut pas dépasser le salaire"
        return self.__salaireBase - IR.MontantIR(self.__salaireBase)


    def DateRetrait(self):
        return self.__dateNaissance.replace(year=self.__dateNaissance.year + 60)

    # from dateutil.relativedelta import relativedelta
    # def DateRetrait(self):
    #     return self.__date_naissance + relativedelta(years=60)


    def Anciennete(self):
        if self.__dateRecrutement is not None:
            return date.today().year - self.__dateRecrutement.year
        return 0


    def Info(self):
        return (f"° Nom : {self.__nom}\n"
                f"° Prénom : {self.__prenom}\n"
                f"° Date de naissance : {self.__dateNaissance}\n"
                f"° Âge : {self.CalculerAge()} ans \n"
                f"° Date de recrutement : {self.__dateRecrutement}\n"
                f"° Salaire de base : {self.__salaireBase} DH\n"
                f"° Date de retraite : {self.DateRetrait()}\n"
                f"° Ancienneté : {self.Anciennete()} ans ")



class Formateur(Employe):
    def __init__(self, nom, prenom, date_Naissance, date_Recrutement, salaire_Base, NbrHrSupp):
        super().__init__(nom, prenom, date_Naissance, date_Recrutement, salaire_Base)
        self.__NbrHrSupp = NbrHrSupp
        self.__RemunerationH = 150.00

    @property
    def RemunerationH(self):
        return self.__RemunerationH

    @RemunerationH.setter
    def RemunerationH(self, nouvelleRemuneration):
        if nouvelleRemuneration > 0:
            self.__RemunerationH = nouvelleRemuneration
        else:
            raise ValueError("La valeur de rémunération horaire est toujours positive.")

    def SalaireNet(self):
        return self.salaireBase + (self.__NbrHrSupp * self.__RemunerationH) - IR.MontantIR(self.salaireBase)

    def Infos(self):
        return (f"{super().Info()}\n"
                f"° Nombre d'heures supplémentaires : {self.__NbrHrSupp} h\n"
                f"° Rémunération horaire : {self.__RemunerationH} DH\n"
                f"° Salaire net : {self.SalaireNet()} DH\n")




class Agent(Employe):
    def __init__(self, nom, prenom, date_Naissance, date_Recrutement, salaire_Base, PrimeResponsabilite):
        super().__init__(nom, prenom, date_Naissance, date_Recrutement, salaire_Base)
        self.__PrimeResponsabilite = PrimeResponsabilite

    @property
    def PrimeResponsabilite(self):
        return self.__PrimeResponsabilite

    @PrimeResponsabilite.setter
    def PrimeResponsabilite(self, value):
        if value > 0:
            self.__PrimeResponsabilite = value
        else:
            raise ValueError("Le montant de la prime responsabilité doit être positif.")

    def SalaireNet(self):
        salaire_Net = (self.salaireBase + self.PrimeResponsabilite) - IR.MontantIR(self.salaireBase + self.PrimeResponsabilite)
        return salaire_Net

    def Info(self):
        return (f"{super().Info()}\n"
                f"° Prime de responsabilité : {self.__PrimeResponsabilite} DH\n"
                f"° Salaire net : {self.SalaireNet()} DH")


try:
    formateur = Formateur("Meriem", "Moukrim", date(2005, 5, 9), date(2023, 7, 9), 8000, 20)
    print("____________Informations du Formateur :_______________\n")
    print(formateur.Infos())

    agent = Agent("Aymen", "Rafiki", date(1985, 3, 10), date(2005, 10, 9), 10000, 400)
    print("_____________Informations de l'Agent :________________\n")
    print(agent.Info())

except ValueError as e:
    print(f"Erreur : {e}")

