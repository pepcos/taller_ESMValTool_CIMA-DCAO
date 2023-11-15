library(yaml)
library(ncdf4)
library(RColorBrewer)
library(ggplot2)

################################################################################
#Load ESMValTool stuff
args <- commandArgs(trailingOnly = TRUE)
params <- read_yaml(args[1])

# define the directories
plot_dir <- params$plot_dir
run_dir <- params$run_dir
work_dir <- params$work_dir
dir.create(run_dir, recursive = TRUE)
dir.create(plot_dir, recursive = TRUE)
dir.create(work_dir, recursive = TRUE)

for (i in 1:length(params$input_files)){
  metadata1 <- read_yaml(params$input_files[i])
  for(j in 1:length(metadata1)){
    nc <- nc_open(metadata1[[j]]$filename)
    gcm <- metadata1[[j]]$dataset
    var_group <- metadata1[[j]]$variable_group
    print(paste("NetCDF of dataset", gcm, "in variable group", var_group, ":"))
    print(nc)
  }
}