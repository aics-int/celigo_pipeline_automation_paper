#!/bin/bash
#SBATCH --time=9-24:00:00
#SBATCH --partition=aics_cpu_general
#SBATCH --mem=6G

# activate Conda
source /etc/profile.d/modules.sh
module load anaconda3
source activate

# activate cellprofiler conda environment
conda activate cellprofiler_v4.2.1

# run Resize with CellProfiler
cellprofiler -r -c -p /allen/aics/microscopy/brian_whitney/repos/celigo-pipeline-core/celigo_pipeline_core/pipelines/rescale_pipeline.cppipe --file-list /allen/aics/microscopy/brian_whitney/temp_output/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um/resize_filelist.txt -o /allen/aics/microscopy/brian_whitney/temp_output/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um

# need to remove refrences to things on the isilon. Currently cannot import these with package.