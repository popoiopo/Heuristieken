"""
ola! Dit is even een python scriptje om alle data
van alle studenten erin te krijgen.

Zo kunnen we van elke student weten in welke klassen die zit,
hoeveel mensen er in elke klas zitten etc.
"""

import csv
from fnmatch import fnmatch, fnmatchcase

rooster = open("studenten_roostering.csv")
csv_rooster = csv.reader(rooster)

data = [row for row in csv_rooster]
var_names = [name for name in data[0]]
people_var = [dict(zip(var_names, person)) for person in data]
people_person = [dict(zip(person, var_names)) for person in data]

for person in people_var:
	print person['Voornaam']
	print ""

for person in people_var:
	if person['Vak1'] in 'Webprogrammeren en databases':
		print person
		print ""

webpro_database = []
for person in people_person:
	if 'Webprogrammeren en databases' in person:
		webpro_database.append(person)

print webpro_database
print len(webpro_database)

rooster.close()