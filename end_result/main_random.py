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
for i in range(0,(n_random_test+1)):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	best_scores_random = take_best_scores(best_scores_random, score_total, time_table, i, best_scores_maxsize_random)
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_random_test) + ' random roosters.')

best_timetable_write = best_scores_random[max(best_scores_random.keys())]
best_score_sheetname = str(max(best_scores_random.keys()))
print ("Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!")
print ("Deze kan je in de map vinden onder: best_random.xlsx")
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_random.xlsx")
print ("Analyse kan je in de map vinden onder: analyse_random.xlsx")
rand_roosters_analyse(score_total, best_scores_random, n_random_test, best_scores_maxsize_random, "Random","analyse_random.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) + ' seconden voor het hele programma.')
student_scheduling.close()

