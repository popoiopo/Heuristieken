"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""
##---------------Parameter waardes ----------------------------------------------##
#bepaalt hoe vol/leeg de werkgroepen mogen zijn
parameter_werkgroep_grootte = 0.21 #0.41 en 0.61 zijn ook interessante grenzen

##---------------Inladen Informatie ---------------------------------------------##
import csv
import math
import random
import time
from fnmatch import fnmatch, fnmatchcase
from copy import deepcopy

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

##---------------DICTs met info ---------------------------------------------##
# Maak dict van type data tegen details student/vak
student_info 	= [dict(zip(header_studenten, check)) for check in data_studenten]
vak_info	 	= [dict(zip(header_vakken, check)) for check in data_vakken]
lokalen_info 	= {"A1.04" : 41, "A1.06" : 22, "A1.08" : 20, "A1.10" : 56, "B0.201" : 48, "C0.110" : 117, "C1.112" : 60}
# Maak dict van student/vak/lokalen tegen details
info_student 	= [dict(zip(check, header_studenten)) for check in data_studenten]
info_vak	 	= [dict(zip(check, header_vakken)) for check in data_vakken]
info_lokalen 	= {41 : "A1.04", 22 : "A1.06", 20 : "A1.08", 56 : "A1.10", 48 : "B0.201", 117 : "C0.110", 60 : "C1.112"}

all_subject_names = ['Advanced_Heuristics',"Algoritmen_en_complexiteit","Analysemethoden_en_technieken","Architectuur_en_computerorganisatie",
"Autonomous_Agents_2","Bioinformatica","Calculus_2","Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum","Data_Mining",
"Databases_2","Heuristieken_1","Heuristieken_2","Informatie_en_organisatieontwerp","Interactie_ontwerp","Kansrekenen_2",
"Lineaire_Algebra","Machine_Learning","Moderne_Databases","Netwerken_en_systeembeveiliging","Programmeren_in_Java_2",
"Project_Genetic_Algorithms","Project_Numerical_Recipes","Reflectie_op_de_digitale_cultuur","Software_engineering",
"Technology_for_games","Webprogrammeren_en_databases","Zoeken_sturen_en_bewegen"]

#Maak een leeg rooster van dicts in volgorde dag->tijdslot->lokalen
#Toe te voegen; Dict met key vak en values studNrs van studenten uit vak/werkgroep
week = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag']
tijdslots = ['9.00-11.00', '11.00-13.00', '13.00-15.00', '15.00-17.00', '17.00-19.00']
rooster = {}
for dag in week:
	rooster[dag] = {}
	for tijdsl in tijdslots:
		rooster[dag][(tijdsl)] = {}
		for lok in lokalen_info:
			rooster[dag][(tijdsl)][lok] = {} #voeg dict met studenten toe

#Maak dict van vak tegen string van student nummers van leerlingen die 't volgen
subject_student_database = {}
for subject in all_subject_names:
	for student in student_info:
		nummer = student['Stud.Nr.']
		for info in info_student:
			if nummer in info:
				if subject in info:
					subject_student_database.setdefault(subject, []).append(nummer)

##------------------------------MAAK LIJST VAN UNIEKE VAKKEN EN INGEDEELDE LEERLINGEN---------------------##
##Maak vaste Hoorcollege, werk- en practicagroepen met string van StudNr's van studenten
group_student_database = {}
for subject in all_subject_names:
	for subject_details in vak_info:
		if subject in subject_details.values():
			subject_student_number = float(len(subject_student_database[subject]))
			##geef hoorcolleges een unieke naam en voeg ze toe aan de dict
			hc = int(subject_details["hoorcolleges"])
			for i in range(1,hc+1):
				vak_naam = "hc_" + str(i) + "_1_" + subject
				group_student_database[vak_naam] = subject_student_database[subject]
			##geef werkcolleges een unieke naam en maak groepen. Voeg die groepen toe aan dict
			wc = int(subject_details["werkcolleges"])
			for i in range(1,wc+1):
				##checkt hoeveel werkgroepen er nodig zijn, dit hangt af van de parameter bovenaan
				stud_over_max = subject_student_number / float(subject_details["werk_max_stud"])
				if (stud_over_max % 1) > parameter_werkgroep_grootte:
					wc_number = int(stud_over_max) + 1
				else:
					wc_number = int(stud_over_max)
				check = int(math.ceil((subject_student_number / wc_number)))
				x = 0
#				check_nrstud_wc = 0	##voor check of alle studenten zijn ingedeeld
				##Loop over alle werkgroepen en maak groepen van gemiddelde grootte
				for j in range(1,wc_number+1): #later ABC?
					vak_naam = "wc_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database[vak_naam] = subject_student_database[subject][x:x+check]
					x += check
#					check_nrstud_wc += len(group_student_database[vak_naam])	##voor check of alle studenten zijn ingedeeld
			##nog niet aan toe gekomen
			pr = int(subject_details["practica"])
			for i in range(1,pr+1):
				stud_over_max = subject_student_number / float(subject_details["practica_max_stud"])
				if (stud_over_max % 1) > parameter_werkgroep_grootte: ##????hier andere parameter doen????##
					pr_number = int(stud_over_max) + 1
				else:
					pr_number = int(stud_over_max)
				check = int(math.ceil((subject_student_number / pr_number)))
				x = 0
#				check_nrstud_pr = 0	##voor check of alle studenten zijn ingedeeld
				for j in range(1,pr_number+1): #later ABC?
					vak_naam = "pr_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database[vak_naam] = subject_student_database[subject][x:x+check]
					x += check
#					check_nrstud_pr += len(group_student_database[vak_naam])	##voor check of alle studenten zijn ingedeeld
#print('Het aantal te roosteren unieke vakken is:')
#print(len(group_student_database))

##-------------------------------KIES RANDOM DAG-TIJDSLOT-LOKAAL IN DE WEEK-----------------------------##
def roosteren(vak, timetable, gro_stu_dat):
	day = random.choice(week)
	time = random.choice(tijdslots)
	room = random.choice(list(lokalen_info.keys()))
	if not bool(timetable[day][time][room]):
		timetable[day][time][room][vak] = gro_stu_dat[vak]
#		print(day, time, room)
#		print(rooster[day][time][room])
	else:
		roosteren(vak, timetable, gro_stu_dat)

def reverse_roosteren(timetable):
	day = random.choice(week)
	time = random.choice(tijdslots)
	room = random.choice(list(lokalen_info.keys()))
	if not bool(timetable[day][time][room]):
		reverse_roosteren
	else:
		vak_name = 	timetable[day][time][room].keys()
		del timetable[day][time][room]
		return vak_name

for subject in list(group_student_database.keys()):
	roosteren(subject, rooster, group_student_database)



##-----------------------------------VANAF HIER IS HET ROOSTER RANDOM & GELDIG---------------------------##
##evalueer punten voor lokaalbezetting
time_1 = time.time()
min_punten_lokalen = int(0)
for dag in week:
	for tijdsl in tijdslots:
		for lok in lokalen_info:
			for keys in rooster[dag][(tijdsl)][lok]:
				x = (lokalen_info[lok]-(len(rooster[dag][(tijdsl)][lok][keys])))
				if x < 0:
					min_punten_lokalen += x
print(min_punten_lokalen)
time_2 = time.time()
min_punten_lokalen = int(0)
for dag in rooster.keys():
	for tijdsl in rooster[dag].keys():
		for lok in rooster[dag][tijdsl].keys():
			for keys in rooster[dag][(tijdsl)][lok]:
				x = (lokalen_info[lok]-(len(rooster[dag][(tijdsl)][lok][keys])))
				if x < 0:
					min_punten_lokalen += x
print(min_punten_lokalen)
time_3 = time.time()
#ticks = time.time()
a = time_2-time_1
print(a)
a = 0.0
a = time_3-time_2
print(a)
#print((time_2-time_1))
#print((time_3-time_2))
print(rooster)
rooster2 = deepcopy(rooster)
rooster.clear()
print('ok')
print(rooster)
print('ok')
print(rooster2['maandag']['9.00-11.00'])
##-----DEEP COPY------------------##
"""
from copy import deepcopy

lst1 = ['a','b',['ab','ba']]

lst2 = deepcopy(lst1)
"""

studenten_roostering.close()
vakinfo.close()