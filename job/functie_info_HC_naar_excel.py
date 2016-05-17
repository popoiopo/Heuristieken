# funtion writing information about hillclimber run:
# maxima of all hillclimbers
# history of the hillclimber with highest peak
# dict with hillclimber info per iteration, only improvements
# averiselist, info per iteration of average improvement, when improving, so average from risedict iterations
# all steps of multiple hillclimbers, incl. info of iterations with lower outcome

# input:
#
# archive: history per hillclimber in dict of lists
# eva_rounds: x iterations/steps
# n_population: amount of hillclimbers to analyse
# mut_per_eva: mutations per iteration/step (parameter)
# para_WG_size: parameter with size of student group size


def write_analyse(archive, eva_rounds, n_population, mut_per_eva, para_WG_size):

	#print("archive")
	#print(archive)

	max_list = []
	# get max values out of multiple HillClimbers
	for letters in archive:
		max_score = max(archive[letters])
		max_list.append(max_score)

	#print("maxima:")
	#print(max_list)

	# write list incl max values of all started random rosters
	score_best_try = max(max_list)

	# get history of best HillClimber
	history_best = []

	for each in archive:
		if score_best_try in archive[each]:
			history_best = archive[each]

	#print("history maximum:")
	#print(history_best)

	# only get values if value is greater, else value is the same as previous
	risedict = {}

	for each in archive:
		riselist = []
		for i in range(0, len(archive[each])):
			valbuf = archive[each][i]
			#print(valbuf)
			if(len(riselist) < 1):
				riselist.append(valbuf)
			#	print("eerste:")
			#	print(riselist)

			elif(valbuf > riselist[i-1]):
				riselist.append(valbuf)
			#	print("groter:")
			#	print(riselist)
			else:
				riselist.append(riselist[i-1])
			#	print("lager")
			#	print(riselist)
			#print(riselist)
		risedict[each] = riselist
	#print("Hier de risedict:")
	#print(risedict)

	averiselist = []

	# get average value of riselists in risedicts multiple hillclimbers
	for i in range(0, len(risedict['a'])):
		sum_mut_round = 0
		for each in risedict:
			buf_mut_round = 0
			buf_mut_round = risedict[each][i]
			sum_mut_round += buf_mut_round

			#print("score:")
			#print(risedict[each][i])
			#print("erbij optellen geeft:")
			#print(sum_mut_round)
		#print("gemiddelde voor ronde:")
		ave_mut_round = sum_mut_round/n_population
		#print(ave_mut_round)
		averiselist.append(ave_mut_round)
		#print("totaallijst")
		#print(averiselist)

	#print(averiselist)


	print(max_list)
	print(history_best)
	print(risedict)
	print(averiselist)
	print(archive)

	# write average per round, maxuitkomsten, history naar excell
	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook('analyse_hillcl.xlsx')
	worksheet = workbook.add_worksheet()

	# creates empty time table
	col = 0
	row = 0
	
	worksheet.write(row, col, "Hillclimber")
	worksheet.write(row+1, col, "Size_pop")
	worksheet.write(row+2, col, "Eva_rounds")
	worksheet.write(row+3, col, "Mutations per step")
	worksheet.write(row+4, col, "WG_size")

	worksheet.write(row+1, col+1, n_population)
	worksheet.write(row+2, col+1, eva_rounds)
	worksheet.write(row+3, col+1, mut_per_eva)
	worksheet.write(row+4, col+1, para_WG_size)

	row += 6

	worksheet.write(row, col, "maxima")
	row += 1

	for i in range(0,len(max_list)):
		buffer_it = max_list[i]
		worksheet.write(row, col, buffer_it)
		col += 1

	col = 0
	row += 1	
	worksheet.write(row, col, "best_history")
	row += 1

	for i in range(0, len(history_best)):
		buffer_it = int(history_best[i])
		worksheet.write(row, col, buffer_it)
		col += 1

	col = 0
	row += 1	
	worksheet.write(row, col, "risedict")
	row += 1

	for each in risedict:
		col = 0
		worksheet.write(row, col, each)
		row += 1
		for i in range(0, len(risedict[each])):
			buffer_it = risedict[each][i]
			worksheet.write(row, col, buffer_it)
			col += 1
		row += 1

	col = 0
	row += 1	
	worksheet.write(row, col, "averiselist")
	row += 1

	for i in range(0, len(averiselist)):
		buffer_it = averiselist[i]
		worksheet.write(row, col, buffer_it)
		col += 1

	col = 0
	row += 1	
	worksheet.write(row, col, "history_population")
	row += 1

	for each in archive:
		col = 0
		worksheet.write(row, col, each)
		row += 1
		for i in range(0, len(archive[each])):
			buffer_it = archive[each][i]
			worksheet.write(row, col, buffer_it)
			col += 1
		row += 1

		
	
	

#functie uitvoeren
write_analyse(score_total_hillcl, n_mutaties, best_scores_maxsize, n_changes_in_mutation, parameter_workgroupsizes)