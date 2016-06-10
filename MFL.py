"""
Extract Home and Work locations from individual spatio-temporal trajectories

This script returns the location most frequented by an individual (called MFL) during weekdays' daytime and nighttime
according to a certain time window. The MFL during a given time windows is defined as the location in which 
the individual has spent most of his/her time. In this algorithm, two scales are considered, hours and days. 
Hopefully, for a given individual, the MFLs detected at the two scales should be the same.

The algorithm takes as input a 6 columns csv file with column names (the value separator is a semicolon ";").
Each row of the file represents a spatio-temporal position of an individual's trajectory. The time is given 
by the columns 2 to 5. 

It is important to note that the table must be SORTED by individual ID and by time.
   
	1. User ID
	2. Year
	3. Month
	4. Day
	5. Hour
	6. ID of the geographical location 
 
The algorithm has 6 parameters:

	1. wdinput:  Path of the input file
	2. wdoutput: Path of the output file
	3. minH: Lower bound (included) of the night time window (ex: 8pm)
	4. maxH: Upper bound (included) of the night time window (ex: 7am)
	5. minW: Lower bound (included) of the day time window (ex: 8am)
	6. maxW: Upper bound (included) of the day time window (ex: 7pm)

The algorithm returns a 19 columns csv file with column names (the value separator is a semicolon ";"). 
Each row represents an individual.
          
	1.  ID: ID of the individual
        2.  NbMonths: Number of distinct months covered by the trajectory
        3.  NbConsMonths: Maximum number of consecutive months covered by the trajectory 
        4.  MFLHomeDays: MFL during nighttime (day scale), 'NoMFL' if NbDaysHome=0 
        5.  MFLHomeDays2: Second MFL during nighttime (day scale) if ex aqueo, 'NoMFL' otherwise  
        6.  NbDaysHomeMFL: Number of distinct days (during nighttime) spent in the MFL
        7.  NbDaysHome: Number of distinct days covered by the trajectory (during nighttime)
        8.  MFLHomeHours: MFL during nighttime (hour scale), 'NoMFL' if NbHoursHome=0
        9.  MFLHomeHours2: Second MFL during nighttime (hour scale) if ex aqueo, 'NoMFL' otherwise  
        10. NbHoursHomeMFL: Number of distinct hours spent in the MFL (during nighttime)
        11. NbHoursHome: Number of distinct hours covered by the trajectory (during nighttime)
        12. MFLWorkDays: MFL during daytime (day scale), 'NoMFL' if NbDaysWork=0
        13. MFLWorkDays2: Second MFL during daytime (day scale) if ex aqueo, 'NoMFL' otherwise 
        14. NbDaysWorkMFL: Number of distinct days spent in the MFL (during daytime)
        15. NbDaysWork: Number of distinct days covered by the trajectory (during daytime)
        16. MFLWorkHours: MFL during daytime (hour scale), 'NoMFL' if NbHoursWork=0
        17. MFLWorkHours2: Second MFL during daytime (hour scale) if ex aqueo, 'NoMFL' otherwise
        18. NbHoursWorkMFL: Number of distinct days spent in the MFL (during daytime)
        19. NbHoursWork: Number of distinct hours covered by the trajectory (during daytime)

Copyright 2015 Maxime Lenormand. All rights reserved. Code under License GPLv3.
"""

# ****************************** IMPORTS ********************************************************************
# ***********************************************************************************************************

import sys
import random
from datetime import datetime
import operator

# ****************************** PARAMETRES *****************************************************************
# ***********************************************************************************************************

wdinput = sys.argv[1]
wdoutput = sys.argv[2]
minH = int(sys.argv[3])   #Nighttime: [minW,maxW]
maxH = int(sys.argv[4])
minW = int(sys.argv[5])   #Daytime: [minH,maxH]
maxW = int(sys.argv[6])

print(" ") 
print("Parameters:" + " "+ wdinput + " " + wdoutput + " " + str(minH) + " " + str(maxH) + " " + str(minW) + " " + str(maxW))
print(" ") 
   
# ****************************** MAIN ***********************************************************************
# ***********************************************************************************************************

#Input file                                        
input_file = open(wdinput)                                 #Open file 
next(input_file)                                           #Skip column names

input_file2 = open(wdinput)                                #Open the file again to detect the last user's position
next(input_file2)                                          #Skip column names
next(input_file2)                                          #Skip first position

#Output file
output_file = open(wdoutput,'w')
output_file.write('ID')                                   
output_file.write(';')
output_file.write('NbMonths')
output_file.write(';')
output_file.write('NbConsMonths')
output_file.write(';')
output_file.write('MFLHomeDays')
output_file.write(';')
output_file.write('MFLHomeDays2')
output_file.write(';')
output_file.write('NbDaysHomeMFL')
output_file.write(';')
output_file.write('NbDaysHome')
output_file.write(';')
output_file.write('MFLHomeHours')
output_file.write(';')
output_file.write('MFLHomeHours2')
output_file.write(';')
output_file.write('NbHoursHomeMFL')
output_file.write(';')
output_file.write('NbHoursHome')
output_file.write(';')
output_file.write('MFLWorkDays')
output_file.write(';')
output_file.write('MFLWorkDays2')
output_file.write(';')
output_file.write('NbDaysWorkMFL')
output_file.write(';')
output_file.write('NbDaysWork')
output_file.write(';')
output_file.write('MFLWorkHours')
output_file.write(';')
output_file.write('MFLWorkHours2')
output_file.write(';')
output_file.write('NbHoursWorkMFL')
output_file.write(';')
output_file.write('NbHoursWork')
output_file.write('\n')

#Initializing Variables
NbTotMonths = 0      #Total number of distinct months covered by the trajectories
TotMonths = {}       #Dictionary of months

NbMonths = 0         #Number of distinct months covered by the trajectory
NbConsMonthsTmp = 0  #Temporary number of consecutive months
NbConsMonths = 0     #Maximal number of consecutive months  
YearMonth = ()       #List of years 
MonthMonth = ()      #List of months
 
Hday = {}            #Dictionary containing for each location a counter and a dictionary of days (during nighttime) 
NbHday={}            #Dictionary of distinct days covered by the trajectory (during nighttime)
Hhour = {}           #Dictionary containing for each location a counter and a dictionary of hours (during nighttime) 
NbHhour={}           #Dictionary of distinct hours covered by the trajectory (during nighttime)
Wday = {}            #Dictionary containing for each location a counter and a dictionary of days (during daytime)  
NbWday={}            #Dictionary of distinct days covered by the trajectory (during daytime)
Whour = {}           #Dictionary containing for each location a counter and a dictionary of hours (during daytime)    
NbWhour={}           #Dictionary of distinct hours covered by the trajectory (during daytime)

nbuser = 0           #Counter user

#Looping through the file line by line
for line in input_file:
    
    #Print number users
    if random.random() > 0.99999:
        print ("Number of users:" + " " + str(nbuser))
    
    #User's position attributes
    attr = line.rstrip('\n\r').split(';')         #Split line
    ID = attr[0]                                  #Individual ID
    year = int(attr[1])                           #Year
    month = int(attr[2])                          #Month
    day = int(attr[3])                            #Day
    hour = int(attr[4])                           #Hour  
    loc = int(attr[5])                            #Location ID

    YM = str(year) + "_" + str(month)                                        #Month ID    
    YMD = str(year) + "_" + str(month) + "_" + str(day)                      #Day ID
    YMDH = str(year) + "_" + str(month) + "_" + str(day) + "_" + str(hour)   #Hour ID
    
    #Weed day (from 0 to 6)
    weekday=datetime(int(year), int(month), int(day))
    weekday=weekday.weekday()
    
    #Next User ID to detect the last users' position and the last line
    try:
        attr = next(input_file2).rstrip('\n\r').split(';')
        ID_next = attr[0]                                         #User ID                                   
    except(StopIteration):
        ID_next = ID + "last"                                     #Fake ID if last line
    
    
    #Total number of distinct months
    if (not TotMonths.__contains__(YM)): #if new month increase the counter
        NbTotMonths = NbTotMonths + 1
        TotMonths[YM] = 0
         
    #Month
    YearMonth = YearMonth + (year,)
    MonthMonth = MonthMonth + (month,)
    if len(YearMonth)>1:
        if (not (year == YearMonth[-2] and month == MonthMonth[-2])):
	    NbMonths = NbMonths + 1
            if ((year == YearMonth[-2] and month == (MonthMonth[-2]+1)) or (year == (YearMonth[-2]-1) and month == 1 and MonthMonth[-2]==12)):
               NbConsMonthsTmp = NbConsMonthsTmp + 1
               NbConsMonths = max(NbConsMonths, NbConsMonthsTmp)
            else:                
               NbConsMonthsTmp = 1     
    else:
        NbMonths = 1
        NbConsMonthsTmp = 1  
        NbConsMonths = 1

    #Home    
    if (((hour >= minH) or (hour <= maxH)) and (weekday < 5)):
        #If new day increase the counter                
        if (not (NbHday.__contains__(YMD))):
            NbHday[YMD]=1
        #If new hour increase the counter                
        if (not (NbHhour.__contains__(YMDH))):
            NbHhour[YMDH]=1
        #If the location already exists
        if Hday.__contains__(loc):
            #If new day increase the counter 
            if (not (Hday[loc][1].__contains__(YMD))):
                Hday[loc][0] = Hday[loc][0] + 1
                Hday[loc][1][YMD] = 0         
            #If new hour increase the counter
            if (not (Hhour[loc][1].__contains__(YMDH))):
                Hhour[loc][0] = Hhour[loc][0] + 1
                Hhour[loc][1][YMDH] = 0
        #If new location         
        else:
            Hday[loc] = [1,{}]
            Hday[loc][1][YMD] = 0
            Hhour[loc] = [1,{}]
            Hhour[loc][1][YMDH] = 0
            
    #Work
    if (((hour >= minW) and (hour <= maxW)) and (weekday < 5)):
        #If new day increase the counter                
        if (not (NbWday.__contains__(YMD))):
            NbWday[YMD]=1
        #If new hour increase the counter                
        if (not (NbWhour.__contains__(YMDH))):
            NbWhour[YMDH]=1
        #If the location already exists
        if Wday.__contains__(loc):
            #If new day increase the counter
            if (not (Wday[loc][1].__contains__(YMD))):
                Wday[loc][0] = Wday[loc][0] + 1
                Wday[loc][1][YMD] = 0                    
            #If new hour increase the counter    
            if (not (Whour[loc][1].__contains__(YMDH))):
                Whour[loc][0] = Whour[loc][0] + 1
                Whour[loc][1][YMDH] = 0
        #If new location        
        else:
            Wday[loc] = [1,{}]
            Wday[loc][1][YMD] = 0
            Whour[loc] = [1,{}]
            Whour[loc][1][YMDH] = 0        
        
     
    #If last user's position, extract the metrics    
    if (ID != ID_next):
        
        #Home day
        MFLHomeDays = 'NoMFL'
        MFLHomeDays2 = 'NoMFL'
        NbDaysHomeMFL = 0
        sort = sorted(Hday.items(), key=operator.itemgetter(1), reverse=True)  #Sort locations by number of days
        if len(sort):
            MFLHomeDays = sort[0][0]
            NbDaysHomeMFL = sort[0][1][0]
            if len(sort)>1:
                if sort[1][1][0] == sort[0][1][0]:
                    MFLHomeDays2 = sort[1][0]
  
        #Home hour
        MFLHomeHours = 'NoMFL'
        MFLHomeHours2 = 'NoMFL'
        NbHoursHomeMFL = 0
        sort = sorted(Hhour.items(), key=operator.itemgetter(1), reverse=True)  #Sort locations by number of hours
        if len(sort):
            MFLHomeHours = sort[0][0]
            NbHoursHomeMFL = sort[0][1][0]
            if len(sort)>1:
                if sort[1][1][0] == sort[0][1][0]:
                    MFLHomeHours2 = sort[1][0]

        #Work day
        MFLWorkDays = 'NoMFL'
        MFLWorkDays2 = 'NoMFL'
        NbDaysWorkMFL = 0
        sort = sorted(Wday.items(), key=operator.itemgetter(1), reverse=True)   #Sort location by number of days
        if len(sort):
            MFLWorkDays = sort[0][0]
            NbDaysWorkMFL = sort[0][1][0]
            if len(sort)>1:
                if sort[1][1][0] == sort[0][1][0]:
                    MFLWorkDays2 = sort[1][0]

        #Work hour
        MFLWorkHours = 'NoMFL'
        MFLWorkHours2 = 'NoMFL'
        NbHoursWorkMFL = 0
        sort = sorted(Whour.items(), key=operator.itemgetter(1), reverse=True)  #Sort location by number of hours
        if len(sort):
            MFLWorkHours = sort[0][0]
            NbHoursWorkMFL = sort[0][1][0]
            if len(sort)>1:
                if sort[1][1][0] == sort[0][1][0]:
                    MFLWorkHours2 = sort[1][0]
            
        #Write output
        output_file.write(str(ID))                                   
        output_file.write(';')
        output_file.write(str(NbMonths))
        output_file.write(';')
        output_file.write(str(NbConsMonths))
        output_file.write(';')
        output_file.write(str(MFLHomeDays))
        output_file.write(';')
        output_file.write(str(MFLHomeDays2))
        output_file.write(';')
        output_file.write(str(NbDaysHomeMFL))
        output_file.write(';')
        output_file.write(str(len(NbHday)))
        output_file.write(';')
        output_file.write(str(MFLHomeHours))
        output_file.write(';')
        output_file.write(str(MFLHomeHours2))
        output_file.write(';')
        output_file.write(str(NbHoursHomeMFL))
        output_file.write(';')
        output_file.write(str(len(NbHhour)))
        output_file.write(';')
        output_file.write(str(MFLWorkDays))
        output_file.write(';')
        output_file.write(str(MFLWorkDays2))
        output_file.write(';')
        output_file.write(str(NbDaysWorkMFL))
        output_file.write(';')
        output_file.write(str(len(NbWday)))
        output_file.write(';')
        output_file.write(str(MFLWorkHours))
        output_file.write(';')
        output_file.write(str(MFLWorkHours2))
        output_file.write(';')
        output_file.write(str(NbHoursWorkMFL))
        output_file.write(';')
        output_file.write(str(len(NbWhour)))
        output_file.write('\n')
        
        #Re-initialise the variables
        YearMonth = ()    
        MonthMonth = ()      
        NbConsMonthsTmp = 0  
        NbConsMonths = 0    
        Hday = {}          
        NbHday={}
        Hhour = {}         
        NbHhour={}
        Wday = {}          
        NbWday={}
        Whour = {}         
        NbWhour={}        
                
        nbuser = nbuser + 1    #count user

#Close files
input_file.close()
input_file2.close()
output_file.close()

#Print the total number of months
print(" ") 
print("The total number of distinct months covered by the trajectories is " + str(NbTotMonths))  
