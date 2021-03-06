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

#create n_random timetables, and savethem in dict
for i in range(0,(n_random_gen+1)):
	time_table = empty_timetable(days_in_week, time_frames, classroom_info)
	time_table = make_random_timetable(time_table, group_student_database, 
				days_in_week, time_frames, classroom_info)
	time_table_points(time_table, score_total, score_double_students, 
				score_classrooms, score_ditribution_in_week)
	best_scores_gen = take_best_scores(best_scores_gen, score_total, time_table, i, (n_random_gen))
	time_table.clear()

time_2 = time.time()
x = time_2-time_0
print('Het duurt ' + str(x) + ' seconden voor het genereren van ' + str(n_random_gen) + ' random roosters.')
print('De beste ' + str((n_random_gen)) + ' roosters zijn bewaard in een dict onder de volgende keys.')
print(best_scores_gen.keys())
#store beginpopulation
score_total_gen = {}
keys = sorted(list(best_scores_gen.keys()), reverse = True)
for i in range(0,n_random_gen):
	n = ascii_lowercase[i]
	key = keys[i]
	score_total_gen[n] = [key]

I = 1
while I < (n_generations + 1):
	make_new_generation(best_scores_gen, group_student_database)
	select_new_population(best_scores_gen)
	#store generation progression, to write to file later
	scores_generation = sorted(list(best_scores_gen.keys()), reverse = True)
	for i in range(0,len(scores_generation)):
		n = str(ascii_lowercase[i])
		key = scores_generation[i]
		score_total_gen[n].append(key)

	if I % print_every_n_mutations_genal == 0:
		print('Generation ' + str(I))
		print(scores_generation)
	I += 1


scores_generation = sorted(list(best_scores_gen.keys()), reverse = True) ###dit is gesorteerd zo :P
print ("Last generation ") 
print (scores_generation)
best_score = max(scores_generation)

best_timetable_write = best_scores_gen[best_score]
best_score_sheetname = str(best_score)
print ("Ons uiteindelijke beste score is " + best_score_sheetname + " punten waard!")
print ("Deze kan je in de map vinden onder: best_gen_alg.xlsx")
excel_schedule(best_timetable_write, days_in_week, time_frames, classroom_info, best_score_sheetname, "best_gen_alg.xlsx")
print("Analyse kan je in de map vinden onder: analyse_gen_alg.xlsx")
write_analyse(score_total_gen, n_generations, n_random_gen, 1, parameter_workgroupsizes, "analyse_gen_alg.xlsx")

time_n = time.time()
x = time_n - time_0
print('Het duurt ' + str(x) +' seconden voor het hele programma.')
student_scheduling.close()



