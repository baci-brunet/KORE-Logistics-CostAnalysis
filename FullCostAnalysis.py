#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Filename: Cost Analysis
#Author: Sebastian Brunet
#Date Created: July 20, 2020
#Date Last Modified: July 20, 2020

'''The first program is a simple one; computes the average 
time and optimimum number of employees for a given task (repalletizing, delabeling, etc.). 

The second program is intended to read EACH order invoice and determine using our precomputed 
averages, what the cost of a given task is when done optimally. Considering several assumptions like 
number of employees per task, average time taken by those employees, average time forklift is in use per 
task and average amount of material used, this program will produce a cost estimate for a given order. 
'''
'''An IN AND OUT order simply consists of offloading, repalletizing, 
        and onloading, so we will group the next two when considering in and outs'''

import xlrd
import os, sys
from time import sleep

class Labor:
    #This function considers the average wage for employees per minute of work for a given activity at the warehouse.
    def emp_cost(self, num_emp, time):
        x = input("Type 'yes' if you would like to use our precomputed average wage of $11.74, or input a specific wage to see how it affects cost? ")
        if x == 'yes':
            avg_wage = 11.74
        else:
            x = float(x)
            avg_wage = x
        avg_cost_per_emp_per_minute = avg_wage / 60
        tot_emp_cost_per_minute = avg_cost_per_emp_per_minute * num_emp
        #TIME IN MINUTES
        tot_emp_cost = tot_emp_cost_per_minute * time
        return tot_emp_cost  

class Materials:
    def tot_sw_amount(self, num_pallets):
        #PRICE FOR A PALLET
        pallet_cost = 0
        tot_pallet_cost = pallet_cost * num_pallets
        #AVERAGE HEIGHT OF A PACKED PALLET
        p = input("Type 'yes' if you would like to use our precalculated average height of 50 inches/pallet, or input a specific height to see how much the shrink wrap for a given pallet will cost? ")
        if p == 'yes':
            avg_height = 50
        else:
            p = float(p)
            if p == 0:
                print('0 is not a valid input')
            else:
                avg_height = p
        #PALLET LENGTH AND WIDTH
        length = 40
        width = 48
        #FORMULA FOR THE SQUARE INCHES OF PALLET TO BE COVERED BY SHRINK WRAP
        pallet_SW = (2 * ((width * avg_height) + (length * avg_height))) * 4
        #ACCOUNTING FOR 3% SCRAPPED SHRINK WRAP 
        scrap = .03 * pallet_SW
        tot_pallet_SW = scrap + pallet_SW
        tot_order_SW = num_pallets * tot_pallet_SW
        return tot_order_SW

    def tot_sw_cost(self, tot_order_SW):
        #SHRINK WRAP PRICE BELOW
        cost_per_roll_sw = 7.25
        #SHRINK WRAP SIZE IN SQUARE INCHES
        size_of_sw = 216000 #in inches
        cost_per_sqin_sw = cost_per_roll_sw / size_of_sw
        cost_sw = cost_per_sqin_sw * tot_order_SW
        return cost_sw

    def forklift_cost(self, minutes_of_use):
        #FORKLIFT GAS COST BELOW
        cost_full_tank = 5.4
        tot_gas_cost_per_min = cost_full_tank / 480 #8 hours so 480 minutes
        tot_gas_cost = tot_gas_cost_per_min * minutes_of_use 
        #depreciation = 0 must add the depreciation on the forklift to costs as it represents the amount lost each year on paper
        #maintenance = 0 must add maintenance cost to formula
        return tot_gas_cost
    
    def pallet_cost(self, num_pallets):
        #Each pallet is purchased for $5.50 and eventually sold for $2.50, therefore, it costs the company $3.00 a pallet
        x = input("Enter 'yes' if this order requires a FULL set of new pallets. Enter 'no' if this order requires no new pallets. If the order requires some new pallets but not a full set, enter the number of pallets needed.")
        if x == 'yes':
            pallet_cost = 3
        elif x == 'no':
            pallet_cost = 0
        else:
            x = float(x)
            pallet_cost = 3
            num_pallets = x 
        tot_pallet_cost = num_pallets * pallet_cost
        return tot_pallet_cost
        
def main():
    
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    loc = os.path.join(dirname, "InvoiceExample.xlsx")
  
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
    
    obj2 = Materials()
    obj = Labor()
    
    
    ans, ans2, ans3, ans4, ans5, ans6, ans7, ans8, ans9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(1, sheet.nrows): 
        if sheet.cell_value(i, 0) == 'Delabelling/Xray/Repalletizing':
            print('Task: Delabelling/Xray/Repalletizing')
            print('Assuming 4 employees are working on this task, it should take approximately 65.11 minutes per standard pallet (50 inches tall). The forklift will run for approximately 3 minutes.')
            time = 65.11
            num_emp = 4
            num_pallets = float(sheet.cell_value(i, 1))
            time_forklift = 3 #add average time forklift is in use
            b = obj2.tot_sw_amount(num_pallets)
            c = obj2.tot_sw_cost(b)
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans = c + f + obj.emp_cost(num_emp, time)
            print(ans)
            
        elif sheet.cell_value(i, 0) == 'Delabelling/Repalletizing':
            print('Task: Delabelling/Repalletizing')
            print('Assuming 3 employees are working on this task, it should take approximately 57.43 minutes per standard pallet (50 inches tall). The forklift will run for approximately 3 minutes.')
            time = 57.43
            num_emp = 3
            num_pallets = sheet.cell_value(i, 1)
            time_forklift = 3 #add average time forklift is in use
            b = obj2.tot_sw_amount(num_pallets)
            c = obj2.tot_sw_cost(b)
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans2 = c + f + obj.emp_cost(num_emp, time)
            print(ans2)

        elif sheet.cell_value(i, 0) == 'Repalletizing':
            print('Task: Repalletizing')
            print('Assuming 2 employees are working on this task, it should take approximately 3.63 minutes per standard pallet (50 inches tall). The forklift will run for approximately 2 minutes.')
            time = 3.63
            num_emp = 2
            num_pallets = sheet.cell_value(i, 1)
            time_forklift = 2 #add average time forklift is in use
            b = obj2.tot_sw_amount(num_pallets)
            c = obj2.tot_sw_cost(b)
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans3 = c + f + obj.emp_cost(num_emp, time)
            print(ans3)
            
        elif sheet.cell_value(i, 0) == 'Xray/Repalletizing':
            print('Task: Xray/Repalletizing')
            print('Assuming 7 employees are working on this task, it should take approximately 4.21 minutes per standard pallet (50 inches tall). The forklift will run for approximately 2 minutes.')
            time = 7
            num_emp = 4.21
            num_pallets = sheet.cell_value(i, 1)
            time_forklift = 2 #add average time forklift is in use
            b = obj2.tot_sw_amount(num_pallets)
            c = obj2.tot_sw_cost(b)
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans4 = c + f + obj.emp_cost(num_emp, time)
            print(ans4)
            
        elif sheet.cell_value(i, 0) == 'Offloading':
            print('Task: Offloading')
            print('Assuming 2 employees are working on this task, it should take approximately 75 minutes per 24 pallet truck (assuming standard 50 inch tall pallets). This means each pallet takes 3.125 minutes to offload. The forklift will run for 50 minutes.')
            time = 3.125
            num_emp = 2
            num_pallets = sheet.cell_value(i, 1)
            time_forklift = 50 #add average time forklift is in use
            d = obj2.pallet_cost(num_pallets) #If we do not use any of our own pallets, this is zero
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans6 = d + f + obj.emp_cost(num_emp, time)
            print(ans6)
        
        elif sheet.cell_value(i, 0) == 'Onloading':
            print('Task: Onloading')
            print('Assuming 1 employee is working on this task with the driver, it should take approximately 50 minutes per 24 pallet truck (assuming standard 50 inch tall pallets). This means each pallet takes 2.1 minutes to offload. The forklift will run for 40 minutes.')
            time = 2.1
            num_emp = 1
            num_pallets = sheet.cell_value(i, 1)
            time_forklift = 40 #add average time forklift is in use
            f = obj2.forklift_cost(time_forklift) * num_pallets
            ans7 = f + obj.emp_cost(num_emp, time)
            print(ans7)
    
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("There are no more sevices to process.")    
    print("Total cost for the invoice is:", ans + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8 + ans9)
    sleep(10.00)        

if __name__=="__main__": 
    main() 

            


# In[ ]:




