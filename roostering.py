"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""

import csv
from fnmatch import fnmatch, fnmatchcase

rooster = open("studenten_roostering.csv")
csv_rooster = csv.reader(rooster)

data = [row for row in csv_rooster]
var_names = [name for name in data[0]]
people_var = [dict(zip(var_names, person)) for person in data]
people_person = [dict(zip(person, var_names)) for person in data]

vakken = ["Advanced_Heuristics","Algoritmen_en_complexiteit","Analysemethoden_en_technieken","Architectuur_en_computerorganisatie","Autonomous_Agents_2","Bioinformatica","Calculus_2","Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum","Data_Mining","Databases_2","Heuristieken_1","Heuristieken_2","Informatie_en_organsatieontwerp","Interactie_ontwerp","Kansrekenen_2","Lineaire_Algebra","Machine_Learning","Moderne_Databases","Netwerken_en_systeembeveiliging","Programmeren_in_Java_2","Project_Genetic_Algorithms","Project_Numerical_Recipes","Reflectie_op_de_digitale_cultuur","Software_engineering","Technology_for_games","Webprogrammeren_en_databases","Zoeken_sturen_en_bewegen"]
vakken_database = {}

for vak in vakken:
	for person in people_person:
		if vak in person:
			vakken_database.setdefault(vak, []).append(person)

print "In totaal hebben wij " + str(len(people_person)) + " studenten, en " + str(len(vakken)) + " vakken."
print "In de komende rijen zie je het vak en het aantal leerlingen die daarin deelnemen in het volgende format."
print "Vaknaam : hoeveelheid leerlingen."
for vak in vakken:
	print vak + " : " + str(len(vakken_database[vak])) + "."


rooster.close()