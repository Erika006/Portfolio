# to open library
library(DBI)
library(dplyr)
library(ggplot2)
library(igraph)
library(RColorBrewer)
colours12 <- brewer.pal(n = 12, name = 'Paired')
memory.limit(size=56000)

setwd("C:\\Users\\Admin\\Documents\\SIM Coursework Final\\Assignment 3 practice\\Data Expo 2009")
getwd()

# if (file.exists("airline_r.db")) 
#   file.remove("airline_r.db")

conn <- dbConnect(RSQLite::SQLite(), "airline_r.db")

# airports <- read.csv("airports.csv", header = TRUE)
# carriers <- read.csv("carriers.csv", header = TRUE)
# planes <- read.csv("plane-data.csv", header = TRUE)
# dbWriteTable(conn, "airports", airports)
# dbWriteTable(conn, "carriers", carriers)
# dbWriteTable(conn, "planes", planes)

# to append the years together
## ontime4 <- read.csv("2004.csv", header = TRUE)
## ontime5 <- read.csv("2005.csv", header = TRUE)
## ontime6 <- read.csv("2006.csv", header = TRUE)
## ontime7 <- read.csv("2007.csv", header = TRUE)
## ontime8 <- read.csv("2008.csv", header = TRUE)

# chose the variable ontime_all so that i wont be confused with other variable names later on
# piping function was used via opening the dplyr library for efficient appending of the csv files.
## ontime_all <- ontime4 %>%
##  rbind(ontime5) %>%
##  rbind(ontime6) %>%
##  rbind(ontime7) %>%
##  rbind(ontime8) 

## dbWriteTable(conn, "ontime", ontime_all)

# remove tables
## rm(ontime4, ontime5, ontime6, ontime7, ontime8)

#---------- this area is to ensure that all data have been appended correctly into the database -----
#reads what is in the table
## dbReadTable(conn, "ontime")

# shows the tables in database 
dbListTables(conn)

# shows the attributes in "airports"
dbListFields(conn, "airports")
dbListFields(conn, "carriers")
dbListFields(conn, "planes")
dbListFields(conn, "ontime")

# also used db browser to ensure that the tables are alright as well as to allow me to have easier reference to the
## database if need be.

#-------------- QUESTION ONE ------------------
# 1. When is the best time of day, day of the week, and time of year to fly to minimize delays?
best_time_of_day <- dbGetQuery(conn, "
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
END AS time,
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
")

best_time_of_day

# to check if the table makes sense
is.data.frame(best_time_of_day)

#plot graph
ggplot(best_time_of_day, aes(x = time, y = avg_delay)) +
  geom_bar(fill = colours12 , stat = "identity") +
  ggtitle("Best time of day") +
  xlab("Time") +
  ylab("Average Delay") +
  geom_text(aes(label= avg_delay,
                size = 2,
                vjust = 1.5))

best_day_of_week <- dbGetQuery(conn, "
                               SELECT DayofWeek as day, round(AVG(DepDelay), 3) as avg_delay
                               FROM ontime
                               GROUP BY day
                               ORDER BY avg_delay
                               ")

# to check if the table makes sense
best_day_of_week

#plot graph
colours7 <- brewer.pal(n = 7, name = 'Paired')
ggplot(best_day_of_week, aes(x = day, y = avg_delay)) +
  geom_bar(fill = colours7, stat= "identity") +
  scale_x_continuous(breaks = seq(1, 7, by = 1)) +
  ggtitle("Best day of the week") +
  xlab("Day") +
  ylab("Average Delay") +
  geom_text(aes(label= avg_delay,
            size = 2,
            vjust = -0.5))

best_time_of_year <- dbGetQuery(conn, "
                                SELECT Month as month, round(avg(DepDelay), 3) as avg_delay
                                FROM ontime
                                GROUP BY month
                                ORDER BY avg_delay
                                ")

best_time_of_year

ggplot(best_time_of_year, aes(x = month, y = avg_delay)) +
  geom_bar(fill = colours12, stat= "identity") +
  ggtitle("Best time of year") +
  xlab("Month") +
  ylab("Average Delay") +
  scale_x_continuous(breaks = seq(1, 12, by = 1)) +
  geom_text(aes(label= avg_delay,
                size = 3,
                vjust = -0.5,
                ))

#-------------- QUESTION TWO ------------------
# 2. Do older planes suffer more delays?
# probably group by year?

# to check the manufacturing years they have for easier outlook of which years are considered old
years_manufactured <- dbGetQuery(conn, "
                                 SELECT DISTINCT year
                                 FROM planes
                                 ORDER BY year
                                 ")

# finding the median, any year later than that is considered as an older planes (assumption)
# those above this year are considered latest planes
median(years_manufactured$year)


older_planes <- dbGetQuery(conn, "
                           SELECT planes.year as planes_year, AVG(ontime.DepDelay) as avg_delay
                           FROM planes JOIN ontime USING (tailnum)
                           WHERE planes.year < 1983
                           GROUP BY planes_year
                           ORDER BY planes_year
                           ")

older_planes

# removing these two rows as the years are invalid or empty. doing so by filling the row with NA first then removing
older_planes[c(1,2),] <- NA

# removing na using na.omit(), table looks cleaner
older_planes <- na.omit(older_planes)



# this table is for newer models so that we can compare with the older models average
newer_planes <- dbGetQuery(conn, "
                           SELECT planes.year as planes_year, AVG(ontime.DepDelay) as avg_delay
                           FROM planes JOIN ontime USING (tailnum)
                           WHERE planes.year >= 1983
                           GROUP BY planes_year
                           ORDER BY planes_year
                           ")

newer_planes

# removing this row as the year is invalid. doing so by filling the row with NA first then removing
newer_planes[27,] <- NA

# removing na using na.omit(), table looks cleaner
newer_planes <- na.omit(newer_planes)

# graph
planes <- rbind(older_planes, newer_planes)

colours<-brewer.pal(n = 12, name = "Paired")

plot(planes$planes_year, planes$avg_delay, type = "l",
     col=colours[2], xlab = 'Manufactured Year', ylab = 'Average Delay', main = 'Average Delay for both older and newer planes')

# to calculate average of total delays for both planes
mean_delay_for_older_planes <- round(mean(older_planes$avg_delay, na.rm = TRUE), 2)
mean_delay_for_newer_planes <- round(mean(newer_planes$avg_delay, na.rm = TRUE), 2)

# string the answers to form a nice sentence
print(paste("Since the average delay of the older and newer planes are", mean_delay_for_older_planes, "and", mean_delay_for_newer_planes, "respectively, this shows that older planes does not suffer more delays compared to the newer ones"))

#-------------- QUESTION THREE ------------------
# 3. How does the number of people flying between different locations change over time?
# assuming the number of trips = more people in that flight to that from a particular origin
in2004 <- dbGetQuery(conn, "
                      SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000 as total_trips
                      FROM ontime JOIN airports ON ontime.dest = airports.iata
                      WHERE year = 2004
                      GROUP BY states
                      ORDER BY year
                      ");

in2005 <- dbGetQuery(conn, "
                      SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000 as total_trips
                      FROM ontime JOIN airports ON ontime.dest = airports.iata
                      WHERE year = 2005
                      GROUP BY states
                      ORDER BY year
                      ");

in2006 <- dbGetQuery(conn, "
                      SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000 as total_trips
                      FROM ontime JOIN airports ON ontime.dest = airports.iata
                      WHERE year = 2006
                      GROUP BY states
                      ORDER BY year
                      ");

in2007 <- dbGetQuery(conn, "
                      SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000 as total_trips
                      FROM ontime JOIN airports ON ontime.dest = airports.iata
                      WHERE year = 2007
                      GROUP BY states
                      ORDER BY year
                      ");

in2008 <- dbGetQuery(conn, "
                      SELECT ontime.Year as year, airports.state as states, COUNT(*)/1000 as total_trips
                      FROM ontime JOIN airports ON ontime.dest = airports.iata
                      WHERE year = 2008 
                      GROUP BY states
                      ORDER BY year
                      ");

# remove NA values as there were 12 unknowns in the database with NULL state
upd2004 <- na.omit(in2004)
upd2005 <- na.omit(in2005)
upd2006 <- na.omit(in2006)
upd2007 <- na.omit(in2007)
upd2008 <- na.omit(in2008)

# in 2006 and 2007 there were trips to the state of DE but other years did no, so i removed it for better comparison
upd2006 <- upd2006[-c(9),]
upd2007 <- upd2007[-c(9),]

# putting all my data frames together
overallchanges <- rbind(upd2004, upd2005, upd2006, upd2007, upd2008)

# create multiple bar plot using ax method
ggplot(overallchanges, aes(x = states, y = total_trips, fill = as.factor(year))) +
  geom_bar(position = "dodge", stat="identity", alpha = 0.8) +
  ggtitle("Flights between states from 2004 to 2008") +
  xlab("States") +
  ylab("Total trips per 1000") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

#-------------- QUESTION FOUR ------------------
# Can you detect cascading failures as delays in one airport create delays in others?

# check which year had the most number of flights (2007)
each_year <- dbGetQuery(conn, "
                        SELECT Year as year, COUNT(*) as total_flights
                        FROM ontime
                        GROUP BY year
                        ORDER BY total_flights DESC
                        ")

# filtered and clean the data so that we focus on the relevant airports for better comparison (EDGES)
relation <- dbGetQuery(conn, "
                       SELECT Origin as origin, Dest as destination, COUNT(ArrDelay)/100 as delayed_arrflights
                       FROM ontime
                       WHERE year = 2007 AND ArrDelay > 0
                       GROUP BY origin, destination
                       HAVING delayed_arrflights >= 15
                       ")

# average delay in each airport from above relation (NODES)
delay <- dbGetQuery(conn, "
                    SELECT Origin as origin, round(avg(DepDelay), 2) as avg_depdelay
                    FROM ontime JOIN airports ON ontime.dest = airports.iata
                    WHERE Year = 2007 AND DepDelay > 0
                    GROUP BY origin
                    ")

## creating network visualization

# finding out which edges are not in my nodes list
relation[which(! relation$origin %in% delay$origin),]
relation[which(! relation$destination %in% delay$origin),]

# testing out the graphical layout
net <- graph_from_data_frame(d = relation, vertices = delay, directed = T)
net.new <- delete.vertices(net , which(degree(net)==0))

summary(delay)

circle <- layout_in_circle(net.new)
plot(net.new, edge.arrow.size = 0.1, vertex.size = 9,
     edge.width = 1.5,
     vertex.label.cex = 0.7, vertex.label.size = 0.1, 
     vertex.color = ifelse(delay$avg_depdelay>45, "red", "orange"), vertex.frame.color = "black", 
     layout = circle)

# yes there will always be cascading delays between one airport and another. From the network graph shown, all the airports
## are link to one another where there is a huge number of delayed arrival flights due to average departure delays in the origin airport the flight was
### coming from. This will then cause a snowball effect where other flights will start to have delay as well since they are not able
#### take off on time.

# From the Network display we can also see the concentration of the most delayed flights to a certain destination. The top 5 would be
## ORD, ATL, DCA, DFW and DEN. We will look further into one of these airports for arrival and look at some of the departure timings some flights at the
### origin airport to show proof of cascading delays.

# to find out which origin we will look at, find the avg dep delay for all origin's to DFW (MLB)
delays_to_DFW <- dbGetQuery(conn, "
                            SELECT Dest as destination, Origin as origin, ROUND(AVG(DepDelay), 2) as avg_delay
                            FROM ontime
                            WHERE destination = 'DFW'
                            GROUP BY destination, origin
                            ORDER BY avg_delay DESC
                            ")

# schedule flights from both ends
departure_delays_from_MLB <- dbGetQuery(conn, "
                             SELECT Origin as origin, Dest as destination, CRSDepTime, Deptime, CRSArrTime, ArrTime, DepDelay
                             FROM ontime
                             WHERE origin = 'MLB'
                             GROUP BY destination, origin
                             ORDER BY CRSDepTime
                             ")

departure_delays_from_DFW <- dbGetQuery(conn, "
                             SELECT Origin as origin, Dest as destination, CRSDepTime, DepTime, DepDelay
                             FROM ontime
                             WHERE origin = 'DFW' AND CRSDepTime >= 2152 AND DepDelay > 0
                             GROUP BY destination
                             ORDER BY CRSDepTime
                             ")

#-------------- QUESTION FIVE ------------------
# Use the available variables to construct a model that predicts delays.
# focusing on 2007
library(mlr3)
library(mlr3learners)
library(mlr3pipelines)
library(mlr3tuning)
library(mlr3viz)

# to see which delay to be used (DepDelay)
avg_delay <- dbGetQuery(conn, "
                        SELECT Year as year, ROUND(AVG(DepDelay), 2) as avg_depdelay, ROUND(AVG(ArrDelay), 2) as avg_arrdelay
                        FROM ontime
                        WHERE year = 2007
                        ")

# which FIRST 5 origin to use (CMX)
origin <- dbGetQuery(conn, "
                     SELECT Origin as origin, ROUND(AVG(DepDelay), 2) as avg_delay
                     FROM ontime
                     WHERE year = 2007 AND DepDelay > 0
                     GROUP BY origin
                     ORDER BY avg_delay DESC
                     LIMIT 5")

# loading data
data <- dbGetQuery(conn, "
                   SELECT *
                   FROM ontime
                   WHERE year = 2007 AND DepDelay > 0
                   ")

ndata <- filter(data, Origin == "CMX" | Origin == "ACK" | Origin == "ALO" | Origin == "SCE" | Origin == "MCN")

ndata$Origin <- factor(ndata$Origin)
ndata$Dest <- factor(ndata$Dest)
ndata$TailNum <- factor(ndata$TailNum)

# getting training and test sets
n <- nrow(ndata)
set.seed(10)
train_set <- sample(n, round(0.6 * n))
test_set <- setdiff(1:n, train_set)

# setting up task
task <- TaskRegr$new('delay', backend = ndata, target = 'DepDelay')
task$select(c('CRSDepTime', 'DepTime', 'Dest', 'Origin', 'TailNum'))
task

measure <- msr('regr.mse')

# Some variables are factors for which some methods do not support
# Hence, we need to convert them to numerical values 

fencoder <- po("encode", method="treatment",
               affect_columns=selector_type("factor"))

# Some methods require tuning the hyperparameters, and we will later use the following:
tuner <- tnr('grid_search')
terminator <- trm('evals', n_evals = 20)

# Extend result with different classifiers

#################
# Random Forest 
#################

learner_rf <- lrn('regr.ranger')
learner_rf$param_set$values <- list(min.node.size = 4)
gr_rf <- po('scale') %>>%
  po('imputemean') %>>%
  po(learner_rf)
glrn_rf <- GraphLearner$new(gr_rf)
tune_ntrees <- ParamSet$new (list(
  ParamInt$new('regr.ranger.num.trees', lower = 50, upper = 600)
))
at_rf <- AutoTuner$new(
  learner = glrn_rf,
  resampling = rsmp('cv', folds = 3),
  measure = measure,
  search_space = tune_ntrees,
  terminator = terminator,
  tuner = tuner
)
at_rf$train(task, row_ids = train_set)
at_rf$predict(task, row_ids = test_set)$score()

##########################
# Support Vector Machine
##########################

learner_svm <- lrn("regr.svm")

gr_svm <- po('imputemean', affect_columns=selector_type("numeric")) %>>%
  po('imputemode', affect_columns=selector_type(c("factor"))) %>>%
  fencoder %>>%
  po('scale') %>>%
  po(learner_svm)

glrn_svm <- GraphLearner$new(gr_svm)

glrn_svm$train(task, row_ids = train_set)
glrn_svm$predict(task, row_ids = test_set)$score() 

# benchmarking the best model
set.seed(1)

lrn_list <- list(
  at_rf,
  glrn_svm
)

# Set the benchmark design and run the comparisons
bm_design <- benchmark_grid(task=task, resamplings=rsmp('cv', folds=3), 
                            learners=lrn_list)
bmr <- benchmark(bm_design, store_models=TRUE)

# Visualise comparisons with boxplots
autoplot(bmr) + theme(axis.text.x = element_text(angle = 45, hjust = 1))
