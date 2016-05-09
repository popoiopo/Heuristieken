#------Job en zijn plotje-------#  
def plot_population(list_scores, name):
	sorted_score = sorted(list_scores)
	fit = stats.norm.pdf(list_scores, np.mean(list_scores), np.std(list_scores))
	minvalue = "min: " + str(min(list_scores))
	maxvalue = "    max: " + str(max(list_scores))
	standdev1 = np.std(list_scores)
	standdev2 = (math.ceil(standdev1*100)/100)
	standdev = "    SD: " + str(standdev2)
	meanvalue = "    mean: " + str(np.mean(list_scores))
	title = name + "  " + minvalue + maxvalue + standdev + meanvalue
	pl.plot(list_scores,fit,'o')
	pl.hist(list_scores,normed=True)
	pl.xlabel('Points')
	pl.ylabel('Frequency(Hz)')
	pl.title(title)
	
	pl.show()


plot_population(score_total, "score_total")
plot_population(score_double_students, "score_double_students")
plot_population(score_classrooms, "score_classrooms")
plot_population(score_distribution_in_week, "score_distribution_in_week")