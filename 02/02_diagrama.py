import csv

class Persona:
    def __init__ (self, nom, edat, sexe, altura):
        self.nom = nom
        self.edat = edat
        self.sexe = sexe
        self.altura = altura

class Estudiant(Persona):
    def __init__ (self, nom: str, edat: int, sexe: str, altura: int, idEstudiant: int, notaMitjana: float):
        super().__init__(nom, edat, sexe, altura)
        self.idEstudiant = idEstudiant
        self.notaMitjana = notaMitjana
        self.grups = list()
    
    def ha_aprovat(self) -> bool:
        if self.notaMitjana >= 5:
            return True
        else:
            return False

class Professor(Persona):
    def __init__ (self, nom: str, edat: int, sexe: str, altura: int, valoracionsAlumnes: float, num_maxim_grups: int):
        super().__init__(nom, edat, sexe, altura)
        self.valoracionsAlumnes = valoracionsAlumnes
        self.num_maxim_grups = num_maxim_grups
        self.grups = list()

    def can_more_classes(self) -> bool:
        if len(self.grups) < self.num_maxim_grups:
            return True
        else:
            return False

class Grup:
    def __init__ (self, nom):
        self.nom = nom
        self.estudiants = list()

    def guardar_estudiant(self, estudiant: Estudiant):
        self.estudiants.append(estudiant)

    def llegir_estudiants(self):
        for estudiant in self.estudiants:
            print(estudiant.nom)

if __name__ == "__main__":
    with open("./02/Dades primera sessió.csv", "r") as file:
        csv_reader = csv.reader(file)
        grups = dict()
        for row in csv_reader:
            if row[6] not in grups:
                grups[row[6]] = Grup(row[6])
            grups[row[6]].guardar_estudiant(Estudiant(*row[:6]))

        for grup in grups.values():
            grup.llegir_estudiants()
