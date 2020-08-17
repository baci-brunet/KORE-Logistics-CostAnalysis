#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Filename: Cost Analysis
#Author: Sebastian Brunet
#Date Created: July 20, 2020
#Date Last Modified: July 20, 2020

'''The first program is a simple one -- computes the average 
time and optimimum number of employees for a given task (repalletizing, delabeling, etc.).'''

import xlrd
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
        p = input("Type 'yes' if you would like to use our precalculated average height of 50 inches, or input a specific height to see how much the shrink wrap for a given pallet will cost? ")
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
    

#main 
def main():
    obj2 = Materials()
    a = int(input("Enter the number of pallets in this order: "))
    b = obj2.tot_sw_amount(a) 
    c = obj2.tot_sw_cost(b)
    d = obj2.pallet_cost(a)
    e = int(input("Enter how long (in minutes) the forklift was being used for: "))
    f = obj2.forklift_cost(e)
    obj = Labor()
    x = float(input("Enter the number of employees} on the job: "))
    y = float(input("Enter how long (in minutes) it took to complete the task: "))
    z = obj.emp_cost(x, y)
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("...")
    sleep(1.00)
    print("The total cost for this order is:", c + d + f + z)
    sleep(3600.00)
    
if __name__=="__main__":
    main()





