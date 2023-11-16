library(yaml)
library(ncdf4)
library(RColorBrewer)
library(ggplot2)
library(gridExtra)

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
  plots_list <- list()
  combined_plot <- ggplot()
  for(j in 1:length(metadata1)){
    nc <- nc_open(metadata1[[j]]$filename)
    gcm <- metadata1[[j]]$dataset
    var_group <- metadata1[[j]]$variable_group
    print(paste("NetCDF of dataset", gcm, "in variable group", var_group, ":"))
    print(nc)
    df <- data.frame(month=ncvar_get(nc,"month_number"), value = ncvar_get(nc, "tas"))
    combined_plot <- combined_plot + geom_line(data=df, aes(x = month, y = value)) 
  }
  combined_plot <- combined_plot  + labs(x="month",y="air_temperature/degC",title=metadata1[[j]]$caption)
  ggsave(paste0(plot_dir,"/var",i,metadata1[[j]]$savefig), plot = combined_plot, width = 8, height = 6, units = "in")
}
