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
		#print(day, time, room)
		#print(rooster[day][time][room])
	else:
		roosteren(vak, timetable, gro_stu_dat)

def aantalcollegesinweek(vakinfo, vak):
	for info in vakinfo:
		if info["vakken"] == vak:
			hc = float(info["hoorcolleges"])
			wc = float(info["werkcolleges"])
			pr = float(info["practica"])
			total = int(hc + wc + pr)
			#return {'hc': hc, 'wc': wc, 'pr': pr, 'tot':total}
			return (total)

def bonusdageninweek(aantalx):
	if aantalx == 4:
		return ['ma', 'di', 'do', 'vr']
	if aantalx == 3:
		return ['ma', 'wo', 'vr']
	if aantalx == 2:
		return [['ma', 'do'], ['di', 'vr']]
	else:
		return ['ma', 'di', 'wo', 'do', 'vr']

def score_distr(weekrooster, vak):
	score = 0
	aantal_contacturen = aantalcollegesinweek(vak_info, vak)
	dagen_in_weekr = len(set(weekrooster))
	if(aantal_contacturen > 1):
		geen_minpunten = 0
		if (dagen_in_weekr == (aantal_contacturen - 1)):
			score -= 10
			geen_minpunten += 1
		if(dagen_in_weekr == (aantal_contacturen - 2)):
			score -= 20
			geen_minpunten += 1
		if(dagen_in_weekr == (aantal_contacturen - 3)):
			score -= 30
			geen_minpunten += 1
		if(geen_minpunten == 0):
			ideale_weekr = bonusdageninweek(aantal_contacturen)
			print("ideaal: ", ideale_weekr)
			check = 0
			if (aantal_contacturen == 2):
				for i in range(0, 2):
					compare = set(weekrooster) & set(ideale_weekr[i])
					if(len(compare) == aantal_contacturen):
						check += 1
				if(check > 0):
					score += 20
			else:
				compare = set(weekrooster) & set(ideale_weekr)
				if(len(compare) == aantal_contacturen):
					score += 20
	return(score)

for subject in list(group_student_database.keys()):
	roosteren(subject, rooster, group_student_database)

# bouw dict met alle vaknamen
def rooster_dagen_vd_week():
	vak_dict = {}
	for i in range(len(all_subject_names)):
		vak_dict[all_subject_names[i]] = []
	# bouw per vak het aantal events in een list, dus: wo0, ma2, ma1, ma0 etc.
	vakken = []
	for dag in rooster.keys():
		for tijd in rooster[dag].keys():
			for lokaal in rooster[dag][tijd].keys():
				for vak in rooster[dag][tijd][lokaal].keys():
					vakken.append(vak)
					vaknaam_1 = vak[7:]

					if(vak[0] == "h"):
						event = dag[:2] + str(0)
						vak_dict[vaknaam_1].append(event)
					else:
						event = dag[:2] + vak[5]
						vak_dict[vaknaam_1].append(event)
	return vak_dict

# geef totaal min en plus per vak aan totaalscore
def eva_minplus_dagenweek():
	totaalscore = 0
	vakken = rooster_dagen_vd_week()
	for vak in vakken:
		print("\n\n", vakken[vak])
		buffer1 = []
		# append iedere groep en bepaal max waarde
		for i in range(0, len(vakken[vak])):
			buffer1.append(int(vakken[vak][i][2]))
		groepen = max(buffer1)
		print("groepen: ", groepen)
		aantal_contacturen = aantalcollegesinweek(vak_info, vak)
		print("contacturen: ", aantal_contacturen)


		# per groep in weekroosters multi
		score_vak = 0
		if(aantal_contacturen > 1):
			if(groepen > 0):
				group_scores = []
			# maak weekrooster voor iedere groep
				for j in range(1,(groepen + 1)):
					weekrooster_enkel = []
					# rooster voor 1 groep
					for k in range(len(vakken[vak])):
						if(vakken[vak][k][2] == "0"):
							weekrooster_enkel.append(vakken[vak][k][:2])
						check = int(vakken[vak][k][2])
						if(check == j):
							weekrooster_enkel.append(vakken[vak][k][:2])
					#score subgroep
					enkel_score = score_distr(weekrooster_enkel, vak)
					group_scores.append(enkel_score)
					print (weekrooster_enkel)
					print (enkel_score)
				score_vak = min(group_scores)
				print ("score_vak: ", score_vak)
				
			else:
				weekrooster_enkel = []
				for l in range(len(vakken[vak])):
					weekrooster_enkel.append(vakken[vak][l][:2])
				print(weekrooster_enkel)
				score_vak = score_distr(weekrooster_enkel, vak)
				print ("score_vak: ", score_vak)
			totaalscore = totaalscore + score_vak
			print("vaktussenstand: ", totaalscore)
	print ("totaal: ", totaalscore)
	return totaalscore

##-----------------------------------VANAF HIER IS HET ROOSTER RANDOM & GELDIG---------------------------##

studenten_roostering.close()
vakinfo.close()