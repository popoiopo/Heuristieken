
vak_info	 	= [dict(zip(header_vakken, check)) for check in data_vakken]



def aantalcollegesinweek(vakinfo, vak):
	for info in vakinfo:
		if info["vakken"] == vak:
			hc = float(info["hoorcolleges"])
			wc = float(info["werkcolleges"])
			pr = float(info["practica"])
			total = int(hc + wc + pr)
			#return {'hc': hc, 'wc': wc, 'pr': pr, 'tot':total}
			return (total)

def bonusdageninweek(aantalx):
	if aantalx == 4:
		return ['ma', 'di', 'do', 'vr']
	if aantalx == 3:
		return ['ma', 'wo', 'vr']
	if aantalx == 2:
		return [['ma', 'do'], ['di', 'vr']]
	else:
		return ['ma', 'di', 'wo', 'do', 'vr']

def score_distr(weekrooster, vak):
	score = 0
	aantal_contacturen = aantalcollegesinweek(vak_info, vak)
	dagen_in_weekr = len(set(weekrooster))
	if(aantal_contacturen > 1):
		geen_minpunten = 0
		if (dagen_in_weekr == (aantal_contacturen - 1)):
			score -= 10
			geen_minpunten += 1
		if(dagen_in_weekr == (aantal_contacturen - 2)):
			score -= 20
			geen_minpunten += 1
		if(dagen_in_weekr == (aantal_contacturen - 3)):
			score -= 30
			geen_minpunten += 1
		if(geen_minpunten == 0):
			ideale_weekr = bonusdageninweek(aantal_contacturen)
			print("ideaal: ", ideale_weekr)
			check = 0
			if (aantal_contacturen == 2):
				for i in range(0, 2):
					compare = set(weekrooster) & set(ideale_weekr[i])
					if(len(compare) == aantal_contacturen):
						check += 1
				if(check > 0):
					score += 20
			else:
				compare = set(weekrooster) & set(ideale_weekr)
				if(len(compare) == aantal_contacturen):
					score += 20
	return(score)

for subject in list(group_student_database.keys()):
	roosteren(subject, rooster, group_student_database)

# bouw dict met alle vaknamen
def rooster_dagen_vd_week():
	vak_dict = {}
	for i in range(len(all_subject_names)):
		vak_dict[all_subject_names[i]] = []
	# bouw per vak het aantal events in een list, dus: wo0, ma2, ma1, ma0 etc.
	vakken = []
	for dag in rooster.keys():
		for tijd in rooster[dag].keys():
			for lokaal in rooster[dag][tijd].keys():
				for vak in rooster[dag][tijd][lokaal].keys():
					vakken.append(vak)
					vaknaam_1 = vak[7:]

					if(vak[0] == "h"):
						event = dag[:2] + str(0)
						vak_dict[vaknaam_1].append(event)
					else:
						event = dag[:2] + vak[5]
						vak_dict[vaknaam_1].append(event)
	return vak_dict

# geef totaal min en plus per vak aan totaalscore
def eva_minplus_dagenweek():
	totaalscore = 0
	vakken = rooster_dagen_vd_week()
	for vak in vakken:
		print("\n\n", vakken[vak])
		buffer1 = []
		# append iedere groep en bepaal max waarde
		for i in range(0, len(vakken[vak])):
			buffer1.append(int(vakken[vak][i][2]))
		groepen = max(buffer1)
		print("groepen: ", groepen)
		aantal_contacturen = aantalcollegesinweek(vak_info, vak)
		print("contacturen: ", aantal_contacturen)


		# per groep in weekroosters multi
		score_vak = 0
		if(aantal_contacturen > 1):
			if(groepen > 0):
				group_scores = []
			# maak weekrooster voor iedere groep
				for j in range(1,(groepen + 1)):
					weekrooster_enkel = []
					# rooster voor 1 groep
					for k in range(len(vakken[vak])):
						if(vakken[vak][k][2] == "0"):
							weekrooster_enkel.append(vakken[vak][k][:2])
						check = int(vakken[vak][k][2])
						if(check == j):
							weekrooster_enkel.append(vakken[vak][k][:2])
					#score subgroep
					enkel_score = score_distr(weekrooster_enkel, vak)
					group_scores.append(enkel_score)
					print (weekrooster_enkel)
					print (enkel_score)
				score_vak = min(group_scores)
				print ("score_vak: ", score_vak)
				
			else:
				weekrooster_enkel = []
				for l in range(len(vakken[vak])):
					weekrooster_enkel.append(vakken[vak][l][:2])
				print(weekrooster_enkel)
				score_vak = score_distr(weekrooster_enkel, vak)
				print ("score_vak: ", score_vak)
			totaalscore = totaalscore + score_vak
			print("vaktussenstand: ", totaalscore)
	print ("totaal: ", totaalscore)
	return totaalscore