"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""

import csv
from fnmatch import fnmatch, fnmatchcase

# Het inladen van informatie van de csv files
studenten_roostering = open("studenten_roostering.csv")
vakinfo = open("vakinfo.csv")
# Lees csv bestand uit
csv_studenten 	= csv.reader(studenten_roostering)
csv_vakken 		= csv.reader(vakinfo)
# Maak dict/array van data uit csv file
data_studenten 		= [row for row in csv_studenten] #previous data
data_vakken 		= [row for row in csv_vakken] #previous data_info
# Neem eerste regel van bestand, geeft info type per kolom
header_studenten 	= [name for name in data_studenten[0]] #previous people_var
header_vakken 		= [name for name in data_vakken[0]] #previous var_info
# Maak dict van type data tegen details student/vak
student_info 	= [dict(zip(header_studenten, check)) for check in data_studenten]
vak_info	 	= [dict(zip(header_vakken, check)) for check in data_vakken]
lokalen_info 	= [{"A1.04" : 41}, {"A1.06" : 22}, {"A1.08" : 20}, {"A1.10" : 56}, {"B0.201" : 48}, {"C0.110" : 117}, {"C1.112" : 60}]
# Maak dict van student/vak/lokalen tegen details
info_student 	= [dict(zip(check, header_studenten)) for check in data_studenten]
info_vak	 	= [dict(zip(check, header_vakken)) for check in data_vakken]
info_lokalen 	= [{41 : "A1.04"}, {22 : "A1.06"}, {20 : "A1.08"}, {56 : "A1.10"}, {48 : "B0.201"}, {117 : "C0.110"}, {60 : "C1.112"}]

all_subject_names = ['Advanced_Heuristics',"Algoritmen_en_complexiteit","Analysemethoden_en_technieken","Architectuur_en_computerorganisatie",
"Autonomous_Agents_2","Bioinformatica","Calculus_2","Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum","Data_Mining",
"Databases_2","Heuristieken_1","Heuristieken_2","Informatie_en_organisatieontwerp","Interactie_ontwerp","Kansrekenen_2",
"Lineaire_Algebra","Machine_Learning","Moderne_Databases","Netwerken_en_systeembeveiliging","Programmeren_in_Java_2",
"Project_Genetic_Algorithms","Project_Numerical_Recipes","Reflectie_op_de_digitale_cultuur","Software_engineering",
"Technology_for_games","Webprogrammeren_en_databases","Zoeken_sturen_en_bewegen"]

#Geeft aantal keer dat vak gegeven wordt per week
#input is vak_info en naam van vak dat gezocht moet worden
def aantalcollegesinweek(vakinfo, vak):
	for info in vakinfo:
		if info["vakken"] == vak:
			hc = info["hoorcolleges"]
			HC = float(hc)
			wc = info["werkcolleges"]
			WC = float(wc)
			pr = info["practica"]
			PR = float(pr)
			total = HC + WC + PR
			#print(vak)
			return total
"""
for check1 in student_info:
	student = check1["Achternaam"]
	print(student)
	for check2 in info_student:
		if student in check2:
			print(check2)
"""
subject_student_database = {}
for subject in all_subject_names:
	for student in student_info:
		naam = student['Achternaam']
		for info in info_student:
			if naam in info:
				if subject in info:
					subject_student_database.setdefault(subject, []).append(naam)
#print(subject_database)

subject_student_number = {}
for check in all_subject_names:
	y = len(subject_student_database[check])
	subject_student_number.setdefault(check, []).append(y)
#print(subject_number_students)

"""
n = 0
for check in all_subject_names:
	n += int(aantalcollegesinweek(vak_info, check))
rooster_info = ["vak", "college", "max_student", "dagen"]
leeg = ["leeg", "leeg", "leeg", "leeg"]
rooster_mogelijkheden_per_college =[ dict(zip(rooster_info, leeg)) for i in range(0, int(n))]
"""

"""
for check in all_subject_names:
	for n in range(0,int(aantalcollegesinweek(vak_info, check))):
		rooster_mogelijkheden_per_college["vak"] = check
		for info in vak_info:
			if info["vakken"] == check:
			hc = info["hoorcolleges"]
			for i in range (0, hc):
				rooster_mogelijkheden_per_college["college"] = 
			HC = float(hc)
			wc = info["werkcolleges"]
			WC = float(wc)
			pr = info["practica"]
			PR = float(pr)
		rooster_mogelijkheden_per_college["college"] = 
		rooster_mogelijkheden_per_college["max_student"] =
		rooster_mogelijkheden_per_college["dagen"] = 
"""




"""
rooster_mogelijkheden_per_college = {}		
#rooster_mogelijkheden_per_college = {}
for check in all_subject_names:
	print(check)
#	x = aantalcollegesinweek(vak_info, check)
#	print(aantalcollegesinweek(vak_info, check))
#	y = int(x)
#	print(y)
	for n in range(0,int(aantalcollegesinweek(vak_info, check))):
		rooster_mogelijkheden_per_college.append(dict(zip(rooster_info, leeg)))
		#rooster_mogelijkheden_per_college = dict(zip(rooster_info, leeg))
#		rooster_mogelijkheden_per_college["vak"] = n
		print(n)
#		print('ok')

"""


#leeg = ["leeg", "leeg", "leeg", "leeg"]
#rooster_mogelijkheden_per_college = [dict(zip(rooster_info, leeg)) for check in all_subject_names]
#rooster_mogelijkheden_per_college
#print(rooster_mogelijkheden_per_college)
#for check in all_subject_names:
#	print(rooster_mogelijkheden_per_college["vak"])
#	rooster_mogelijkheden_per_college['vak'] = 'check'
#print(rooster_mogelijkheden_per_college)

# Per vak iedereen opzoeken die het vak gevolgd heeft, 
# en deze vervolgens toe te voegen database
#vakken_database = {}
#for vak in all_subject_names:
#	print(vak)
#	for person in info_student:
#		print(person)
#		if vak in person:
#			vakken_database.setdefault(vak, []).append(person)
#print(vakken_database)



studenten_roostering.close()
vakinfo.close()