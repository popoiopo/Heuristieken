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
#create n_random_tests timetables, and save the best best_scores_maxsize 
for i in range(0,n_random_tests_gen):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	best_scores_random = take_best_scores(best_scores_random, score_total, time_table, i, best_scores_maxsize)
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_random_tests_gen) + ' random roosters.')
print('De beste ' + str(best_scores_maxsize) + ' roosters zijn bewaard in een dict onder de volgende keys.')
print(best_scores_random.keys())

#Loop over generations
I = 1
while I < (n_generations + 1):
	print('Generation ' + str(I))
	scores_generation = list(best_scores_random.keys())
	print(sorted(scores_generation, reverse = True))
	make_new_generation(best_scores_random, group_student_database)
	select_new_population(best_scores_random)
	I += 1
	if i == n_generations:
		best_score = max(scores_generation)

best_timetable_write = best_scores_random[best_score]
best_score_sheetname = str(best_score)
print ("Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!")
print ("Deze kan je in de map vinden onder: best_gen_alg.xlsx")
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_gen_alg.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) +' seconden voor het hele programma.')

student_scheduling.close()



