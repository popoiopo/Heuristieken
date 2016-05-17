"""
Heuristics:
Lectures & Lesroosters

Bas Chatel
10246215
Bram Sloots

Job Huisman

"""
##---------------Loading libraries -------------------------------------------##
import sys
sys.path.insert(0, 'functions_and_parameters')
from config import *
from functions_team_datanose import *

time_0 = time.time() #starting timer to keep track of execution duration 
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

##---------------As of now all timetables are random and valid ---------------##
#scores for random time tables
score_total = []
score_double_students = []
score_classrooms = []
score_ditribution_in_week = []
#scores for mutations Hillclimber
score_total_hillcl = {}
score_double_students_hillcl = {}
score_classrooms_hillcl = {}
score_ditribution_in_week_hillcl = {}

best_scores_random = {} #dict for best n timetables of randomly generated time tables
best_scores_hillcl = {} #dict to mutate best n time tables in hillclimber

best_scores_random = {-1001: 'lala'} #needed trash value to temporary fill dict

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
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_random_tests) + ' random roosters.')

print('De beste ' + str(best_scores_maxsize) + ' roosters zijn bewaard in een dict onder de volgende keys.')
print(best_scores_random.keys())
print('Om de Hillclimber te laten werken veranderen we deze keys in:')

keys = list(best_scores_random.keys())
for i in range(0,best_scores_maxsize):
	n = str(ascii_lowercase[i])
	key = keys[i]
	score_total_hillcl[n] = [key]
	score_double_students_hillcl[n] = [0]
	score_classrooms_hillcl[n] = [0]
	score_ditribution_in_week_hillcl[n] = [0]
	best_scores_hillcl[n] = best_scores_random.pop(key)
print(best_scores_hillcl.keys())
print('Om te weten wat de score is van deze roosters is houden we een list van scores bij\n in een list, opgeslagen in een apparte dict, onder de zelfde key als de roosters:')
print(score_total_hillcl)
print('Ook de subscores van score_double_students, score_classrooms en score_ditribution_in_week zijn zo opgeslagen.')

print('Nu gaan we een aantal mutaties proberen. De parameter n_mutaties geeft aan hoe vaak we dit doen.')
i = 1
while i < n_mutaties:
	for j in range(0,best_scores_maxsize):
		key = str(ascii_lowercase[j])
		table = copy.deepcopy(best_scores_hillcl[key])
		random_subject = delete_random_subject(table)
		scheduling2(random_subject, table, group_student_database, days_in_week, time_frames, classroom_info)
		time_table_points(table, score_total_hillcl[key], score_double_students_hillcl[key],score_classrooms_hillcl[key], score_ditribution_in_week_hillcl[key])
		best_scores_hillcl[key] = take_best_scores2(best_scores_hillcl[key], score_total_hillcl[key], table, i, key)
		if i % print_every_n_mutations == 0:
			if key == 'a':
				print('Dit is mutatie loop ' + str((i)))
				time_print = time.time()
				x = time_print - time_0
				print('Het duurt al ' + str(x) + ' seconden')
			best_score_print = sorted(score_total_hillcl[key], reverse = True)[0]
			print('beste score voor rooster ' + str(key) + ' is ' + str(best_score_print))
			if i == n_mutaties - 1:
				best_timetable_excel[best_score_print] = key
	i += 1

best_timetable_write = best_scores_hillcl[best_timetable_excel[max(best_timetable_excel)]]
best_score_sheetname = str(max(best_timetable_excel))
print "Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!"
print "Deze kan je in de map vinden onder: best_hill_climb.xlsx"
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_hill_climb.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) + ' seconden voor het hele programma.')
student_scheduling.close()