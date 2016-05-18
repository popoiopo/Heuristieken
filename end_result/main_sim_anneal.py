"""
Heuristics:
Lectures & Lesroosters

Bas Chatel
10246215
Bram Sloots
10017887
Job Huisman

"""
##---------------Loading libraries -------------------------------------------##
import sys
sys.path.insert(0, 'functions_and_parameters')
from config import *
from functions_team_datanose import *

time_0 = time.time() #starting timer to keep track of execution duration 

##---------------As of now all timetables are random and valid ---------------##
for i in range(0,n_random_simann):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	random_simann = take_best_scores(random_simann, score_total, time_table, i, simann_maxsize)
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_random_simann) + ' random roosters.')

print('De beste ' + str(simann_maxsize) + ' roosters zijn bewaard in een dict onder de volgende keys.')
print(random_simann.keys())
print('Om de Hillclimber te laten werken veranderen we deze keys in:')

keys = list(random_simann.keys())
print keys
for i in range(0,simann_maxsize):
	n = str(ascii_lowercase[i])
	key = keys[i]
	score_total_simann[n] = [key]
	score_double_students_simann[n] = [0]
	score_classrooms_simann[n] = [0]
	score_ditribution_in_week_simann[n] = [0]
	best_scores_simann[n] = random_simann.pop(key)
print(best_scores_simann.keys())
print('Om te weten wat de score is van deze roosters is houden we een list van scores bij\n in een list, opgeslagen in een apparte dict, onder de zelfde key als de roosters:')
print(score_total_simann)
print('Ook de subscores van score_double_students, score_classrooms en score_ditribution_in_week zijn zo opgeslagen.')

print('Nu gaan we een aantal mutaties proberen. De parameter n_mutations_simann geeft aan hoe vaak we dit doen.')
i = 1
while i < n_mutations_simann:
	for j in range(0,simann_maxsize):
		key = str(ascii_lowercase[j])
		table = copy.deepcopy(best_scores_simann[key])
		random_subject = delete_random_subject(table)
		scheduling2(random_subject, table, group_student_database, days_in_week, time_frames, classroom_info)
		time_table_points(table, score_total_simann[key], score_double_students_simann[key],score_classrooms_simann[key], score_ditribution_in_week_simann[key])
		temperature = acceptance_probability(temperature, i)
		best_scores_simann[key] = take_best_scores3(best_scores_simann[key], score_total_simann[key], table, i, key, temperature) 
		if i % print_every_n_mutations_simann == 0:
			if key == 'a':
				print('Dit is mutatie loop ' + str((i)))
				time_print = time.time()
				x = time_print - time_0
				print('Het duurt al ' + str(x) + ' seconden')
			best_score_print = sorted(score_total_simann[key], reverse = True)[0]
			print('beste score voor rooster ' + str(key) + ' is ' + str(best_score_print))
		if i == n_mutations_simann - 1:
			best_timetable_excel[best_score_print] = key
	i += 1
	
print best_timetable_excel
best_timetable_write = best_scores_simann[best_timetable_excel[max(best_timetable_excel)]]
best_score_sheetname = str(max(best_timetable_excel))
print ("Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!")
print ("Deze kan je in de map vinden onder: best_sim_anneal.xlsx")
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_sim_anneal.xlsx")
write_analyse(score_total_simann, n_mutations_simann, simann_maxsize, 1, parameter_workgroupsizes, "analyse_sim_anneal.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) + ' seconden voor het hele programma.')
student_scheduling.close()