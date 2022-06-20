# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:00:11 2021

@author: Erika
"""

# ensures I can run the notebook multiple times without errors
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import networkx as nx

# changing directory to my stored data
os.chdir("C:\\Users\\Admin\\Documents\\SIM Coursework Final\\Assignment 3 practice\\Data Expo 2009")

# connect to database
conn = sqlite3.connect('airline_p.db')

# to set up tables in airlines_p.db
airports = pd.read_csv(".\\airports.csv")
carriers = pd.read_csv(".\\carriers.csv")
planes = pd.read_csv(".\\plane-data.csv")

airports.to_sql('airports', con = conn, index = False)
carriers.to_sql('carriers', con = conn, index = False)
planes.to_sql('planes', con = conn, index = False)

# read individual ontime csv from 2004 to 2008
ontime04 = pd.read_csv("2004.csv", encoding = "latin-1")
ontime05 = pd.read_csv("2005.csv", encoding = "latin-1")
ontime06 = pd.read_csv("2006.csv", encoding = "latin-1")
ontime07 = pd.read_csv("2007.csv", encoding = "latin-1")
ontime08 = pd.read_csv("2008.csv", encoding = "latin-1")

# concatonate all the ontime files into one 'ontime'
ontime1 = pd.concat([ontime04, ontime05], ignore_index = True)
ontime2 = pd.concat([ontime1, ontime06], ignore_index = True)
ontime3 = pd.concat([ontime2, ontime07], ignore_index = True)
ontime = pd.concat([ontime3, ontime08], ignore_index = True)

# removal of unwanted tables in variable explorer
del ontime04, ontime05, ontime06, ontime07, ontime08
del ontime1, ontime2, ontime3

# runs dataframes into sql
ontime.to_sql('ontime', con = conn, index = False)

# shortcut to access my database
c = conn.cursor()

# i had issues with connecting my 'ontime' file into the sql table so i had to drop the table in my database and commit those changes before
## redo-ing the connection above at line 46
c.execute("DROP TABLE ontime")
conn.commit()


# check that all tables are there
c.execute('''
          SELECT name
          FROM sqlite_master
          WHERE type = 'table'
          ''').fetchall()
          
# ---------------------- QUESTION ONE ---------------------------
# 1. When is the best time of day, day of the week, and time of year to fly to minimise delays?

time = c.execute('''
               SELECT
CASE
WHEN CRSDepTime >= 0000 AND CRSDepTime <= 0159 THEN '0000 to 0159'
WHEN CRSDepTime >= 0200 AND CRSDepTime <= 0359 THEN '0200 to 0359'
WHEN CRSDepTime >= 0400 AND CRSDepTime <= 0559 THEN '0400 to 0559'
WHEN CRSDepTime >= 0600 AND CRSDepTime <= 0759 THEN '0600 to 0759'
WHEN CRSDepTime >= 0800 AND CRSDepTime <= 0959 THEN '0800 to 0959'
WHEN CRSDepTime >= 1000 AND CRSDepTime <= 1159 THEN '1000 to 1159'
WHEN CRSDepTime >= 1200 AND CRSDepTime <= 1359 THEN '1200 to 1359'
WHEN CRSDepTime >= 1400 AND CRSDepTime <= 1559 THEN '1400 to 1559'
WHEN CRSDepTime >= 1600 AND CRSDepTime <= 1759 THEN '1600 to 1759'
WHEN CRSDepTime >= 1800 AND CRSDepTime <= 1959 THEN '1800 to 1959'
WHEN CRSDepTime >= 2000 AND CRSDepTime <= 2159 THEN '2000 to 2159'
WHEN CRSDepTime >= 2200 AND CRSDepTime <= 2359 THEN '2200 to 2359'
END,
round(AVG(DepDelay), 3) as avg_delay
FROM ontime
GROUP BY
CASE
WHEN CRSDepTime >= 0000 AND CRSDepTime <= 0159 THEN '0000 to 0159'
WHEN CRSDepTime >= 0200 AND CRSDepTime <= 0359 THEN '0200 to 0359'
WHEN CRSDepTime >= 0400 AND CRSDepTime <= 0559 THEN '0400 to 0559'
WHEN CRSDepTime >= 0600 AND CRSDepTime <= 0759 THEN '0600 to 0759'
WHEN CRSDepTime >= 0800 AND CRSDepTime <= 0959 THEN '0800 to 0959'
WHEN CRSDepTime >= 1000 AND CRSDepTime <= 1159 THEN '1000 to 1159'
WHEN CRSDepTime >= 1200 AND CRSDepTime <= 1359 THEN '1200 to 1359'
WHEN CRSDepTime >= 1400 AND CRSDepTime <= 1559 THEN '1400 to 1559'
WHEN CRSDepTime >= 1600 AND CRSDepTime <= 1759 THEN '1600 to 1759'
WHEN CRSDepTime >= 1800 AND CRSDepTime <= 1959 THEN '1800 to 1959'
WHEN CRSDepTime >= 2000 AND CRSDepTime <= 2159 THEN '2000 to 2159'
WHEN CRSDepTime >= 2200 AND CRSDepTime <= 2359 THEN '2200 to 2359'
END
               ''').fetchall()

time

timedf = pd.DataFrame(time, columns = ['time', 'avg delay'])

#plot graph & find out how to input the data on top of the bar plots & try again
# colours = ['r' if timedf['avg delay'].min() else 'b']
timeplot = timedf.plot.bar(x = 'time', y = 'avg delay', rot = 0,
                figsize = (20, 10),
                title = 'Best time of day',
                xlabel = 'Time',
                ylabel = 'Average Delay',
                # color = colours,
                fontsize='large')

# placed a round function to round to the nearest 2 dp for a cleaner look on the result output
day = c.execute('''
                 SELECT DayofWeek as day, ROUND(AVG(DepDelay), 3) as avg_delay
                 FROM ontime
                 GROUP BY day
                 ORDER BY avg_delay
                 ''').fetchall()

daydf = pd.DataFrame(day, columns = ['day', 'avg delay'])

#plot graph
daydf.plot.bar(x = 'day', y = 'avg delay', rot = 0,
                figsize = (10, 6),
                title = 'Best day of week',
                xlabel = 'Day',
                ylabel = 'Average Delay',
                fontsize='large')

# assumed time of year was based on months
year = c.execute('''
                 SELECT Month as month, ROUND(avg(DepDelay), 3) as avg_delay
                 FROM ontime
                 GROUP BY month
                 ORDER BY avg_delay
                 ''').fetchall()

yeardf = pd.DataFrame(year, columns = ['month', 'avg delay'])

#plot graph
yeardf.plot.bar(x = 'month', y = 'avg delay', rot = 0,
                figsize = (20, 10),
                title = 'Best time of year',
                xlabel = 'Month',
                ylabel = 'Average Delay',
                fontsize='large')

# ---------------------- QUESTION TWO ---------------------------
# 2. Do older planes suffer more delays?

# checking the range of plane's manufactured years
manufactured_year = c.execute('''
                              SELECT DISTINCT year
                              FROM planes
                              ORDER BY year
                              ''').fetchall()
                              
df_manuyear = pd.DataFrame(manufactured_year, columns = ['year'])


# this states that the median year in the data frame is 1983 (assumption same, older planes < 1983, newer planes > 1983)
pd.DataFrame.median(df_manuyear[2:51])

older_planes = c.execute('''
                         SELECT planes.year as planes_year, AVG(ontime.DepDelay) as avg_delay
                         FROM planes JOIN ontime USING (tailnum)
                         WHERE planes.year < 1983
                         GROUP BY planes_year
                         ORDER BY planes_year
                         ''').fetchall()
                         
df_olderplanes = pd.DataFrame(older_planes, columns = ['year', 'avg_delay'])


# to replace 0000 and removing that entire row from df_olderplanes, created my own function to make it easier to remove invalid rows
def omit(value, data):
    nan_value = float('NaN')
    data.replace(value, nan_value, inplace = True)
    data.dropna(subset = ['year'], inplace = True)
    return data

omit('0000', df_olderplanes)

newer_planes = c.execute('''
                         SELECT planes.year as planes_year, AVG(ontime.DepDelay) as avg_delay
                         FROM planes JOIN ontime USING (tailnum)
                         WHERE planes.year >= 1983
                         GROUP BY planes_year
                         ORDER BY planes_year
                         ''').fetchall()

df_newerplanes = pd.DataFrame(newer_planes, columns = ['year', 'avg_delay'])

omit('None', df_newerplanes)

# graph
bplanes = pd.concat([df_olderplanes, df_newerplanes])
tick_spacing = 2
fig, ax = plt.subplots(figsize = (15,10))
ax.plot(bplanes['year'], bplanes['avg_delay'])
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.show()

# to calculate average of total delays for both planes, made my own function
def mean(data, col):
    mean = pd.DataFrame.mean(data[col])
    result = round(mean,2)
    return result

# to calculate both dataframe's mean
older = mean(df_olderplanes, 'avg_delay')
print(older)

newer = mean(df_newerplanes, 'avg_delay')
print(newer)

answer = 'Comparing {} minutes and {} minutes, this shows that the older planes does not suffer more delays'.format(older, newer)
print(answer)

# ---------------------- QUESTION THREE ---------------------------
# 3. How does the number of people flying between different locations change over time?
# assuming the number of trips = more people in that flight to that from a particular origin

in2004 = c.execute('''
                   SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000
                   FROM ontime JOIN airports ON ontime.dest = airports.iata
                   WHERE year = 2004
                   GROUP BY states
                   ORDER BY year
                   ''').fetchall()
                   
in2005 = c.execute('''
                   SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000
                   FROM ontime JOIN airports ON ontime.dest = airports.iata
                   WHERE year = 2005
                   GROUP BY states
                   ORDER BY year
                   ''').fetchall()
                   
in2006 = c.execute('''
                   SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000
                   FROM ontime JOIN airports ON ontime.dest = airports.iata
                   WHERE year = 2006
                   GROUP BY states
                   ORDER BY year
                   ''').fetchall()                

in2007 = c.execute('''
                   SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000
                   FROM ontime JOIN airports ON ontime.dest = airports.iata
                   WHERE year = 2007
                   GROUP BY states
                   ORDER BY year
                   ''').fetchall()

in2008 = c.execute('''
                   SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000
                   FROM ontime JOIN airports ON ontime.dest = airports.iata
                   WHERE year = 2008
                   GROUP BY states
                   ORDER BY year
                   ''').fetchall()

# rename all col in the data frames and changing the 'year' column to integer type
def rename(x):
    df_x = pd.DataFrame(x, columns = ['year', 'states', 'total_trips'])
    return df_x       

names2004 = rename(in2004)
names2005 = rename(in2005)
names2006 = rename(in2006)
names2007 = rename(in2007)
names2008 = rename(in2008)

# removal of unwanted tables in variable explorer
del in2004, in2005, in2006, in2007, in2008
         
# remove NA values from above dataframe           
names2004 = names2004.dropna()
names2005 = names2005.dropna()
names2006 = names2006.dropna()
names2007 = names2007.dropna()
names2008 = names2008.dropna()

# remove DE to have a more accurate result/graph plotted
names2006 = names2006.drop(labels = 8, axis = 0)
names2007 = names2007.drop(labels = 8, axis = 0)

# filtering the states into 5 parts for each year
### GROUP BY YEAR ORDER BY STATES
## plot 1 first 10 states
upd104 = names2004[0:10]
upd105 = names2005[0:10]
upd106 = names2006[0:10]
upd107 = names2007[0:10]
upd108 = names2008[0:10]

p11 = pd.concat([upd104, upd105], ignore_index = True)
p21 = pd.concat([p11, upd106], ignore_index = True)
p31 = pd.concat([p21, upd107], ignore_index = True)
plot1 = pd.concat([p31, upd108], ignore_index = True)

plot1f = plot1.sort_values(['states', 'year'], ascending = True)
plot1f = plot1f.reset_index()

## plot 2 2nd batch of 10
upd204 = names2004[10:20]
upd205 = names2005[10:20]
upd206 = names2006[10:20]
upd207 = names2007[10:20]
upd208 = names2008[10:20]

p12 = pd.concat([upd204, upd205], ignore_index = True)
p22 = pd.concat([p12, upd206], ignore_index = True)
p32 = pd.concat([p22, upd207], ignore_index = True)
plot2 = pd.concat([p32, upd208], ignore_index = True)

plot2f = plot2.sort_values(['states', 'year'], ascending = True)
plot2f = plot2f.reset_index()

## plot 3 3rd batch of 10
upd304 = names2004[20:30]
upd305 = names2005[20:30]
upd306 = names2006[20:30]
upd307 = names2007[20:30]
upd308 = names2008[20:30]

p13 = pd.concat([upd304, upd305], ignore_index = True)
p23 = pd.concat([p13, upd306], ignore_index = True)
p33 = pd.concat([p23, upd307], ignore_index = True)
plot3 = pd.concat([p33, upd308], ignore_index = True)

plot3f = plot3.sort_values(['states', 'year'], ascending = True)
plot3f = plot3f.reset_index()

## plot 4 4th batch of 10
upd404 = names2004[30:40]
upd405 = names2005[30:40]
upd406 = names2006[30:40]
upd407 = names2007[30:40]
upd408 = names2008[30:40]

p14 = pd.concat([upd404, upd405], ignore_index = True)
p24 = pd.concat([p14, upd406], ignore_index = True)
p34 = pd.concat([p24, upd407], ignore_index = True)
plot4 = pd.concat([p34, upd408], ignore_index = True)

plot4f = plot4.sort_values(['states', 'year'], ascending = True)
plot4f = plot4f.reset_index()

## plot 5 5th batch of 10
upd504 = names2004[40:52]
upd505 = names2005[40:52]
upd506 = names2006[40:52]
upd507 = names2007[40:52]
upd508 = names2008[40:52]

p15 = pd.concat([upd504, upd505], ignore_index = True)
p25 = pd.concat([p15, upd506], ignore_index = True)
p35 = pd.concat([p25, upd507], ignore_index = True)
plot5 = pd.concat([p35, upd508], ignore_index = True)

plot5f = plot5.sort_values(['states', 'year'], ascending = True)
plot5f = plot5f.reset_index()

# set up for plot
fig, ax = plt.subplots(3, 2, figsize = (15, 20))
ax[2][1].set_visible(False)

# duplicate of first 10 states DO NOT EVER TOUCH THIS
ax[0][0].plot(plot1f['year'][0:5, ], plot1f['total_trips'][0:5, ], color = 'red', label = 'AK')
ax[0][0].plot(plot1f['year'][5:10, ], plot1f['total_trips'][5:10, ], '--', label = 'AL')
ax[0][0].plot(plot1f['year'][10:15, ], plot1f['total_trips'][10:15, ],  color = 'blue', label = 'AR')
ax[0][0].plot(plot1f['year'][15:20, ], plot1f['total_trips'][15:20, ], '--k', label = 'AZ')
ax[0][0].plot(plot1f['year'][20:25, ], plot1f['total_trips'][20:25, ], color = 'green', label = 'CA')
ax[0][0].plot(plot1f['year'][25:30, ], plot1f['total_trips'][25:30, ], '^--c', label = 'CO')
ax[0][0].plot(plot1f['year'][30:35, ], plot1f['total_trips'][30:35, ], color = 'black', label = 'CT')
ax[0][0].plot(plot1f['year'][35:40, ], plot1f['total_trips'][35:40, ], ':r', label = 'FL')
ax[0][0].plot(plot1f['year'][40:45, ], plot1f['total_trips'][40:45, ], color = 'magenta', label = 'GA')
ax[0][0].plot(plot2f['year'][45:50, ], plot2f['total_trips'][45:50, ], '-.', label = 'HI')

ax[0][0].legend()

ax[0][0].set_xticks(range(2004, 2009, 1))
ax[0][0].set_xlabel('Year')
ax[0][0].set_ylabel('Total trips per 1000')
ax[0][0].title.set_text('How flights to each state changed from 2004 to 2008')

# line plot for 2nd batch of 10 states
ax[0][1].plot(plot2f['year'][0:5, ], plot2f['total_trips'][0:5, ], color = 'red', label = 'IA')
ax[0][1].plot(plot2f['year'][5:10, ], plot2f['total_trips'][5:10, ],  '--', label = 'ID')
ax[0][1].plot(plot2f['year'][10:15, ], plot2f['total_trips'][10:15, ], color = 'blue', label = 'IL')
ax[0][1].plot(plot2f['year'][15:20, ], plot2f['total_trips'][15:20, ], '--k', label = 'IN')
ax[0][1].plot(plot2f['year'][20:25, ], plot2f['total_trips'][20:25, ], color = 'green', label = 'KS')
ax[0][1].plot(plot2f['year'][25:30, ], plot2f['total_trips'][25:30, ], '^--c', label = 'KY')
ax[0][1].plot(plot2f['year'][30:35, ], plot2f['total_trips'][30:35, ], color = 'black', label = 'LA')
ax[0][1].plot(plot2f['year'][35:40, ], plot2f['total_trips'][35:40, ], ':r', label = 'MA')
ax[0][1].plot(plot2f['year'][40:45, ], plot2f['total_trips'][40:45, ], color = 'magenta', label = 'MD')
ax[0][1].plot(plot3f['year'][45:50, ], plot3f['total_trips'][45:50, ], '-.', label = 'ME')

ax[0][1].legend()

ax[0][1].set_xticks(range(2004, 2009, 1))
ax[0][1].set_xlabel('Year')
ax[0][1].set_ylabel('Total trips per 1000')
ax[0][1].title.set_text('How flights to each state changed from 2004 to 2008')

# line plot for 3rd batch of 10 states
ax[1][0].plot(plot3f['year'][0:5, ], plot3f['total_trips'][0:5, ], color = 'red', label = 'MI')
ax[1][0].plot(plot3f['year'][5:10, ], plot3f['total_trips'][5:10, ], '--', label = 'MN')
ax[1][0].plot(plot3f['year'][10:15, ], plot3f['total_trips'][10:15, ], color = 'blue', label = 'MO')
ax[1][0].plot(plot3f['year'][15:20, ], plot3f['total_trips'][15:20, ], '--k', label = 'MS')
ax[1][0].plot(plot3f['year'][20:25, ], plot3f['total_trips'][20:25, ], color = 'green', label = 'MT')
ax[1][0].plot(plot3f['year'][25:30, ], plot3f['total_trips'][25:30, ], '^--c', label = 'NC')
ax[1][0].plot(plot3f['year'][30:35, ], plot3f['total_trips'][30:35, ], color = 'black', label = 'ND')
ax[1][0].plot(plot3f['year'][35:40, ], plot3f['total_trips'][35:40, ], ':r', label = 'NE')
ax[1][0].plot(plot3f['year'][40:45, ], plot3f['total_trips'][40:45, ], color = 'magenta', label = 'NH')
ax[1][0].plot(plot4f['year'][45:50, ], plot4f['total_trips'][45:50, ], '-.', label = 'NJ')
ax[1][0].legend()

ax[1][0].set_xticks(range(2004, 2009, 1))
ax[1][0].set_xlabel('Year')
ax[1][0].set_ylabel('Total trips per 1000')
ax[1][0].title.set_text('How flights to each state changed from 2004 to 2008')

# line plot for 4th batch of 10 states 
ax[1][1].plot(plot4f['year'][0:5, ], plot4f['total_trips'][0:5, ], color = 'red', label = 'NM')
ax[1][1].plot(plot4f['year'][5:10, ], plot4f['total_trips'][5:10, ],  '--', label = 'NV')
ax[1][1].plot(plot4f['year'][10:15, ], plot4f['total_trips'][10:15, ], color = 'blue', label = 'NY')
ax[1][1].plot(plot4f['year'][15:20, ], plot4f['total_trips'][15:20, ], '--k', label = 'OH')
ax[1][1].plot(plot4f['year'][20:25, ], plot4f['total_trips'][20:25, ], color = 'green', label = 'OK')
ax[1][1].plot(plot4f['year'][25:30, ], plot4f['total_trips'][25:30, ], '^--c', label = 'OR')
ax[1][1].plot(plot4f['year'][30:35, ], plot4f['total_trips'][30:35, ], color = 'black', label = 'PA')
ax[1][1].plot(plot4f['year'][35:40, ], plot4f['total_trips'][35:40, ], ':r', label = 'PR')
ax[1][1].plot(plot4f['year'][40:45, ], plot4f['total_trips'][40:45, ], color = 'magenta', label = 'RI')
ax[1][1].plot(plot5f['year'][45:50, ], plot5f['total_trips'][45:50, ], '-.', label = 'SC')

ax[1][1].legend(loc = 'upper right')

ax[1][1].set_xticks(range(2004, 2009, 1))
ax[1][1].set_xlabel('Year')
ax[1][1].set_ylabel('Total trips per 1000')
ax[1][1].title.set_text('How flights to each state changed from 2004 to 2008')

# line plot for 2nd batch of 10 states (remove TX from the graph to have a better comparison of other states in this batch)
ax[2][0].plot(plot5f['year'][0:5, ], plot5f['total_trips'][0:5, ], color = 'red', label = 'SD')
ax[2][0].plot(plot5f['year'][5:10, ], plot5f['total_trips'][5:10, ],  '--', label = 'TN')
# ax[2][0].plot(plot5f['year'][10:15, ], plot5f['total_trips'][10:15, ], color = 'blue', label = 'TX')
ax[2][0].plot(plot5f['year'][15:20, ], plot5f['total_trips'][15:20, ], '--k', label = 'UT')
ax[2][0].plot(plot5f['year'][20:25, ], plot5f['total_trips'][20:25, ], color = 'green', label = 'VA')
ax[2][0].plot(plot5f['year'][25:30, ], plot5f['total_trips'][25:30, ], '^--c', label = 'VI')
ax[2][0].plot(plot5f['year'][30:35, ], plot5f['total_trips'][30:35, ], color = 'black', label = 'VT')
ax[2][0].plot(plot5f['year'][35:40, ], plot5f['total_trips'][35:40, ], ':r', label = 'WA')
ax[2][0].plot(plot5f['year'][40:45, ], plot5f['total_trips'][40:45, ], color = 'magenta', label = 'WI')
ax[2][0].plot(plot5f['year'][45:50, ], plot5f['total_trips'][45:50, ], '-.', label = 'WV')
ax[2][0].plot(plot5f['year'][55:60, ], plot5f['total_trips'][55:60, ], color = 'yellow', label = 'WY')
ax[2][0].legend()

ax[2][0].set_xticks(range(2004, 2009, 1))
ax[2][0].set_xlabel('Year')
ax[2][0].set_ylabel('Total trips per 1000')
ax[2][0].title.set_text('How flights to each state changed from 2004 to 2008')
plt.show()

# ---------------------- QUESTION FOUR ---------------------------
# Can you detect cascading failures as delays in one airport create delays in others?  

# most number of flights out of the 5 years (2007)
most_flights = c.execute('''
                         SELECT Year as year, COUNT(*) as total_flights
                         FROM ontime
                         GROUP BY year
                         ORDER BY total_flights DESC
                         ''').fetchall()
                         
most_flightsdf = pd.DataFrame(most_flights, columns = ['year', 'total_flights'])

# getting edges to create Network visualisation
relation = c.execute('''
                     SELECT Origin as origin, Dest as destination, COUNT(ArrDelay)/100 as delayed_arrflights
                     FROM ontime
                     WHERE year = 2007 AND ArrDelay > 0
                     GROUP BY origin, destination
                     HAVING delayed_arrflights >= 15
                     ''').fetchall()

relationdf = pd.DataFrame(relation, columns = ['origin', 'destination', 'delayed_arrflights'])
          
## creation of network visualisation
G = nx.Graph()
G.clear()

for index, row in relationdf.iterrows():
   G.add_edge(row['origin'], row['destination'], weight = row['delayed_arrflights'])

# removal of isolated vertices if any
remove = [node for node,degree in G.degree() if degree ==0]
G.remove_nodes_from(remove)

G.number_of_nodes()
G.number_of_edges()

# setting size and colors
options = {
   'node_color': 'orange',
   'edge_color': 'lightblue',
   'node_size': 4,
   'width': 0.7,
   'alpha': 1.0,
   }

# producing the network
plt.subplots(figsize = (10,10))
pos = nx.circular_layout(G)
nx.draw(G, pos = pos, font_size = 9, **options, with_labels = True)
nx.draw_networkx_labels(G, pos = pos, font_size = 9, **options)
plt.tight_layout()
plt.axis('off')
plt.show()

# since ATL could be visibly seen with a high concentration of inbound flights, we will focus on ATL schedules
## for python

# finding out the origin to look at for flights going to ATL (BGR)
delays_to_ATL = c.execute('''
                          SELECT Dest as destination, Origin as origin, ROUND(AVG(DepDelay), 2) as avg_delay
                          FROM ontime
                          WHERE destination = 'ATL'
                          GROUP BY destination, origin
                          ORDER BY avg_delay DESC
                          ''').fetchall()
                          
delays_to_ATLdf = pd.DataFrame(delays_to_ATL, columns = ['destination', 'origin', 'avg_delay'])

# schedules
departure_delays_from_BGR = c.execute('''
                                      SELECT Origin as origin, Dest as destination, CRSDepTime, Deptime, CRSArrTime, ArrTime, DepDelay
                                      FROM ontime
                                      WHERE origin = 'BGR'
                                      GROUP BY destination, origin
                                      ORDER BY CRSDepTime
                                      ''').fetchall()
                                      
departure_delays_from_BGRdf = pd.DataFrame(departure_delays_from_BGR, columns = ['origin', 'destination', 'CRSDepTime', 'Deptime', 'CRSArrTime', 'ArrTime', 'DepDelay'])

departure_delays_from_ATL = c.execute('''
                                      SELECT Origin as origin, Dest as destination, CRSDepTime, DepTime, DepDelay
                                      FROM ontime
                                      WHERE origin = 'ATL' AND CRSDepTime >= 1840 AND DepDelay > 0
                                      GROUP BY destination
                                      ORDER BY CRSDepTime
                                      ''').fetchall()
                                      
departure_delays_from_ATLdf = pd.DataFrame(departure_delays_from_ATL, columns = ['origin', 'destination', 'CRSDepTime', 'Deptime', 'DepDelay'])

# ---------------------- QUESTION FIVE ---------------------------
# Use the available variables to construct a model that predicts delays.

# import libraries
from sklearn.model_selection import train_test_split, GridSearchCV      
from sklearn.ensemble import RandomForestClassifier  # added classification model
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer #transform different types

# first 5 origin with the highest average departure delay
origins = c.execute('''
                    SELECT Origin as origin, ROUND(AVG(DepDelay), 2) as avg_delay
                    FROM ontime
                    WHERE year = 2007 AND DepDelay > 0
                    GROUP BY origin
                    ORDER BY avg_delay DESC
                    LIMIT 5
                    ''').fetchall()

originsdf = pd.DataFrame(origins, columns = ['origin', 'avg_delay'])

# loading data
data = pd.read_csv("2007.csv")
nameoforigins = ['CMX', 'ACK', 'ALO', 'SCE', 'MCN']
ndata = data[data.Origin.isin(nameoforigins)]

ndata.isnull().sum()
ndata = ndata.dropna(subset=['DepDelay'])
print(ndata.shape)

features = ['DayOfWeek', 'UniqueCarrier', 'Origin', 'Dest', 'CRSDepTime']
X = ndata[features]
y = ndata['DepDelay']


numerical_features = ['CRSDepTime', 'DayOfWeek']

# Applying SimpleImputer and StandardScaler into a pipeline
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler())])

categorical_features = ['Dest', 'Origin', 'UniqueCarrier']

# Applying SimpleImputer and then OneHotEncoder into another pipeline
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer()),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

data_transformer = ColumnTransformer(
    transformers=[
        ('numerical', numerical_transformer, numerical_features),
        ('categorical', categorical_transformer, categorical_features)])

# creating train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

# setting parameters
param_grid = {
    'data_transformer__numerical__imputer__strategy': ['mean', 'median', 'most_frequent'],
    'data_transformer__categorical__imputer__strategy': ['constant','most_frequent']
}

# Random forest
pipe_rf = Pipeline(steps=[('data_transformer', data_transformer),
                           ('pipe_rf', RandomForestClassifier(random_state=2))])

grid_rf = GridSearchCV(pipe_rf, param_grid=param_grid)
grid_rf.fit(X_train, y_train);

print(grid_rf.best_score_)
print(grid_rf.best_params_)

y_predict_rf = grid_rf.predict(X_test)

sns.regplot(x=y_predict_rf, y=y_test, color = 'green', marker = "D")
plt.xlabel("Predicted Delay")
plt.ylabel("Actual Delay")
plt.title("Random Forest Model")
plt.show()





















