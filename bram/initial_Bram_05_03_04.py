"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""

##---------------Inladen Informatie ---------------------------------------------##
import csv
import math
import random
import time
import copy
import queue
from copy import deepcopy
from fnmatch import fnmatch, fnmatchcase
from queue import PriorityQueue

##---------------Parameter waardes ----------------------------------------------##
#bepaalt hoe vol/leeg de werkgroepen mogen zijn
parameter_werkgroep_grootte = 0.21 #0.41 en 0.61 zijn ook interessante grenzen

all_subject_names = ['Advanced_Heuristics',"Algoritmen_en_complexiteit","Analysemethoden_en_technieken","Architectuur_en_computerorganisatie",
"Autonomous_Agents_2","Bioinformatica","Calculus_2","Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum","Data_Mining",
"Databases_2","Heuristieken_1","Heuristieken_2","Informatie_en_organisatieontwerp","Interactie_ontwerp","Kansrekenen_2",
"Lineaire_Algebra","Machine_Learning","Moderne_Databases","Netwerken_en_systeembeveiliging","Programmeren_in_Java_2",
"Project_Genetic_Algorithms","Project_Numerical_Recipes","Reflectie_op_de_digitale_cultuur","Software_engineering",
"Technology_for_games","Webprogrammeren_en_databases","Zoeken_sturen_en_bewegen"]
days_in_week = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag']
time_frames = ['9.00-11.00', '11.00-13.00', '13.00-15.00', '15.00-17.00']



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

##---------------Functies ----------------------------------------------##
def duplicate_student(rooster):
	counter_malus = 0
	for dag in rooster.keys():
		for tijdslot in rooster[dag].keys():
			student_check=[]
			for zaal in rooster[dag][tijdslot].keys():
				for vak in rooster[dag][tijdslot][zaal].keys():
					for student in rooster[dag][tijdslot][zaal][vak]:
						if student in student_check:
							counter_malus-=1
						else:
							student_check.append(student)
	return(counter_malus)

def malus_lokalen(rooster):
	min_punten_lokalen = 0
	for dag in rooster.keys():
		for tijdsl in rooster[dag].keys():
			for lok in rooster[dag][tijdsl].keys():
				for keys in rooster[dag][(tijdsl)][lok]:
					x = (lokalen_info[lok]-(len(rooster[dag][(tijdsl)][lok][keys])))
					if x < 0:
						min_punten_lokalen += x
	return(min_punten_lokalen)

#def rooster_punten(rooster):
#	return 1000 - duplicate_student(rooster) + malus_lokalen(rooster)

def roosteren(vak, timetable, gro_stu_dat, week, tijdslots, classroom_info):
	day = random.choice(week)
#	time = random.choice(timetable[day].keys())
#	room = random.choice(timetable[day][time].keys())
	time = random.choice(tijdslots)
	room = random.choice(list(lokalen_info.keys()))
	if not bool(timetable[day][time][room]):
		timetable[day][time][room][vak] = gro_stu_dat[vak]
	else:
		roosteren(vak, timetable, gro_stu_dat, week, tijdslots, classroom_info)



#Maak een leeg rooster van dicts in volgorde dag->tijdslot->lokalen
#Toe te voegen; Dict met key vak en values studNrs van studenten uit vak/werkgroep
def empty_timetable(week, tijdslots, classroom_info):
	time_table = {}
	for dag in week:
		time_table[dag] = {}
		for tijdsl in tijdslots:
			time_table[dag][(tijdsl)] = {}
			for lok in classroom_info:
				time_table[dag][(tijdsl)][lok] = {} #voeg dict met studenten toe
	return time_table


##-------------------------------KIES RANDOM DAG-TIJDSLOT-LOKAAL IN DE WEEK-----------------------------##
def make_random_timetable(random_timetable, student_database, week, tijdslots, classroom_info):
	for subject in list(student_database.keys()):
		roosteren(subject, random_timetable, student_database, week, tijdslots, classroom_info)
	return random_timetable


##----------------------functies job-------------------------##

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

def score_distr(weekrooster, vak, vak_info):
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
#			print("ideaal: ", ideale_weekr)
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

# bouw dict met alle vaknamen
def rooster_dagen_vd_week(rooster, all_subject_names):
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
def bonus_distribution(rooster, all_subject_names, vak_info): 
	totaalscore = 0
	vakken = rooster_dagen_vd_week(rooster, all_subject_names)
	for vak in vakken:
#		print(vakken[vak])
#		print(vak)
		buffer1 = []
		# append iedere groep en bepaal max waarde
		for i in range(0, len(vakken[vak])):
			buffer1.append(int(vakken[vak][i][2]))
		groepen = max(buffer1)
#		print("groepen: ", groepen)
		aantal_contacturen = aantalcollegesinweek(vak_info, vak)
#		print("contacturen: ", aantal_contacturen)
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
					enkel_score = score_distr(weekrooster_enkel, vak, vak_info)
					group_scores.append(enkel_score)
#					print (weekrooster_enkel)
#					print (enkel_score)
				score_vak = min(group_scores)
#				print ("score_vak: ", score_vak)
			else:
				weekrooster_enkel = []
				for l in range(len(vakken[vak])):
					weekrooster_enkel.append(vakken[vak][l][:2])
#				print(weekrooster_enkel)
				score_vak = score_distr(weekrooster_enkel, vak, vak_info)
#				print ("score_vak: ", score_vak)
			totaalscore = totaalscore + score_vak
#			print("vaktussenstand: ", totaalscore)
#	print ("totaal: ", totaalscore)
	return totaalscore

##----------------------einde functies JOB-----------------------------##
def rooster_punten(rooster, totaal_punten, punten_dubbele_roostering, punten_lokaal_capaciteit, punten_verdeling_week):
	punten_dubb_roos = duplicate_student(rooster)
	punten_loka_capa = malus_lokalen(rooster)
	punten_verd_week = bonus_distribution(rooster, all_subject_names, vak_info)
#	punten_verd_week = 1
	punten_tot = 1000 + punten_dubb_roos + punten_loka_capa + punten_verd_week

	totaal_punten.append(punten_tot)
	punten_dubbele_roostering.append(punten_dubb_roos)
	punten_lokaal_capaciteit.append(punten_loka_capa)
	punten_verdeling_week.append(punten_verd_week)
	return

#chekc if value is already in priority queue, if so, change value to prevent error
def unique_score(Score, value):
#	print(Score)
	print(value)
	if value in Score:
		value -= 1
		unique_score(Score, value)	
	return value

#compare Ttable score to lowest score of stored Ttables and replace if better.
def take_best_scores(scores, passed_scores, table, x, max_size):
	key = sorted(scores.keys())[0]
	min_value_0 = key
	min_value_1 = scores.pop(key)
	Ttable = {}
	if passed_scores[x] > min_value_0:
		Ttable = copy.deepcopy(table)
		print(passed_scores[x])
		if passed_scores[x] in passed_scores[:(x-1)]:
			print('oeps')
			check = unique_score(score_total, score_total[i])
			passed_scores[x] = check
		scores[passed_scores[x]] = Ttable
		Ttable.clear()
		if len(scores) < max_size:
			scores[min_value_0] = min_value_1
	else:
		scores[min_value_0] = min_value_1
	return scores

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

##-----------------------------------VANAF HIER IS HET ROOSTER RANDOM & GELDIG---------------------------##
time_1 = time.time()


score_total = []
score_double_students = []
score_classrooms = []
score_ditribution_in_week = []

best_scores = {}
best_scores_maxsize = 20
best_scores = {23: 'lala', 29: 'haha', 9: 'hihi'}
for i in range(0,3000):
	rooster = empty_timetable(days_in_week, time_frames, lokalen_info)
	rooster = make_random_timetable(rooster, group_student_database, days_in_week, time_frames, lokalen_info) #days_in_week, time_frames, lokalen_info mag uit input gehaald
	rooster_punten(rooster, score_total, score_double_students, score_classrooms, score_ditribution_in_week)
	rooster1 = {'hallo': 'test'}
	best_scores = take_best_scores(best_scores, score_total, rooster1, i, best_scores_maxsize)

	rooster.clear()

#print(score_total)
#print(score_classrooms)
#print(score_double_students)
#print(score_ditribution_in_week)


time_2 = time.time()
x = time_2-time_1

print(best_scores.keys())
print(x)











##---------later te gebruiken om beste roosters te bewaren---------------##
def multiple_timetables(rooster):
	beste_rooster = []
	for i in range(0, 1):
		for subject in list(group_student_database.keys()):
			roosteren(subject, random_timetable, student_database, week, tijdslots, classroom_info)
		if not beste_rooster:
			beste_rooster = deepcopy(rooster)
		hoogste_punt = rooster_punten(beste_rooster)
		nieuw_punt = rooster_punten(rooster)
		if hoogste_punt < nieuw_punt:
			beste_rooster = deepcopy(rooster)
			hoogste_punt = rooster_punten(beste_rooster)
		rooster.clear()
	return hoogste_punt, beste_rooster






studenten_roostering.close()
vakinfo.close()