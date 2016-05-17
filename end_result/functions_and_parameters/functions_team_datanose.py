"""
This is our own library where all the functions we use for this project are
save to be exported to the main file.

"""
##---------------Loading libraries -------------------------------------------##
import math
import time
import copy
import queue
import config
import random
import xlsxwriter
import collections
from config import *
from copy import deepcopy
from random import shuffle
from string import ascii_lowercase
from fnmatch import fnmatch, fnmatchcase

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

def scheduling2(course, timetable, gro_stu_dat, week, timeslots, classroom_info):
	day = random.choice(week)
	time = random.choice(timeslots)
	room = random.choice(list(classroom_info.keys()))
	if not bool(timetable[day][time][room]):
		timetable[day][time][room][course] = gro_stu_dat[course]
	else:
		scheduling(course, timetable, gro_stu_dat, week, timeslots, classroom_info)

# Picks random day-timeslot-classroom in the week-------------------------------
def make_random_timetable(random_timetable, student_database, week, timeslots, classroom_info):
	for subject in list(student_database.keys()):
		scheduling(subject, random_timetable, student_database, week, timeslots, classroom_info)
	return random_timetable

##---------------Evaluation functions ----------------------------------------##

# Checks if there are student that are scheduled double within the same timeslot
def duplicate_student(time_table):
	counter_minus = 0
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
					score += 20 ###dit moet dus 10 worden ipv 20
			else:
				compare = set(time_table_week) & set(ideal_week)
				if(len(compare) == course_activity_counter):
					score += 20 ###dit moet dus 10 worden ipv 20
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
				group_scores = [] ###delete
				###group_scores = 0
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
					group_scores.append(single_score) ###delete
					###group_scores = group_score + single_score
				course_score = min(group_scores) ###delete
				###course_score = group_score
			else:
				single_time_table_week = []
				for l in range(len(courses[course])):
					single_time_table_week.append(courses[course][l][:2])
				course_score = score_distr(single_time_table_week, course, course_info)
			score_total = score_total + course_score
	return score_total

# Returns total of points a timetable is worth----------------------------------
def time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week):
	points_double_sched = duplicate_student(time_table)
	points_classroom_capa = minus_classrooms(time_table)
	points_distr_week = bonus_distribution(time_table, all_subject_names, course_info)
	points_tot = 1000 + points_double_sched + points_classroom_capa + points_distr_week

	score_total.append(points_tot)
	score_double_students.append(points_double_sched)
	score_classrooms.append(points_classroom_capa)
	score_ditribution_in_week.append(points_distr_week)
	return

def time_table_points2(time_table):
	points_double_sched = duplicate_student(time_table)
	points_classroom_capa = minus_classrooms(time_table)
	points_distr_week = bonus_distribution(time_table, all_subject_names, course_info)
	points_tot = 1000 + points_double_sched + points_classroom_capa + points_distr_week
	return points_tot

##---------------Top time tables ---------------------------------------------##

# Keeps track of best time tables for further use-------------------------------
###deze functie wordt niet gebruikt dus kan weg...
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

##---------------Visualisation functions -------------------------------------##

# Writes a schedule to a readable format in excel-------------------------------
def excel_schedule(time_table, week, timeslots, classroom_info, best_score_sheetname, filename):
	print "writing to excel..."

	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet(best_score_sheetname)

	# creates empty time table
	day_col = 2
	timeslot_row = 1
	classroom_row = 1

	for day in week:
		worksheet.write(0, day_col, day)
		day_col += 1

	for timeslot in timeslots:
		worksheet.write(timeslot_row, 0, timeslot)
		timeslot_row += 7
		for classroom in (classroom_info):
			worksheet.write(classroom_row, 1, classroom)
			classroom_row += 1

	# Fills in time table

	# Counters for each day and timeslot to orden the dicts
	ma_row_9 = 1
	ma_row_11 = 8
	ma_row_13 = 15
	ma_row_15 = 22
	di_row_9 = 1
	di_row_11 = 8
	di_row_13 = 15
	di_row_15 = 22
	wo_row_9 = 1
	wo_row_11 = 8
	wo_row_13 = 15
	wo_row_15 = 22
	do_row_9 = 1
	do_row_11 = 8
	do_row_13 = 15
	do_row_15 = 22 
	vr_row_9 = 1
	vr_row_11 = 8
	vr_row_13 = 15
	vr_row_15 = 22

	# Fills the time table if classroom is filled
	for day in time_table.keys():
		for timeslot in time_table[day].keys():
			for classroom in time_table[day][timeslot].keys():
				if bool (time_table[day][timeslot][classroom]):
					course = str(time_table[day][timeslot][classroom].keys())
					if day is "maandag":
						if timeslot == '9.00-11.00':
							worksheet.write(ma_row_9,2, course)
							ma_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(ma_row_11,2, course)
							ma_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(ma_row_13,2, course)
							ma_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(ma_row_15,2, course)
							ma_row_15 += 1
					if day is "dinsdag":
						if timeslot == '9.00-11.00':
							worksheet.write(di_row_9,3, course)
							di_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(di_row_11,3, course)
							di_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(di_row_13,3, course)
							di_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(di_row_15,3, course)
							di_row_15 += 1
					if day is "woensdag":
						if timeslot == '9.00-11.00':
							worksheet.write(wo_row_9,4, course)
							wo_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(wo_row_11,4, course)
							wo_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(wo_row_13,4, course)
							wo_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(wo_row_15,4, course)
							wo_row_15 += 1
					if day is "donderdag":
						if timeslot == '9.00-11.00':
							worksheet.write(do_row_9,5, course)
							do_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(do_row_11,5, course)
							do_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(do_row_13,5, course)
							do_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(do_row_15,5, course)
							do_row_15 += 1				
					if day is "vrijdag":
						if timeslot == '9.00-11.00':
							worksheet.write(vr_row_9,6, course)
							vr_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(vr_row_11,6, course)
							vr_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(vr_row_13,6, course)
							vr_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(vr_row_15,6, course)
							vr_row_15 += 1

				# If classroom is empty fill in blank
				if not bool (time_table[day][timeslot][classroom]):
					course = " "
					if day is "maandag":
						if timeslot == '9.00-11.00':
							worksheet.write(ma_row_9,2, course)
							ma_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(ma_row_11,2, course)
							ma_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(ma_row_13,2, course)
							ma_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(ma_row_15,2, course)
							ma_row_15 += 1
					if day is "dinsdag":
						if timeslot == '9.00-11.00':
							worksheet.write(di_row_9,3, course)
							di_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(di_row_11,3, course)
							di_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(di_row_13,3, course)
							di_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(di_row_15,3, course)
							di_row_15 += 1
					if day is "woensdag":
						if timeslot == '9.00-11.00':
							worksheet.write(wo_row_9,4, course)
							wo_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(wo_row_11,4, course)
							wo_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(wo_row_13,4, course)
							wo_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(wo_row_15,4, course)
							wo_row_15 += 1
					if day is "donderdag":
						if timeslot == '9.00-11.00':
							worksheet.write(do_row_9,5,  course)
							do_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(do_row_11,5, course)
							do_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(do_row_13,5, course)
							do_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(do_row_15,5, course)
							do_row_15 += 1				
					if day is "vrijdag":
						if timeslot == '9.00-11.00':
							worksheet.write(vr_row_9,6, course)
							vr_row_9 += 1
						if timeslot == '11.00-13.00':
							worksheet.write(vr_row_11,6, course)
							vr_row_11 += 1
						if timeslot == '13.00-15.00':
							worksheet.write(vr_row_13,6, course)
							vr_row_13 += 1
						if timeslot == '15.00-17.00':
							worksheet.write(vr_row_15,6, course)
							vr_row_15 += 1
	workbook.close()

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
			check = unique_score(passed_scores, passed_scores[x])
			passed_scores[x] = check
		scores[passed_scores[x]] = copy.deepcopy(Ttable)
		Ttable.clear()
		if len(scores) < max_size:
			scores[min_value_0] = copy.deepcopy(min_value_1)
	else:
		scores[min_value_0] = copy.deepcopy(min_value_1)
	return scores

def take_best_scores2(score, passed_scores, table, x, abc):
	recent_score = passed_scores.pop(x)
	previous_best_score = sorted(passed_scores, reverse = True)[0]
	Ttable = {}
	if recent_score > previous_best_score:
		Ttable = copy.deepcopy(table)
		score = copy.deepcopy(Ttable)
		Ttable.clear()
	passed_scores.append(recent_score)
	return score

def acceptance_probability(temperature, i):
	#linear simulated annealing
#	temperature = float(temperature) - (float(1) / float(n_mutaties))
#	return temperature

	#exponential simulated annealing
	temperature = float(temperature) * pow(float(alpha), float(i))
	return temperature

def take_best_scores3(score, passed_scores, table, x, abc, temperature):
	recent_score = passed_scores.pop(x)
	previous_best_score = sorted(passed_scores, reverse = True)[0]
	Ttable = {}
	if recent_score > previous_best_score:
		Ttable = copy.deepcopy(table)
		score = copy.deepcopy(Ttable)
		Ttable.clear()
	elif temperature > random.random():
		Ttable = copy.deepcopy(table)
		score = copy.deepcopy(Ttable)
		Ttable.clear()
	passed_scores.append(recent_score)
	return score

#check if value is already in priority queue, if so, change value to prevent error
def unique_score(Score, value):
	if value in Score:
		value -= 1 ###deze waarde veranderen van 1 naar 0.1
		unique_score(Score, value)	
	return value

##-----------------Mutations on time table ------------------------------------##
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
		return subject_name

##-----------------functie voor genetic algotrithmen----------------------##
def take_two_diff_genes(all_genes):
	gen1 = random.choice(all_genes)
	gen2 = random.choice(all_genes)
	if gen1 == gen2:
		return take_two_diff_genes(all_genes)
	return(gen1,gen2)

def check_validity_time_table(table, gene_pool, parent1, parent2, group_student_database):
	count_unique_subjects = 0
	count_empty_spaces = 0
	count_double_subjects = 0
	count_all_options = 0
	check_all_subjects = copy.deepcopy(list(group_student_database.keys()))
	for day in table.keys():
		for timeslot in table[day].keys():
			for classroom in table[day][timeslot].keys():
				count_all_options+=1
				if not bool(table[day][timeslot][classroom]):
					count_empty_spaces += 1
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
###dit toevoegen voor n mutaties, mogelijk als voorwaarde aantal dubbele vakken mee te geven.
'''
		if count_double_subjects < mutations_condition_GA:
			for i in range(0,number_of_mutations_GA):
				random_subject = delete_random_subject(table)
				scheduling2(random_subject, table, group_student_database, days_in_week, time_frames, classroom_info)
'''
		return True
###	else:
###		return False

###Volgens mij wordt deze functie nergens gebruikt... Als dat zo is kan ie weg...
def mutation(ttable, week, timeslots , classroom_info):
	day = random.choice(week)
	time = random.choice(timeslots)
	room = random.choice(list(classroom_info.keys()))
	if not bool(timetable[day][time][room]):
		mutation(ttable, week, timeslots , classroom_info)
	else:
		subject = list(table[day][timeslot][classroom].keys())[0]
		timetable[day][time][room].pop(subject)

def recombine_genes(parent1, parent2, population_all_parents, genes, group_student_database):
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
	if not bool(check_validity_time_table(recombination_table, genes, parent1, parent2, group_student_database)):
		recombination_table.clear()
###	else: #ipv elif bool zoals hier onder staat
	elif bool(check_validity_time_table(recombination_table, genes, parent1, parent2, group_student_database)):
		points = time_table_points2(recombination_table)
		check_scores = list(population_all_parents.keys())
		if points in check_scores:
			points = unique_score(check_scores, points)
		population_all_parents[points] = recombination_table
		return True

def make_new_generation(old_generation_dict, group_student_database):
	gene_pool = list(old_generation_dict.keys())
	mean_value_genepool = mean_value(gene_pool)
	size_population_parents = len(list(old_generation_dict.keys()))
###	print('print grootte van populatie ouders',size_population_parents)
	print('Met een gemiddelde waarde van: ' + str(mean_value_genepool))
	while len(list(old_generation_dict.keys())) < (size_population_parents + population_size_per_generation):
		(gen1, gen2) = take_two_diff_genes(gene_pool)
		recombine_genes(gen1, gen2, old_generation_dict, gene_pool, group_student_database)

def select_new_population(population):
	old_population = copy.deepcopy(population)
	population.clear()
	population_scores = sorted(list(old_population.keys()), reverse = True)
###dit ipv het oude erin zetten svp. Zo ontstaat een selectie kans ipc beste overerving.
'''
	i = 0
	while len(list(population.keys())) < (selection_on_population):
		select = selection_function
		if select > random.random() :
			key = population_scores[i]
			population[key] = old_population[key]
		else:
#			print('denied')
			hallo = 0
		i+=1
'''	
###deze 3 regels mogen weg.	
	for i in range(0,selection_on_population):
		key = population_scores[i]
		population[key] = old_population[key]

def mean_value(list_values):
	size = len(list_values)
	total = 0
	mean = 0
	for i in range(0,size):
		total += list_values[i]
	mean = (float(total)/float(size))
	return mean