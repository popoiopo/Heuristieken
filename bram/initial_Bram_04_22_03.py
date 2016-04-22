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
lijst = [0,1,2,3]
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
#print(subject_student_database)

#Maak dict van vak tegen aantal leerlingen dat 't volgt (en omgekeerd)
subject_student_number = {}
number_student_subject = {}
#Check hoeveel studenten er een vak volgen door len van dict[StudNr.] te geven
for check in all_subject_names:
	y = len(subject_student_database[check])
#	print(subject_student_database[check])
#	print(y)
	subject_student_number.setdefault(check, y)
	number_student_subject.setdefault(y, check)

parameter_werkgroep_grootte = 0.21
group_student_database = {}
test = {}
x = 0
#for subject in all_subject_names:
for k in range(0,1):
	subject = "Reflectie_op_de_digitale_cultuur"
	for subject_details in vak_info:
		if subject in subject_details.values():
			print(subject)
			hc = int(subject_details["hoorcolleges"])
			for i in range(1,hc+1):
				vak_naam = "hc_" + str(i) + "_1_" + subject
				group_student_database[vak_naam] = subject_student_database[subject]
			wc = int(subject_details["werkcolleges"])
			for i in range(1,wc+1):
				stud_over_max = float(subject_student_number[subject])/float(subject_details["werk_max_stud"])
				if (stud_over_max%1.0) > parameter_werkgroep_grootte:
					wc_number = int(stud_over_max) + 1
				else:
					wc_number = int(stud_over_max)
				for j in range(1,wc_number+1): #misschien leuk om dit later als abc op te slaan ipv 123
					vak_naam = "wc_" + str(i) + "_" + str(j) + "_" + subject
					print(vak_naam)
#					print(subject_student_number[subject])
					print(wc_number)
					group = int(float(subject_student_number[subject]+1.0)/wc_number)
#					print(group)
#					print(subject_student_database[subject])
					print(subject_student_database[subject][0:group])
					print(len(subject_student_database[subject][0:group]))
					print(group)
					subject_student_database[subject][0:group] = []
					#subject_student_database[subject].remove(subject_student_database[subject][subject_student_database[subject][group:]])
					print(subject_student_number[subject])
					#group_student_database[vak_naam] = subject_student_database[subject][int(float(subject_student_number[subject]))/wc_number):]
			pr = int(subject_details["practica"])
			for i in range(1,pr+1):
				pr_number = int(1)
				for j in range(1,pr_number+1): #misschien leuk om dit later als abc op te slaan ipv 123
					vak_naam = "pr_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database.setdefault(vak_naam, []).append(x)
#print(group_student_database)
#print(group_student_database['hc_1_1_Advanced_Heuristics'])
"""
for vak in all_subject_names:
	for subject_info in vak_info:
		if vak in subject.values():
			print(vak)
"""
"""
	college_type = aantalcollegesinweek(vak_info, vak)
	print(college_type)
	for i in range (0,round(college_type[0]):
		print('hc')
	for i in range (0,college_type[1]):
		print('wc')
	for i in range (0,college_type[2]):
		print('pr')
"""	
"""
	if vak_info["vakken"] == vak:
		print(vak_info)
		print(vak_info["hoorcolleges"])
		p = vak_info["hoorcolleges"]
		y = int(p)
		print(y) 
		hc = int(vak_info["hoorcolleges"])
		for i in range(1,hc):
			vak_naam = "hc_" + str(i) + "_" + vak
			group_student_database.setdefault(vak_naam, []).append(subject_student_database[vak])
print(group_student_database)		

"""

		#word[1:]


##------------------------------FUNCTIES----------------------------##


#Geeft aantal keer dat vak gegeven wordt per week
#input is vak_info en naam van vak dat gezocht moet worden
def aantalcollegesinweek(vakinfo, vak):
	for info in vakinfo:
		if info["vakken"] == vak:
			hc = float(info["hoorcolleges"])
			wc = float(info["werkcolleges"])
			pr = float(info["practica"])
			total = hc + wc + pr
			#return {'hc': hc, 'wc': wc, 'pr': pr, 'tot':total}
			return {hc,wc,pr}
#Geeft aantal beschikbare dagen volgens bonus regeling
#input is aantal x college in de week
def bonusdageninweek(aantalx):
	if aantalx == 4:
		return ['ma', 'di', 'do', 'vr']
	if aantalx == 3:
		return ['ma', 'wo', 'vr']
	if aantalx == 2:
		return [{'ma', 'di'}, {'do', 'vr'}]
	else:
		return ['ma', 'di', 'wo', 'do', 'vr']





"""
#Loop over vakken, begin bij 't grootste vak
for number in sorted(subject_student_number.values(), reverse=True):
	subject = number_student_subject[number]
	#Hoe vaak wordt vak gegeven in de week?
	times_week = int(aantalcollegesinweek(vak_info, subject))
	#Welke dagen mogen er geroosterd worden volgens bonusregeling
	possible_days = bonusdageninweek(times_week)
	#loop over details per vak
	for subject_details in vak_info:
		#check of dit het vak is waar je details van wil
		if subject in subject_details.values():
			#gebruik details
			#print(subject_details)
			# subject is naam van vak
			#number is aantal studenten
			hc = int(subject_details["hoorcolleges"])
			wc = int(subject_details["werkcolleges"])
			pr = int(subject_details["practica"])
#			print(subject)
			
			for x in range(0,hc):
#				print(hc)
#				print(number)
		for x in range(0,wc):
				wc_max = int(subject_details["werk_max_stud"])
#				print(wc)
#				print(wc_max)
				number2 = int(number/wc_max)
#				print(number2)
			for x in range(0,pr):
				pr_max = int(subject_details["practica_max_stud"])
#				print(pr)
				number2 = int(number/pr_max)
#				print(number2)
"""

studenten_roostering.close()
vakinfo.close()