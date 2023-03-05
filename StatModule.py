import csv 
import math
from collections import Counter

""" 
    * Apply  Python's statistics module to your csv file which doesn't require other parameters(quantiles or linear regression for example). 
    * The datasets columns must have numerical values.
    
    StatModule.Statistics(*file, to_csv= False, round_k = 2):
        The function to handle statistics module.

        Parameters:
            *path
                [str] Location of csv file.
            to_csv
                [str] Default: False. If its a string, will create a csv file which its name is string value. Returns statistics even 
                if it has a string value.
            round_k
                [int] Default: 2. Determine the rounds of outputs to make statistics look less ugly. 
        
        Returns:
            [list] Statistics of each column 
"""

def Statistics(*path, to_csv = False, round_k = 2):
    data = []
    stat = [['Columns','Arithmetic mean','Geometric mean','Harmonic mean','Median','Low median','High median','Mode','Multimode','Population standard deviation','Population variance','Sample standard deviation','Sample variance']]
    with open(path[0], 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data.append(row)
    len_column = len(data[0])
    len_row = len(data) - 1 
    for col in range(len_column):
        single_col_values = []
        product_for_geo_mean = 1
        sum_for_harmonic_mean = 0
        sum_for_deviation = 0
        median_low = False
        median_high = False
        median = False
        mode = False
        multimode =  []
        for row in data[1:]:
            single_col_values.append(row[col])
        if (len_row % 2) == 0:
            try:
                median_low = float(single_col_values[int(len_row/2)-1])
                median_high = float(single_col_values[int((len_row/2))])
                median = float((median_low + median_high)) / 2 
            except ValueError:
                pass
        else:
            median = single_col_values[math.floor(len_row/2)] 
            median_low = median
            median_high = median
        sum = 0
        for element in single_col_values:
            try:
                sum += float(element)
                product_for_geo_mean *= float(element)
                sum_for_harmonic_mean += 1/float(element)
            except ValueError:
                pass
            except ZeroDivisionError: 
                pass
        for element in single_col_values:
            try:
                sum_for_deviation += (float(element) - (sum/len_row))**(2)
            except ValueError:
                break    
        try:
            b = Counter(iter(single_col_values))
            maxcount = max(b.values())
            if maxcount != 1:
                mode = float(max(single_col_values, key=single_col_values.count)),
                mode = mode[0]
                for value,count in b.items():
                    if count == maxcount:
                        multimode.append(float(value)) 
            else:
                mode = "Every Element is mode"    
                multimode.append("Every Element is mode")
        except ValueError:
            mode = "NaN"
            multimode = "NaN"
        try:
            PopVariance = sum_for_deviation/len_row
            SampVariance = sum_for_deviation/(len_row - 1)
            stat.append(
                [
                data[0][col],
                round((sum/len_row), round_k),
                round(product_for_geo_mean**(1/len_row), round_k), 
                round((sum_for_harmonic_mean/len_row)**(-1), round_k),
                median, 
                median_low,   
                median_high, 
                mode,
                multimode,
                round((PopVariance**(1/2)),round_k),
                round((PopVariance),round_k),
                round((SampVariance**(1/2)),round_k),
                round((SampVariance),round_k),
                 ]
                )
        except TypeError:
            pass
        except ZeroDivisionError:
            pass
    if to_csv != False:
        with open( to_csv + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(stat)
    return stat 