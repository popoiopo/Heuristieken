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

##---------------As of now all timetables are random and valid ---------------##
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
print keys
for i in range(0,best_scores_maxsize):
	n = str(ascii_lowercase[i])
	key = keys[i]
	score_total_hillcl[n] = [key]
	score_double_students_hillcl[n] = [0]
	score_classrooms_hillcl[n] = [0]
	score_ditribution_in_week_hillcl[n] = [0]
	best_scores_sim_anneal[n] = best_scores_random.pop(key)
print(best_scores_sim_anneal.keys())
print('Om te weten wat de score is van deze roosters is houden we een list van scores bij\n in een list, opgeslagen in een apparte dict, onder de zelfde key als de roosters:')
print(score_total_hillcl)
print('Ook de subscores van score_double_students, score_classrooms en score_ditribution_in_week zijn zo opgeslagen.')

print('Nu gaan we een aantal mutaties proberen. De parameter n_mutaties geeft aan hoe vaak we dit doen.')
i = 1
while i < n_mutaties:
	for j in range(0,best_scores_maxsize):
		key = str(ascii_lowercase[j])
		table = copy.deepcopy(best_scores_sim_anneal[key])
		random_subject = delete_random_subject(table)
		scheduling2(random_subject, table, group_student_database, days_in_week, time_frames, classroom_info)
		time_table_points(table, score_total_hillcl[key], score_double_students_hillcl[key],score_classrooms_hillcl[key], score_ditribution_in_week_hillcl[key])
		temperature = acceptance_probability(temperature, i)
		best_scores_sim_anneal[key] = take_best_scores3(best_scores_sim_anneal[key], score_total_hillcl[key], table, i, key, temperature) 
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

best_timetable_write = best_scores_sim_anneal[best_timetable_excel[max(best_timetable_excel)]]
best_score_sheetname = str(max(best_timetable_excel))
print "Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!"
print "Deze kan je in de map vinden onder: best_sim_anneal.xlsx"
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_sim_anneal.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) + ' seconden voor het hele programma.')
student_scheduling.close()