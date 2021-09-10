#Importing modules

from os import closerange
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import csv

#Defining plot params
fnt = 20
wht = 'bold'
 #Colour blind friendly paltte: dark blue, light blue, cyan, teal, green, orange, light yellow, dark yellow, red, wine, magenta, purple
colours = ['#332288','#0077BB','#33BBEE','#009988','#117733','#EE7733','#EECC66','#997700','#CC3311','#882255','#EE3377','#AA4499']

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

#Analysis 1 - Normalised volume of sales across the year - Did the sales months show an increase in volume? How effective were the sales months?
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
fig1 = plt.figure(figsize=(10,8))
barchart = plt.bar(month_vol.keys(), month_vol.values(), color=colours[0], edgecolor = 'black', label = 'No promotions months')
plt.bar(0,0, color = colours[4], label = 'Promotion months')#Highlight sales promotion months
barchart[3].set_facecolor('g') 
barchart[4].set_facecolor('g')
barchart[7].set_facecolor('g')
plt.plot(avg_no_sale_vol.keys(), avg_no_sale_vol.values(), linestyle = '--',  linewidth = 2, color=colours[8], label = 'Average no promotions volume')

plt.title('2019 Monthly Sales Volume', fontsize = 24)
plt.xlabel('Month', fontsize = fnt, fontweight = wht)
plt.ylabel('Normalised Volume [%]', fontsize = fnt, fontweight = wht)

#Set fontsize for axis tickers
for item in (plt.gca().get_xticklabels() + plt.gca().get_yticklabels()):
    item.set_fontsize(14)

handles, labels = plt.gca().get_legend_handles_labels()#Force legend order to be logical
order = [1,2,0]
plt.legend([handles[i] for i in order], [labels[i] for i in order], loc = 'best', fontsize = 14)

plt.savefig('monthly_sales_volume.png')#Save figure
plt.show()

#------------------------------

#Analysis 2 - Normalised volume of sales per region. Which regions contribute the most to sales?
regions = ['SC','NE','NW','YH','WL','WM','EM','EE','GL','SW','SE']

regions_full = ['Scotland','North East','North West','Yorkshire & Humber','Wales','West Midlands','East Midlands','East of England','London','South West','South East']

reg_vol = {}

for j in range(0,len(regions)):
    reg_vol[regions_full[j]] = int(sum(data_arr[i][6] == regions[j] for i in range(0, len(data_arr)-1)))*100/500

#Sort regions by size for logical pie chart formatting
reg_vol_sort = sorted(reg_vol.items(), key=lambda x: x[1], reverse=True)#Sorted list of regions from smallest to largest
reg_vol_val = {}
for i in range(0, len(reg_vol_sort)):
    reg_vol_val[reg_vol_sort[i][0]] = reg_vol_sort[i][1]#Get values from sorted list

explode = (0.1,0.1,0.1,0,0,0,0,0,0,0,0)

#Plot the analysis
fig2 = plt.figure(figsize=(10,8))
plt.pie(reg_vol_val.values(), labels=reg_vol_val.keys(), explode = explode, autopct='%.1f%%', shadow=True, startangle=90, radius = 2, labeldistance=1.05, frame=True)
plt.axis('equal')
plt.title('2019 Regional Sales Volume', fontsize = 24)
plt.tick_params(axis = 'both', bottom=False, left=False, labelbottom=False, labelleft = False)
matplotlib.rcParams['patch.linewidth'] = 0
matplotlib.rcParams['patch.edgecolor'] = 'black'
plt.savefig('regional_sales_volume.png')#Save figure
plt.show()

