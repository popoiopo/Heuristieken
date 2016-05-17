"""
Heuristics:

Bas Chatel
Bram Sloots
Job Huisman

"""

##---------------Loading libraries -------------------------------------------##
import csv
import math
import time
import random
import copy
import queue
#import xlsxwriter
import collections
from copy import deepcopy
from fnmatch import fnmatch, fnmatchcase
from string import ascii_lowercase
from random import shuffle

##---------------Parameter values --------------------------------------------##
# Decides the ratio of emptyness/fullnes of the classrooms
parameter_workgroupsizes = 0.21 #0.41 and 0.61 are also interesting values
best_scores_maxsize = 40 #onthoud n aantal beste random gemaakte roosters
n_random_tests = (best_scores_maxsize+1) #genereert n aantal random roosters waarvan de beste (n=best_scores_maxsize) worden onthouden

n_generaties = 30 #maak n generaties
max_faults_in_recombination = 120 #maximum recombination faults is n
population_size_per_generation = int(3*best_scores_maxsize) #laat populatie groeien tot deze size voordat selectie wordt toegepast
selection_on_population = int(1*best_scores_maxsize) #graag van selectie; n=1 is constante populatie

time_0 = time.time()
##---------------Loading and organising CSV files ----------------------------##
# Loading info out of csv file
student_scheduling	= open("studenten_roostering.csv")
course_info 		= open("vakinfo.csv")
# Reading csv file
csv_students 		= csv.reader(student_scheduling)
csv_courses 		= csv.reader(course_info)
# Create dict/array out of csv file data
data_students 		= [row for row in csv_students]
data_courses 		= [row for row in csv_courses] 
# Extracts variable names
header_students 	= [name for name in data_students[0]]
header_courses 		= [name for name in data_courses[0]]

##---------------Creating dicts containing info ------------------------------##
# Create dicts of data for each variable
student_info 	= [dict(zip(header_students, check)) for check in data_students]
course_info	 	= [dict(zip(header_courses, check)) for check in data_courses]
classroom_info 	= {"A1.04" : 41, "A1.06" : 22, "A1.08" : 20, "A1.10" : 56, 
		"B0.201" : 48, "C0.110" : 117, "C1.112" : 60}
# Create dict of student/course/classroom vs details
info_student 	= [dict(zip(check, header_students)) for check in data_students]
info_course	 	= [dict(zip(check, header_courses)) for check in data_courses]
info_classroom 	= {41 : "A1.04", 22 : "A1.06", 20 : "A1.08", 56 : "A1.10", 
		48 : "B0.201", 117 : "C0.110", 60 : "C1.112"}

##---------------All courses/days/time frames --------------------------------##
all_subject_names = ['Advanced_Heuristics',"Algoritmen_en_complexiteit",
	"Analysemethoden_en_technieken","Architectuur_en_computerorganisatie",
	"Autonomous_Agents_2","Bioinformatica","Calculus_2",
	"Collectieve_Intelligentie","Compilerbouw","Compilerbouw_practicum",
	"Data_Mining","Databases_2","Heuristieken_1","Heuristieken_2",
	"Informatie_en_organisatieontwerp","Interactie_ontwerp","Kansrekenen_2",
	"Lineaire_Algebra","Machine_Learning","Moderne_Databases",
	"Netwerken_en_systeembeveiliging","Programmeren_in_Java_2",
	"Project_Genetic_Algorithms","Project_Numerical_Recipes",
	"Reflectie_op_de_digitale_cultuur","Software_engineering",
	"Technology_for_games","Webprogrammeren_en_databases",
	"Zoeken_sturen_en_bewegen"]

days_in_week = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag']

time_frames = ['9.00-11.00', '11.00-13.00', '13.00-15.00', '15.00-17.00']

##---------------Functions ---------------------------------------------------##
##---------------Creating timetable ------------------------------------------##

# Creates empty time table: day->timeslot->classroom----------------------------
# Classroom will later be filled with unique course/workgroup name with students
def empty_timetable(week, timeslots, classroom_info):
	time_table = {}
	for day in week:
		time_table[day] = {}
		for timeslot in timeslots:
			time_table[day][(timeslot)] = {}
			for classroom in classroom_info:
				time_table[day][(timeslot)][classroom] = {}
	return time_table

# Schedules courses in empty slots----------------------------------------------
def scheduling(course, timetable, gro_stu_dat, week, timeslots, classroom_info):
	day = random.choice(week)
	time = random.choice(timeslots)
	room = random.choice(list(classroom_info.keys()))
	if not bool(timetable[day][time][room]):
		timetable[day][time][room][course] = gro_stu_dat[course]
	else:
		scheduling(course, timetable, gro_stu_dat, week, timeslots, classroom_info)

###Brammm start
def scheduling2(course, timetable, gro_stu_dat, week, timeslots, classroom_info):
	day = random.choice(week)
	time = random.choice(timeslots)
	room = random.choice(list(classroom_info.keys()))
	if not bool(timetable[day][time][room]):
		timetable[day][time][room][course] = gro_stu_dat[course]
	else:
		scheduling(course, timetable, gro_stu_dat, week, timeslots, classroom_info)
###Brammm end



# Picks random day-timeslot-classroom in the week-------------------------------
def make_random_timetable(random_timetable, student_database, week, timeslots, classroom_info):
	for subject in list(student_database.keys()):
		scheduling(subject, random_timetable, student_database, week, timeslots, classroom_info)
	return random_timetable

##---------------Evaluation functions ----------------------------------------##

# Checks if there are student that are scheduled double within the same timeslot
def duplicate_student(time_table):
	counter_minus = 0
#	print(time_table)
	for day in time_table.keys():
		for timeslot in time_table[day].keys():
			student_check=[]
			for classroom in time_table[day][timeslot].keys():
				for course in time_table[day][timeslot][classroom].keys():
					for student in time_table[day][timeslot][classroom][course]:
						if student in student_check:
							counter_minus-=1
						else:
							student_check.append(student)
	return(counter_minus)

# Checks if the amount of students exceed the capacity of the classroom---------
def minus_classrooms(time_table):
	minus_points_classrooms = 0
	for day in time_table.keys():
		for timeslot in time_table[day].keys():
			for classroom in time_table[day][timeslot].keys():
				for keys in time_table[day][(timeslot)][classroom]:
					x = (classroom_info[classroom]-(len(time_table[day][(timeslot)][classroom][keys])))
					if x < 0:
						minus_points_classrooms += x
	return(minus_points_classrooms)

# Counts how many activities a course has per week------------------------------
def activity_amount_week(course_info, course):
	for info in course_info:
		if info["vakken"] == course:
			hc = float(info["hoorcolleges"])
			wc = float(info["werkcolleges"])
			pr = float(info["practica"])
			total = int(hc + wc + pr)
			return (total)

# Returns the ideal distribution of course activities in a week-----------------
def week_distribution_bonus(amount_activities):
	if amount_activities == 4:
		return ['ma', 'di', 'do', 'vr']
	if amount_activities == 3:
		return ['ma', 'wo', 'vr']
	if amount_activities == 2:
		return [['ma', 'do'], ['di', 'vr']]
	else:
		return ['ma', 'di', 'wo', 'do', 'vr']

# Calculates the bonus/minus points from the course activity distribution-------
def score_distr(time_table_week, course, course_info):
	score = 0
	course_activity_counter = activity_amount_week(course_info, course)
	days_in_week = len(set(time_table_week))
	if(course_activity_counter > 1):
		no_minus_points = 0
		if (days_in_week == (course_activity_counter - 1)):
			score -= 10
			no_minus_points += 1
		if(days_in_week == (course_activity_counter - 2)):
			score -= 20
			no_minus_points += 1
		if(days_in_week == (course_activity_counter - 3)):
			score -= 30
			no_minus_points += 1
		if(no_minus_points == 0):
			ideal_week = week_distribution_bonus(course_activity_counter)
			check = 0
			if (course_activity_counter == 2):
				for i in range(0, 2):
					compare = set(time_table_week) & set(ideal_week[i])
					if(len(compare) == course_activity_counter):
						check += 1
				if(check > 0):
					score += 20
			else:
				compare = set(time_table_week) & set(ideal_week)
				if(len(compare) == course_activity_counter):
					score += 20
	return(score)

# Creates a dict with all the course names--------------------------------------
def schedule_days_of_week(time_table, all_subject_names):
	course_dict = {}
	for i in range(len(all_subject_names)):
		course_dict[all_subject_names[i]] = []
	# create per course amount of events in list, so: we0,mo2,mo1,mo0 
	courses = []
	for day in time_table.keys():
		for timeslot in time_table[day].keys():
			for classroom in time_table[day][timeslot].keys():
				for course in time_table[day][timeslot][classroom].keys():
					courses.append(course)
					course_name_1 = course[7:]
					if(course[0] == "h"):
						event = day[:2] + str(0)
						course_dict[course_name_1].append(event)
					else:
						event = day[:2] + course[5]
						course_dict[course_name_1].append(event)
	return course_dict

# Gives total of bonus/minus for each course------------------------------------
def bonus_distribution(time_table, all_subject_names, course_info): 
	score_total = 0
	courses = schedule_days_of_week(time_table, all_subject_names)
	for course in courses:
		buffer1 = []
		# appends every group and assesses max value
		for i in range(0, len(courses[course])):
			buffer1.append(int(courses[course][i][2]))
		groups = max(buffer1)
		course_activity_counter = activity_amount_week(course_info, course)
		course_score = 0
		if(course_activity_counter > 1):
			if(groups > 0):
				group_scores = []
				# create time table for each group
				for j in range(1,(groups + 1)):
					single_time_table_week = []
					# time table for one group
					for k in range(len(courses[course])):
						if(courses[course][k][2] == "0"):
							single_time_table_week.append(courses[course][k][:2])
						check = int(courses[course][k][2])
						if(check == j):
							single_time_table_week.append(courses[course][k][:2])
					#score subgroup
					single_score = score_distr(single_time_table_week, course, course_info)
					group_scores.append(single_score)
				course_score = min(group_scores)
			else:
				single_time_table_week = []
				for l in range(len(courses[course])):
					single_time_table_week.append(courses[course][l][:2])
				course_score = score_distr(single_time_table_week, course, course_info)
			score_total = score_total + course_score
	return score_total

# Returns total of points a timetable is worth----------------------------------
def time_table_points(time_table, totaal_punten, punten_dubbele_roostering, 
			punten_lokaal_capaciteit, punten_verdeling_week):
	punten_dubb_roos = duplicate_student(time_table)
	punten_loka_capa = minus_classrooms(time_table)
	punten_verd_week = bonus_distribution(time_table, all_subject_names, course_info)
	punten_tot = 1000 + punten_dubb_roos + punten_loka_capa + punten_verd_week

#	print(totaal_punten)
	totaal_punten.append(punten_tot)
	punten_dubbele_roostering.append(punten_dubb_roos)
	punten_lokaal_capaciteit.append(punten_loka_capa)
	punten_verdeling_week.append(punten_verd_week)
	return

##---------------Top time tables ---------------------------------------------##

# Keeps track of best time tables for further use-------------------------------
def multiple_timetables(time_table):
	best_time_table = []
	for i in range(0, 1):
		for subject in list(group_student_database.keys()):
			scheduling(subject, random_timetable, student_database, week, timeslots, classroom_info)
		if not best_time_table:
			best_time_table = deepcopy(time_table)
		highest_score = time_table_points(best_time_table)
		new_score = time_table_points(time_table)
		if highest_score < new_score:
			best_time_table = deepcopy(time_table)
			highest_score = time_table_points(best_time_table)
		time_table.clear()
	return highest_score, best_time_table

##---------------Remember best n timetables -----------------------------------##
#compare Ttable score to lowest score of stored Ttables and replace if better.
def take_best_scores(scores, passed_scores, table, x, max_size):
	key = sorted(scores.keys())[0]
	min_value_0 = key
	min_value_1 = scores.pop(key)
	Ttable = {}
	if passed_scores[x] > min_value_0:
		Ttable = copy.deepcopy(table)
		if passed_scores[x] in passed_scores[:(x-1)]:
#			print('oeps')
			check = unique_score(score_total, score_total[i])
			passed_scores[x] = check
		scores[passed_scores[x]] = copy.deepcopy(Ttable)
		Ttable.clear()
		if len(list(scores.keys())) < max_size:
			scores[min_value_0] = copy.deepcopy(min_value_1)
	else:
		scores[min_value_0] = copy.deepcopy(min_value_1)
	return scores

def take_best_scores2(score, passed_scores, table, x, abc):
	recent_score = passed_scores.pop(x)
	previous_best_score = sorted(passed_scores, reverse = True)[0]
	Ttable = {}
	if recent_score > previous_best_score:
###		print('DEZE IS BETER!!!!', x)
		Ttable = copy.deepcopy(table)
		score = copy.deepcopy(Ttable)
		Ttable.clear()
	passed_scores.append(recent_score)
	return score

#chekc if value is already in priority queue, if so, change value to prevent error
def unique_score(Score, value):
	if value in Score:
#		print('in keys is', value)
		value -= 0.1
		return unique_score(Score, value)
	else:
#		print('not in keys is', value)
		return value

##-----------------Mutaties op rooster voor Hillclimber----------------------##
def delete_random_subject(table):
	days = list(table.keys())
	day = random.choice(days)
	times = list(table[day].keys())
	time = random.choice(times)
	rooms = list(table[day][time].keys())
	room = random.choice(rooms)
	if not bool(table[day][time][room]):
		check = delete_random_subject(table)
		return check
	else:
		subject = copy.deepcopy(table[day][time][room])
		for check in subject.keys():
			delete = table[day][time][room].pop(check)
			subject_name = check
###		print(subject_name ,'wordt gedelete uit het rooster')
		return subject_name

##---------------Filling the courses -----------------------------------------##
subject_student_database = {}
for subject in all_subject_names:
	for student in student_info:
		number = student['Stud.Nr.']
		for info in info_student:
			if number in info:
				if subject in info:
					subject_student_database.setdefault(subject, []).append(number)


##---------------Create list of unique courses and students within -----------##
# Create regular classes, work and practical lessons with string is 
# studentnumbers of students attending those courses
group_student_database = {}
for subject in all_subject_names:
	for subject_details in course_info:
		if subject in subject_details.values():
			subject_student_number = float(len(subject_student_database[subject]))
			# give lecture unique name and add to list
			hc = int(subject_details["hoorcolleges"])
			for i in range(1,hc+1):
				course_name = "hc_" + str(i) + "_1_" + subject
				group_student_database[course_name] = subject_student_database[subject]
			# give work groups unique name and add to list
			wc = int(subject_details["werkcolleges"])
			for i in range(1,wc+1):
				# checks amount of work groups needed depending on parameter
				# defined on top
				stud_over_max = subject_student_number / float(subject_details["werk_max_stud"])
				if (stud_over_max % 1) > parameter_workgroupsizes:
					wc_number = int(stud_over_max) + 1
				else:
					wc_number = int(stud_over_max)
				check = int(math.ceil((subject_student_number / wc_number)))
				x = 0
				# Loop over all work groupd and make groupes of average size
				for j in range(1,wc_number+1): #later ABC?
					course_name = "wc_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database[course_name] = subject_student_database[subject][x:x+check]
					x += check
			pr = int(subject_details["practica"])
			for i in range(1,pr+1):
				stud_over_max = subject_student_number / float(subject_details["practica_max_stud"])
				if (stud_over_max % 1) > parameter_workgroupsizes:
					pr_number = int(stud_over_max) + 1
				else:
					pr_number = int(stud_over_max)
				check = int(math.ceil((subject_student_number / pr_number)))
				x = 0
				for j in range(1,pr_number+1): #later ABC?
					course_name = "pr_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database[course_name] = subject_student_database[subject][x:x+check]
					x += check



####Brammm start
##---------------As of now all timetables are random and valid ---------------##
#scores voor random roosters
score_total = []
score_double_students = []
score_classrooms = []
score_ditribution_in_week = []
#scores voor Genetic Algorithm key = generation
score_total_GenAl = {}
score_double_students_GenAl = {}
score_classrooms_GenAl = {}
score_ditribution_in_week_GenAL = {}

best_scores_random = {} #dict voor beste n roosters van random gemaakte roosters
best_scores_hillcl = {} #dict om beste n roosters te muteren in hillclimber
best_scores_GenAl = {}

best_scores_random = {-10001: 'lala'} #noodzakelijke nulwaarde om programma te laten werken
#maak n_radom_tests timetables, bewaar de best_scores_maxsize beste daarvan
for i in range(0,n_random_tests):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	best_scores_random = take_best_scores(best_scores_random, score_total, time_table, i, best_scores_maxsize)
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt', x,'seconden voor het genereren van', n_random_tests, 'random roosters')
print('De beste', best_scores_maxsize,'roosters zijn bewaard in een dict onder de volgende keys')
print(best_scores_random.keys())

##-----------------functie voor genetic algotrithmen----------------------##
def time_table_points2(time_table):
	p_dubb_roos = duplicate_student(time_table)
	p_loka_capa = minus_classrooms(time_table)
	p_verd_week = bonus_distribution(time_table, all_subject_names, course_info)
	p_tot = 1000 + p_dubb_roos + p_loka_capa + p_verd_week
	return p_tot

def take_two_diff_genes(all_genes):
	gen1 = random.choice(all_genes)
	gen2 = random.choice(all_genes)
	if gen1 == gen2:
		return take_two_diff_genes(all_genes)
	return(gen1,gen2)

def check_geldigheid_rooster(table, gene_pool, parent1, parent2):
	count_unique_subjects = 0
	count_empty_spaces = 0
	count_double_subjects = 0
	count_all_options = 0
	check_all_subjects = copy.deepcopy(list(group_student_database.keys()))
#	days = list(table.keys())
#	random.shuflle(days, random.random)
#	for day in days:
	for day in table.keys():
		for timeslot in table[day].keys():
			for classroom in table[day][timeslot].keys():
				count_all_options+=1
				if not bool(table[day][timeslot][classroom]):
					count_empty_spaces += 1
#					if I > 1:
#						print(day, timeslot, classroom)
				if bool(table[day][timeslot][classroom]):
					subject = list(table[day][timeslot][classroom].keys())[0]
					if subject in check_all_subjects:
						count_unique_subjects += 1
						position = check_all_subjects.index(subject)
						check_all_subjects.pop(position)
					else:
						count_double_subjects += 1
						table[day][timeslot][classroom].pop(subject)
	if (len(check_all_subjects)) < max_faults_in_recombination:
		for rescedule_subject in check_all_subjects:
			scheduling(rescedule_subject, table, group_student_database, days_in_week, time_frames , classroom_info)
#		print(count_double_subjects)
###		if len(check_all_subjects) < 10:
###		print (len(check_all_subjects), count_unique_subjects)
#		if (count_double_subjects) < 10:
#			print(len(check_all_subjects), count_double_subjects)
#			print(count_empty_spaces, 'empty classrooms')
#			print(count_double_subjects, 'double subjects')
		return True
#	if (len(check_all_subjects)) < 18:
#		print(count_empty_spaces, 'empty classrooms')
#		print((parent1+parent2))
#		print(count_all_options, 'zijn alle doorlopen tijdslots')
#		print(len(check_all_subjects), (count_double_subjects), 'zijn dubbel geroosterd')
#		print(count_empty_spaces, 'zijn alle lege lokalen')
#		print((count_empty_spaces+count_double_subjects), 'plekken in het rooster zijn leeg of dubbel')
#		return True

def mutation(ttable, week, timeslots , classroom_info):
	day = random.choice(week)
	time = random.choice(timeslots)
	room = random.choice(list(classroom_info.keys()))
	if not bool(timetable[day][time][room]):
		mutation(ttable, week, timeslots , classroom_info)
	else:
		subject = list(table[day][timeslot][classroom].keys())[0]
		timetable[day][time][room].pop(subject)

def recombine_genes(parent1, parent2, population_all_parents, genes):
	table1 = copy.deepcopy(population_all_parents[parent1])
	table2 = copy.deepcopy(population_all_parents[parent2])
	recombination_table = {}
	days = list(table1.keys())
	random.shuffle(days, random.random)
	recombination_table[days[0]] = table2[days[0]]
	recombination_table[days[1]] = table1[days[1]]
	recombination_table[days[2]] = table1[days[2]]
	recombination_table[days[3]] = table2[days[3]]
	recombination_table[days[4]] = table1[days[4]]
	if not bool(check_geldigheid_rooster(recombination_table, genes, parent1, parent2)):
		recombination_table.clear()
	else:
#	elif bool(check_geldigheid_rooster(recombination_table, genes, parent1, parent2)):
		points = time_table_points2(recombination_table)
		check_scores = list(population_all_parents.keys())
		if points in check_scores:
#			print('change original score')
			points = unique_score(check_scores, points)
#			print(list(population_all_parents.keys()))
#			print(points)
#		print(points)
		population_all_parents[points] = recombination_table
#		print(len(list(population_all_parents.keys())))
		return True

def make_new_generation(old_generation_dict):
	gene_pool = list(best_scores_random.keys())
	mean_value_genepool = mean_value(gene_pool)
	size_population_parents = len(list(old_generation_dict.keys()))
	print('print grootte van populatie ouders',size_population_parents)
	print('met een gemiddelde waarde van', mean_value_genepool)
#	print('print beoogde populatie grootte', size_population_parents + population_size_per_generation)
	while len(list(old_generation_dict.keys())) < (size_population_parents + population_size_per_generation):
		(gen1, gen2) = take_two_diff_genes(gene_pool)
		recombine_genes(gen1, gen2, old_generation_dict, gene_pool)

def select_new_population(population):
	old_population = copy.deepcopy(population)
	population.clear()
	population_scores = sorted(list(old_population.keys()), reverse = True)
	i = 0
	while len(list(population.keys())) < (selection_on_population):
#	for i in range(0,selection_on_population):
		select = i/(i+1)
#		select = (population_scores[i] / (pow(population_scores[i], i)*1.01))

		if select > random.random() :
			key = population_scores[i]
			population[key] = old_population[key]
		else:
			print('denied')
		i+=1
#	print('print aantal ouders voor volgende generatie', len(population.keys()))

def mean_value(list_values):
	size = len(list_values)
	total = 0
	mean = 0
	for i in range(0,size):
		total += list_values[i]
	mean = (total/size)
	return mean

###--------------einde functies--------------------###
#Sla scores op voor de nulde generatie
score_total_GenAl[0]=[]

#Loop over generaties
I = 1
while I < (n_generaties+1):
	print('generation', I)
	scores_generation = list(best_scores_random.keys())
	print(sorted(scores_generation, reverse = True))
	make_new_generation(best_scores_random)
#	print('print lengte totale populatie', len(list(best_scores_random.keys())))
	select_new_population(best_scores_random)
	I += 1

time_n = time.time()
x = time_n - time_0
print('Het duurt', x,'seconden voor het hele programma')
###Brammm end

student_scheduling.close()



