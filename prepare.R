setwd("~/code/bladder_coms")

data <- read.csv2('rad_seance.csv', colClasses = rep("character",4))
colnames(data) <- c("treatment", "date", "time", "comment")
data$id_date = paste(data$treatment, data$date)
#
data_dbl = duplicated(data$id_date) | duplicated(data$id_date, fromLast = TRUE)
#
data_duplicated_only = data[data_dbl, -5]
#
write.csv(data_duplicated_only, "ok_cols_start.csv", row.names=FALSE)