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

size = 500
month_vol = []

for month in months:
    month_vol.append(sum(data_arr[i][1] == month for i in range(0, len(data_arr)-1)))

#explode1 = (0,0,0,0.1,0.1,0,0,0.1,0,0,0,0)
#fig1, ax1 = plt.subplots()
#ax1.pie(np.array(month_vol)*100/500, explode=explode1, labels = months, autopct = '%.1f%%', shadow = True)
#ax1.axis('equal')#Ensure a circle is formed
#plt.show()

#Calculate the average monthly volume without sales promotions
non_sales_months = []
for month in range(0,len(months)-1):
    if months[month] == 'Apr' or 'May' or 'Aug':
        continue
    else:
        non_sales_months.append(month_vol[month])
        print(month_vol[month])
#avg_month = sum(non_sales_months)/len(non_sales_months)

#print(non_sales_months)

xpos1 = [i for i, _ in enumerate(months)]

fig = plt.figure(figsize=(10,8))
plt.bar(xpos1, np.array(month_vol)*100/500, color='blue')
#plt.plot(xpos1,avg_month)
plt.xlabel('Month', fontsize = fnt, fontweight = wht)
plt.ylabel('Normalised Volume of Sales [%]', fontsize = fnt, fontweight = wht)
plt.xticks(xpos1, months, fontsize = 12)
plt.show()


