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
best_scores_random = {} #dict for best n timetables of randomly generated time tables
best_scores_random = {-1001: 'lala'} #needed trash value to temporary fill dict

for i in range(0,n_mutaties):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	best_scores_random = take_best_scores(best_scores_random, score_total, time_table, i, best_scores_maxsize)
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_mutaties - 1) + ' random roosters.')

best_timetable_write = best_scores_random[max(best_scores_random.keys())]
best_score_sheetname = str(max(best_scores_random.keys()))
print "Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!"
print "Deze kan je in de map vinden onder: best_random.xlsx"
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_random.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) + ' seconden voor het hele programma.')
student_scheduling.close()