Extract Most Frequented Locations from individual spatio-temporal trajectories
========================================================================

## Description

This script returns the location most frequented by an individual (called MFL) during  weekdays' daytime and nighttime
according to a certain time window. The MFL during a given time windows is defined as the  location in which 
the individual has spent most of his/her time. In this algorithm, two scales are considered, hours and days. 
Hopefully, for a given individual, the MFLs detected at the two scales should be the same.

## Input

The algorithm takes as input a 6 columns csv file with column names, **the value separator is a semicolon ";"**. Each row of the file represents a spatio-temporal position of an individual's trajectory. The time is given by the columns 2 to 5 (year, month, day and hour).
It is important to note that the table should be **SORTED** by individual ID and time.

1. **ID of the individual**
2. **Year**
3. **Month** (1->12)
4. **Day** (1->31)
5. **Hour** (0->23)
6. **ID of the geographical location** 

## Parameters
 
The algorithm has 6 parameters:

1. **wdinput:**  Path of the input file (ex: "input.csv")
2. **wdoutput:** Path of the output file (ex: "outputoftheawsomemaximelenormandsalgorithm.csv")
3. **minH:** Lower bound (included) of the night time window (ex: 20h)
4. **maxH:** Upper bound (included) of the night time window (ex: 7h)
5. **minW:** Lower bound (included) of the day time window (ex: 8h)
6. **maxW:** Upper bound (included) of the day time window (ex: 19h)

## Output

The algorithm returns a 19 columns csv file with column names, **the value separator is a semicolon ";"**. Each row represents an individual:

1.  **ID:** ID of the individual
2.  **NbMonths:** Number of distinct months covered by the trajectory
3.  **NbConsMonths:** Maximum number of consecutive months covered by the trajectory 
4.  **MFLHomeDays:** MFL during nighttime (day scale), 'NoMFL' if NbDaysHome=0 
5.  **MFLHomeDays2:** Second MFL during nighttime (day scale) if ex aqueo, 'NoMFL' otherwise  
6.  **NbDaysHomeMFL:** Number of distinct days (during nighttime) spent in the MFL
7.  **NbDaysHome:** Number of distinct days covered by the trajectory (during nighttime)
8.  **MFLHomeHours:** MFL during nighttime (hour scale), 'NoMFL' if NbHoursHome=0
9.  **MFLHomeHours2:** Second MFL during nighttime (hour scale) if ex aqueo, 'NoMFL' otherwise  
10. **NbHoursHomeMFL:** Number of distinct hours spent in the MFL (during nighttime)
11. **NbHoursHome:** Number of distinct hours covered by the trajectory (during nighttime)
12. **MFLWorkDays:** MFL during daytime (day scale), 'NoMFL' if NbDaysWork=0
13. **MFLWorkDays2:** Second MFL during daytime (day scale) if ex aqueo, 'NoMFL' otherwise 
14. **NbDaysWorkMFL:** Number of distinct days spent in the MFL (during daytime)
15. **NbDaysWork:** Number of distinct days covered by the trajectory (during daytime)
16. **MFLWorkHours:** MFL during daytime (hour scale), 'NoMFL' if NbHoursWork=0
17. **MFLWorkHours2:** Second MFL during daytime (hour scale) if ex aqueo, 'NoMFL' otherwise
18. **NbHoursWorkMFL:** Number of distinct days spent in the MFL (during daytime)
19. **NbHoursWork:** Number of distinct hours covered by the trajectory (during daytime)

## Execution

You can run the code using the command:

**python MFL.py input.csv output.csv 20 7 8 19**

## Citation

If you use this code, please cite:

Lenormand M, Louail T, Barthelemy M & Ramasco JJ (2016) [Is spatial information in ICT data reliable?](https://arxiv.org/abs/1609.03375) In proceedings of the 2016 Spatial Accuracy Conference, 9-17, Montpellier, France.

If you need help, find a bug, want to give me advice or feedback, please contact me!
You can reach me at maxime.lenormand[at]inrae.fr
