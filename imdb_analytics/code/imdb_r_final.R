library(magrittr) # use %>%
library(dplyr) # use group_by function
library(tidyr) # use spread function
library(reshape2) # melt function
library(ggplot2) # plot correlation heatmap
library(caret) # apply linear regression

rating <- read.table('Documents/git_repos/data_science/imdb_analytics/res/title.ratings.tsv', sep = '\t', header = TRUE, quote = "")
# read ratings data
people <- read.table('Documents/git_repos/data_science/imdb_analytics/res/title.principals.tsv', sep = '\t', header = TRUE, quote = "", fill=TRUE)
# read all cast, director etc. data data
basics <- read.table('Documents/git_repos/data_science/imdb_analytics/res/title.basics.tsv', sep = '\t', header = TRUE, quote = "", fill=TRUE)
# read few basic data about the movie
basics <- basics[basics$startYear != "\\N",]
# remove rows with \\N as startYear
basics$startYear <- as.numeric(levels(basics$startYear))[basics$startYear]
# convert startYear column from factor to numeric
basics <- na.omit(basics)
# remove rows with NA values
basics_year_greater_2008 <- basics[basics$startYear >= 2008 & basics$startYear <= 2017, ]
# extract rows having start year >= 2008 and <= 2017
basics_type_movie_greater_2008 <- basics_year_greater_2008[basics_year_greater_2008$titleType == 'movie', ]
# extract rows having title type as movie
people <- subset(people, tconst %in% basics_type_movie_greater_2008$tconst)
# get all the people details of all the movies saved in variable basics_type_movie_greater_2008
people_cat <- people[,c(1,3,4)]
# extract movie code, person code adn person role from people variable
tmp <- people_cat %>% group_by(tconst,category) %>% arrange(nconst) %>% filter(row_number()==1)
# group by category and movie and extract only 1 row from each group
roles = spread(tmp,category,nconst)
# pivot the tmp variable to covert each category to column
roles = roles[,c(1,2,3,6,7,8,9,10,13)]
# extract columns that have large amount of data
analysis_df <- merge(roles, rating, by=c("tconst","tconst"))
# generate a new data frame that has people details and rating details for each movie
analysis_df <- na.omit(analysis_df)
# remove all rows with NA
analysis_df[,1:9] <- as.numeric(unlist(analysis_df[,1:9]))
# convert all factor columns to numeric
cormat <- round(cor(analysis_df[,2:11]),2)
# generate correlation matrix
melted_cormat <- melt(cormat)
ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + geom_tile()
# plot correlation heatmap
analysis_df = analysis_df[,2:11]
# remove movie ID column
train_control <- trainControl(method="cv", number=100)
# cross validation with 100 folds
linMod <- train(averageRating ~ .,data = analysis_df,trControl=train_control, "lm")
# apply Linear Regression
plot(analysis_df$numVotes,analysis_df$averageRating)
# scatter plot between number of votes and averageRating
runtime_analysis_df <- merge(roles, basics_type_movie_greater_2008[,c(1,8)], by=c("tconst","tconst"))
# generate a new data frame that has people details and runtime details for each movie
runtime_analysis_df <- runtime_analysis_df[,2:10]
# remove movie ID column
runtime_analysis_df <- runtime_analysis_df[runtime_analysis_df$runtimeMinutes != "\\N",]
# remove rows with \\N as runtimeMinutes
runtime_analysis_df$runtimeMinutes <- as.numeric(levels(runtime_analysis_df$runtimeMinutes))[runtime_analysis_df$runtimeMinutes]
# convert runtimeMinutes from factor to numeric with exact values
runtime_analysis_df[,1:8] <- as.numeric(unlist(runtime_analysis_df[,1:8]))
# convert all factor columns to numeric
runtime_analysis_df <- na.omit(runtime_analysis_df)
# remove rows with NA in any column
cormat_rm <- round(cor(runtime_analysis_df),2)
# create correlation matrix of new data frame
melted_cormat_rm <- melt(cormat_rm)
ggplot(data = melted_cormat_rm, aes(x=Var1, y=Var2, fill=value)) + geom_tile()
# plot new correlation heatmap
train_control_rm <- trainControl(method="cv", number=100)
train_control <- trainControl(method="cv", number=100)
# cross validation with 100 folds
linMod_rm <- train(runtimeMinutes ~ .,data = runtime_analysis_df, trControl=train_control_rm, "lm")
# apply Linear Regression