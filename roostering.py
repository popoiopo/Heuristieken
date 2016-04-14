"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""

import csv
from fnmatch import fnmatch, fnmatchcase

# Het inladen van informatie van de csv files
rooster = open("studenten_roostering.csv")
info = open("vakinfo.csv")
csv_rooster = csv.reader(rooster)
csv_info = csv.reader(info)

# Het in dictionary format zetten van student informatie
data = [row for row in csv_rooster]
var_names = [name for name in data[0]]
people_var = [dict(zip(var_names, person)) for person in data]
people_person = [dict(zip(person, var_names)) for person in data]

# Het in dictionary format zetten van vak informatie
data_info = [row for row in csv_info]
var_info = [name for name in data_info[0]]
vak_var = [dict(zip(var_info, vak)) for vak in data_info]
vak_info = [dict(zip(vak, var_info)) for vak in data_info]

# Klaarzetten om vak als key te maken in dictionary, en lokaal informatie in dictionary list zetten
vakken = ["Advanced_Heuristics","Algoritmen_en_complexiteit","Analysemethoden_en_technieken","Architectuur_en_computerorganisatie",
"Autonomous_Agents_2","Bioinformatica","Calculus_2","Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum","Data_Mining",
"Databases_2","Heuristieken_1","Heuristieken_2","Informatie_en_organsatieontwerp","Interactie_ontwerp","Kansrekenen_2",
"Lineaire_Algebra","Machine_Learning","Moderne_Databases","Netwerken_en_systeembeveiliging","Programmeren_in_Java_2",
"Project_Genetic_Algorithms","Project_Numerical_Recipes","Reflectie_op_de_digitale_cultuur","Software_engineering",
"Technology_for_games","Webprogrammeren_en_databases","Zoeken_sturen_en_bewegen"]
vakken_database = {}
lokalen = [{"A1.04" : 41}, {"A1.06" : 22}, {"A1.08" : 20}, {"A1.10" : 56}, {"B0.201" : 48}, {"C0.110" : 117}, {"C1.112" : 60}]

# Per vak iedereen opzoeken die het vak gevolgd heeft, 
# en deze vervolgens toe te voegen database
for vak in vakken:
	for person in people_person:
		if vak in person:
			vakken_database.setdefault(vak, []).append(person)

"""
# Info printen!
print "In totaal hebben wij " + str(len(people_person)) + " studenten, en " + str(len(vakken)) + " vakken."
print "In de komende rijen zie je het vak en het aantal leerlingen die daarin deelnemen in het volgende format."
print "Vaknaam : hoeveelheid leerlingen."
for vak in vak_var:
		print vak["vakken"] + " heeft " + vak["werkcolleges"] + " werkcolleges."

for vak in vakken:
	print vak + " : " + str(len(vakken_database[vak])) + "."
	print vakken_database[vak]
"""
'''
for vak in vakken_database:
	print vak
	print "---------------------------------------------"
	for student in vakken_database[vak]:
		print student
'''

print (vakken_database)

rooster.close()
info.close()