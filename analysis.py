#Importing modules

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

months_size = [[]]#Normalisation for non-bias months

