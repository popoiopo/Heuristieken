import csv

rooster = open("studenten_roostering.csv")
csv_rooster = csv.reader(rooster)

data = []
for row in csv_rooster:
	data.append(row)

d = {data[0][0]:data[1][0]}
print d


print data[3][0]

rooster.close()