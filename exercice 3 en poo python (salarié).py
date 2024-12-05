from datetime import date
from dateutil.relativedelta import relativedelta


class Salarie:
    __auto = 0

    def __init__( self , nom , prenom , dateNaissance , dateEmbauche = None , salaire_Base = None ) :

        Salarie.__auto += 1
        self.__matricule = Salarie.__auto
        self.__nom = nom
        self.__prenom = prenom
        self.__date_Naissance = dateNaissance
        self.__date_Embauche = dateEmbauche
        self.__salaire_Base = salaire_Base

    @property
    def matricule(self) :
        return self.__matricule

    @property
    def nom(self) :
        return self.__nom

    @nom.setter
    def nom(self, value) :
        self.__nom = value

    @property
    def prenom(self) :
        return self.__prenom

    @prenom.setter
    def prenom(self, value) :
        self.__prenom = value

    @property
    def dateNaissance(self) :
        return self.__date_Naissance

    @dateNaissance.setter
    def dateNaissance(self, nouvelleDateNaissance) :
        if isinstance(nouvelleDateNaissance, date) :
            self.__date_Naissance = nouvelleDateNaissance
        else:
            raise ValueError("Date de naissance invalide")

    @property
    def Age(self) :
        return date.today().year - self.__date_Naissance.year

    @property
    def dateEmbauche(self) :
        return self.__date_Embauche

    @dateEmbauche.setter
    def dateEmbauche(self, nouvelleDateEmbauche) :
        if isinstance(nouvelleDateEmbauche, date) and self.Age >=16 :
            self.__date_Embauche = nouvelleDateEmbauche
        else:
            raise ValueError("Date embauche invalide")

    @property
    def salaireBase(self) :
        return self.__salaire_Base

    @salaireBase.setter
    def salaireBase(self, nouvelleSalaireDeBase) :
        if nouvelleSalaireDeBase > 0:
            self.__salaire_Base = nouvelleSalaireDeBase
        else:
            raise ValueError("Salaire invalide")

    def __str__(self) :
        return (f"Matricule : {self.__matricule}\n"
                f"Nom : {self.__nom}\n"
                f"Prénom : {self.__prenom}\n"
                f"Date de Naissance : {self.__date_Naissance}\n"
                f"Age : {self.Age} ans \n"
                f"Date embauche : {str(self.__date_Embauche) if self.__date_Embauche else 'rien'}\n"
                f"Salaire de base : {str(self.__salaire_Base) + 'DH' if self.__salaire_Base else 'rien'} ")

    @property
    def Mutuelle(self) :
        if self.__salaire_Base:
            return (3 * self.__salaire_Base) / 100
        return 0

    @property
    def Retraite(self) :
        if self.__salaire_Base:
            return (6 * self.__salaire_Base) / 100
        return 0

    @property
    def dateRetraite(self) :
        if self.__date_Embauche :
            return self.__date_Embauche + relativedelta(years = 60)

    @property
    def Anciente(self) :
        if self.__date_Embauche :
            return date.today().year - self.__date_Embauche.year
        return 0

    @property
    def PrimeAnciente(self) :
        anciente = self.Anciente
        if anciente > 0 :
            if 0 < anciente < 2 :
                taux_anciente = 0
            elif 2 <= anciente < 5 :
                taux_anciente = 5
            elif 5 <= anciente < 10 :
                taux_anciente = 10
            elif 10 <= anciente < 15 :
                taux_anciente = 15
            elif 15 <= anciente < 20 :
                taux_anciente = 20
            else :
                taux_anciente = 25
            return self.__salaire_Base * taux_anciente / 100
        return 0

    @property
    def salaireBrute(self) :
        if self.__salaire_Base:
            return self.__salaire_Base + self.PrimeAnciente
        return 0

    @property
    def IR(self) :
        if self.salaireBrute :
            SB = self.salaireBrute
            if 0 < SB <= 2500:
                Deduction = Taux = 0
            elif 2500 < SB <= 4166:
                Deduction , Taux = 250 , 10
            elif 4166 < SB <= 5000:
                Deduction , Taux = 666.67 , 20
            elif 5000 < SB <= 6666:
                Deduction , Taux = 1166.67, 30
            elif 6666 < SB <= 15000:
                Deduction , Taux = 1433.33, 34
            else:
                Deduction , Taux = 2033.33, 38
            IR = (SB * Taux / 100) - Deduction
            return IR
        return 0

    @property
    def salaireNet(self) :
        return self.salaireBrute - self.Mutuelle - self.Retraite - self.IR

    def AugmentationSalaire(self, pourcentage) :
        if pourcentage > 0:
            augmentation = (self.__salaire_Base * pourcentage) / 100
            self.__salaire_Base += augmentation
            return f"Le salaire a été augmenté de {pourcentage}% : {self.__salaire_Base} DH."
        else:
            return "Le pourcentage d'augmentation doit être positif."

    def BulletinPaie(self) :
        return (f"Matricule : {self.__matricule}\n"
                f"Nom : {self.__nom} {self.__prenom}\n"
                f"Date de Naissance : {self.__date_Naissance}\n"
                f"Age : {self.Age} ans\n"
                f"Date embauche : {str(self.__date_Embauche) if self.__date_Embauche else 'rien'}\n"
                f"Salaire de base : {str(self.__salaire_Base) + 'DH' if self.__salaire_Base else 'rien'}\n"
                f"_________ ***Bulletin De Paie*** _____________\n"
                f"La Mutuelle : {self.Mutuelle} DH \n"
                f"La Retraite : {self.Retraite} DH \n"
                f"Date de Retraite : {self.dateRetraite}\n"
                f"Salaire Net : {self.salaireNet} DH \n"
                f"Ancienneté : {self.Anciente} ans \n"
                f"Prime d'ancienneté : {self.PrimeAnciente} DH \n"
                f"Impot sur le revenu (IR) : {self.IR} DH \n"
                f"Salaire Brut : {self.salaireBrute} DH \n"
                f"Augmentation de Salaire : {self.AugmentationSalaire(10)}")


salarie1 = Salarie("meriem","moukrim",date(2005,5,9),date(2025,7,7),8000)
print(salarie1.BulletinPaie())
