library(yaml)
library(ncdf4)
library(RColorBrewer)
library(ggplot2)

#Directory information
setwd("/esarchive/scratch/molmo/")
OUTPUTS <- "/esarchive/scratch/molmo/output/"

#Useful functions
png.save <- function(x,filename,main,xlab,ylab){
  png(filename = paste(filename,".png",sep=""))
  plot(x,type="o",main=main,xlab = xlab,ylab=ylab)
  dev.off()
}
################################################################################
#Load ESMValTool stuff
args <- commandArgs(trailingOnly = TRUE)
#params <- read_yaml(args[1])
setwd("/esarchive/scratch/molmo/output/")
params <- read_yaml(paste(list.dirs(recursive = F)[length(list.dirs(recursive = F))],"/run/diagnostic_1/script1/settings.yml",sep=""))

plot_dir <- params$plot_dir
run_dir <- params$run_dir
work_dir <- params$work_dir

# Create working dirs if they do not exist
dir.create(plot_dir, recursive = TRUE)
dir.create(run_dir, recursive = TRUE)
dir.create(work_dir, recursive = TRUE)

metadata1 <- read_yaml(params$input_files[1])

for(mod in 1:length(metadata1)){
nc <- nc_open(metadata1[[mod]]$filename)
gcm <- metadata1[[mod]]$dataset

################################################################################
#Load SLP data
message("Loading and preprocessing data...")
nc_lon <- ncvar_get(nc,"lon")
nc_lat <- ncvar_get(nc,"lat")
nc_var <- ncvar_get(nc,"unknown") #x,y,time

