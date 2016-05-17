"""
This is our config file, where all global parameters will be set.

"""
##---------------Loading libraries -------------------------------------------##
import csv

##---------------Parameter values --------------------------------------------##
# Decides the ratio of emptyness/fullnes of the classrooms
parameter_workgroupsizes = 0.21 #0.41 and 0.61 are also interesting values
best_scores_maxsize = 10 #remembers n best random time tables
n_random_tests = 10 #generates n random time table of which the best (n=best_scores_maxsize) will be remembered
n_mutaties = 201 #will do n mutations and remembers when new time table has a better score
print_every_n_mutations = 100 #prints out all max values after n mutations

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

##---------------Simulated annealing parameters --------------------------------##

temperature = float(1.0)
e = float(2.71828)
alpha = float(1) - (float(1) / float(n_mutaties))

##---------------Empty dict to find best time table ----------------------------##

best_timetable_excel = {}
