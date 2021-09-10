#Importing modules

from os import closerange
import numpy as np
import matplotlib.pyplot as plt
import csv

#Defining plot params
fnt = 20
wht = 'bold'

#Define 2D data array
data_arr = []

#Loading data
with open('cleaned_data.csv','r') as data:
    reader = csv.reader(data)
    fields = next(reader)#Skip the first row with column names
    for row in reader:
        data_arr.append(row)

#Tidy fields to be used for analysis
unwanted_characters = "-19"
for i in range(0,len(data_arr)-1):
    for character in unwanted_characters:
        data_arr[i][1] = data_arr[i][1].replace(character,"")#Removes year from month field

#Analysis 1 - Normalised (non-bias) volume of sales across the year
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

month_vol = {}

for month in months:
    month_vol[month] = int(sum(data_arr[i][1] == month for i in range(0, len(data_arr)-1)))*100/500

#Calculate the average monthly volume without sales promotions
no_sale = []
for key in month_vol.keys():
    if key == 'Apr' or key == 'May' or key == 'Aug':
        continue
    else:
        no_sale.append(month_vol[key])

avg_no_sale = np.mean(no_sale)
avg_no_sale_vol = {}

for month in months:
    avg_no_sale_vol[month] = int(avg_no_sale)

#Plot the analysis
fig = plt.figure(figsize=(10,8))
barchart = plt.bar(month_vol.keys(), month_vol.values(), color='blue', edgecolor = 'black', label = 'No promotions months')
plt.bar(0,0, color = 'g', label = 'Promotion months')#Highlight sales promotion months
barchart[3].set_facecolor('g') 
barchart[4].set_facecolor('g')
barchart[7].set_facecolor('g')
plt.plot(avg_no_sale_vol.keys(), avg_no_sale_vol.values(), linestyle = '--', color='red', label = 'Average no promotions volume')
plt.xlabel('Month', fontsize = fnt, fontweight = wht)
plt.ylabel('Normalised Volume of Sales [%]', fontsize = fnt, fontweight = wht)

handles, labels = plt.gca().get_legend_handles_labels()#Force legend order to be logical
order = [1,2,0]
plt.legend([handles[i] for i in order], [labels[i] for i in order], loc = 'best', fontsize = 14)

plt.show()


