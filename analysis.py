#Importing modules

import numpy as np
import matplotlib.pyplot as plt
import csv
import random

#Defining plot params
fnt = 20
wht = 'bold'
 #Colour blind friendly paltte: dark blue, light blue, cyan, teal, green, orange, light yellow, dark yellow, red, wine, magenta, purple
colours = ['#004488','#0077BB','#33BBEE','#009988','#117733','#EE7733','#EECC66','#997700','#CC3311','#882255','#EE3377','#AA4499']

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
for i in range(0,len(data_arr)):
    for character in unwanted_characters:
        data_arr[i][1] = data_arr[i][1].replace(character,"")#Removes year from month field


#Analysis 1 - Normalised volume of sales across the year - Did the sales months show an increase in volume? How effective were the sales months?
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

month_vol = {}

for month in months:
    month_vol[month] = int(sum(data_arr[i][1] == month for i in range(0, len(data_arr))))*100/500

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
    avg_no_sale_vol[month] = float(avg_no_sale)

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
plt.ylabel('Normalised volume [%]', fontsize = fnt, fontweight = wht)

#Set fontsize for axis tickers
for item in (plt.gca().get_xticklabels() + plt.gca().get_yticklabels()):
    item.set_fontsize(14)

handles, labels = plt.gca().get_legend_handles_labels()#Force legend order to be logical
order = [1,2,0]
plt.legend([handles[i] for i in order], [labels[i] for i in order], loc = 'best', fontsize = 14)

plt.savefig('monthly_sales_volume.png')#Save figure
#plt.show()
plt.close()

#csv output file for difference between averages

delta_vol = {}

for month in months:
    delta_vol[month] = float(month_vol[month] - avg_no_sale)

with open('delta_vol.csv', 'w') as delta:
    w = csv.writer(delta, delimiter = ',')
    w.writerow(['Month', 'Difference from average'])
    for key in delta_vol:
        row = [key] + [delta_vol[key]]
        w.writerow(row)


#Analysis 2 - Normalised volume of sales per region. Which regions contribute the most to sales?
regions = ['SC','NE','NW','YH','WL','WM','EM','EE','GL','SW','SE']

regions_full = ['Scotland','North East','North West','Yorkshire & Humber','Wales','West Midlands','East Midlands','East of England','London','South West','South East']

reg_vol = {}

for j in range(0,len(regions)):
    reg_vol[regions_full[j]] = int(sum(data_arr[i][6] == regions[j] for i in range(0, len(data_arr))))*100/500

#Sort regions by size for logical pie chart formatting
reg_vol_sort = sorted(reg_vol.items(), key=lambda x: x[1], reverse=True)#Sorted list of regions from smallest to largest
reg_vol_val = {}
for i in range(0, len(reg_vol_sort)):
    reg_vol_val[reg_vol_sort[i][0]] = reg_vol_sort[i][1]#Get values from sorted list

explode = (0.1,0.1,0.1,0,0,0,0,0,0,0,0)

pie_col = random.sample(colours, len(colours))

#Plot the analysis
fig2 = plt.figure(figsize=(10,8))
plt.pie(reg_vol_val.values(), labels=reg_vol_val.keys(), explode = explode, autopct='%.1f%%', shadow=True, startangle=90, radius = 1, labeldistance=1.05, frame=True, colors=pie_col ,
pctdistance= 0.8 , wedgeprops={'edgecolor': 'black','linewidth': 1}, textprops={'fontsize':12, 'fontweight':wht})
plt.axis('equal')
plt.title('2019 Regional Sales Volume', fontsize = 24)
plt.tick_params(axis = 'both', bottom=False, left=False, labelbottom=False, labelleft = False)
plt.savefig('regional_sales_volume.png')#Save figure
plt.show()
#plt.close()

#Analysis 3 - Average price and volume of items across the year

#Define lists of lists
price = []
item_vol = []

for i in range(len(months)):
    price.append([])
    item_vol.append([])

for i in range(0,len(data_arr)):
    for j in range(0,len(months)):
        if data_arr[i][1] == months[j]:
            price[j].append(float(data_arr[i][2]))
            item_vol[j].append(float(data_arr[i][4]))

avg_price = {}
avg_item_vol = {}
price_err = []
item_err = []

for i in range(0,len(months)):
    avg_price[months[i]] = np.mean(price[i])
    price_err.append(np.std(price[i])/np.sqrt(len(price[i])))
    avg_item_vol[months[i]] = np.mean(item_vol[i])
    item_err.append(np.std(item_vol[i])/np.sqrt(len(item_vol[i])))

xpos = 3*np.arange(len(months))
width = 1

#Plot analysis
fig3 = plt.figure(figsize=(14,10))
barplt1 = plt.bar(xpos, avg_price.values(), yerr = price_err, width = width, color=colours[0], edgecolor = 'black')
plt.ylabel('Average price [£]', fontsize = fnt, fontweight = wht)
plt.xlabel('Month', fontsize = fnt, fontweight = wht)

#Set fontsize for axis tickers
for item in (plt.gca().get_xticklabels() + plt.gca().get_yticklabels()):
    item.set_fontsize(14)

plt.twinx()
barplt2 = plt.bar(xpos+width, avg_item_vol.values(), yerr = item_err, width  = width, color=colours[8], edgecolor = 'black')
plt.xticks(xpos + width/2, avg_price.keys())

#Set fontsize for axis tickers
for item in (plt.gca().get_yticklabels()):
    item.set_fontsize(14)

plt.ylabel('Average item volume', fontsize = fnt, fontweight = wht)
plt.title('2019 Monthly Sale Value & Item Volume', fontsize = 20)

plt.bar(0,0, color = colours[0], label = 'Price')
plt.bar(0,0, color = colours[8], label = 'Item Volume')
plt.legend(loc='upper left', fontsize = 16, framealpha = 1, ncol =2)
plt.savefig('monthly_price_item.png')
#plt.show()
plt.close()

# Analysis 4 - Do loyality customers spend more on average?

#Define lists
loyal = []
Nloyal = []

for i in range(0,len(data_arr)):
    if data_arr[i][5] == 'Null' or data_arr[i][5] == 'NULL':
        Nloyal.append(float(data_arr[i][2]))
    else:
        loyal.append(float(data_arr[i][2]))

loyal_avg = np.mean(loyal)
Nloyal_avg = np.mean(Nloyal)

loyal_err = np.std(loyal)/np.sqrt(len(loyal))
Nloyal_err = np.std(Nloyal)/np.sqrt(len(Nloyal))

print(u'The average loyality customer spends £%2.f \u00B1 %1.f, whilst a non-loyality customer spends £%2.f \u00B1 %1.f' % (loyal_avg,loyal_err,Nloyal_avg,Nloyal_err))