import csv

#Define 2D data array
population_data = []

#Loading data
with open('region_population.csv','r') as data:
    reader = csv.reader(data)
    fields = next(reader)#Skip the first row with column names
    for row in reader:
        population_data.append(row)

region = []
population = []

for i in range(0, len(population_data)):
    if population_data[i][1] == 'Region':
        region.append(population_data[i][0])
        population.append(population_data[i][-1])
    else:
        continue

table = zip(region, population)

print('Region population')
for i, j in table:
    print(i,j, '\n')


