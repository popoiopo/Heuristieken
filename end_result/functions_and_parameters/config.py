"""
This is our config file, where all global parameters will be set.

"""
##---------------Loading libraries -------------------------------------------##
import csv
import math

##----------------General Parameters and lists--------------------------------##
best_timetable_excel = {}
score_total = []
score_double_students = []
score_classrooms = []
score_ditribution_in_week = []
# Decides the ratio of emptyness/fullnes of the classrooms
parameter_workgroupsizes = 0.21 #0.41 and 0.61 are also interesting values

##-------------Parameters Random-------------------------##
n_random_tests = 5000 #generates n random time table of which the best (n=best_scores_maxsize) will be remembered
best_scores_maxsize_random = 10 #remembers n best random time tables
#scores for random timetables
best_scores_random = {-100001: 'lala'} #dict for best n timetables of randomly generated time tables
'''
##-------------Parameters HillCl-------------------------##
n_random_hillcl = 27 #number of random tables, takes hillcl_maxsize bests to develop
hillcl_maxsize = 26 #maximum of best tables to develop !!can't be bigger then 26!!
n_mutations_hillcl = 5000 #number of mutations per table
print_every_n_mutations_hillcl = 1000 #prints out all max values after n mutations
#scores for mutations Hillclimber
random_hillcl = {-100001: 'lala'} #dict of best random generated tables voor hillclimber
best_scores_hillcl = {} #dict to mutate best n time tables in hillclimber
score_total_hillcl = {}
score_double_students_hillcl = {}
score_classrooms_hillcl = {}
score_ditribution_in_week_hillcl = {}

##-------------Parameters SimAnnealing-------------------##
n_random_simann = 27
simann_maxsize = 26
n_mutations_simann = 5000
print_every_n_mutations_simann = 1000
temperature = float(1.0)
e = float(2.71828)
alpha = float(1) - (float(1) / float(n_mutations_simann))
#scores for mutations SimulatedAnnealing
random_simann = {-100001: 'lala'} #dict of best random generated tables voor SimulatedAnnealing
best_scores_simann = {} #dict to mutate best n time tables in SimulatedAnnealing
score_total_simann = {}
score_double_students_simann = {}
score_classrooms_simann = {}
score_ditribution_in_week_simann = {}

##-------------Parameters GenAl--------------------------##
n_random_gen = 41 #generates n-1 amount of random timetables for first parent population
n_generations = 10 #creates n generations
population_size_per_generation = int(3*n_random_gen) #lets population grow until this size before selection is applied
selection_on_population = int(1*n_random_gen) #growth of population, 1 is constant parent population per generation
mutations_condition_GA = 10 #make mutations when n subjects are missing
number_of_mutations_GA = 3 #number of mutations
#scores for mutations Hillclimber
max_faults_in_recombination = 120 #maximum recombination faults is n recombined table
best_scores_gen = {-100001: 'lala'} #dict of best tables per generation, initial value to compare tables
'''
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
				# Loop over all work group and make groups of average size
				for j in range(1,wc_number+1): 
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
				for j in range(1,pr_number+1): 
					course_name = "pr_" + str(i) + "_" + str(j) + "_" + subject
					group_student_database[course_name] = subject_student_database[subject][x:x+check]
					x += check