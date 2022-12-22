#!/bin/bash
#SBATCH --time=9-24:00:00
#SBATCH --partition=aics_cpu_general
#SBATCH --mem=12G

# activate Conda
. /allen/aics/apps/prod/anaconda/Anaconda3-5.1.0/bin/activate

# activate Ilastik conda environment
conda activate /allen/aics/apps/prod/venvs/cellprofiler/v4.1.3

# run Ilastik
/allen/aics/apps/prod/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh --headless --project="/allen/aics/microscopy/CellProfiler_4.1.3_Testing/96wellPipeline_v2/96_well_colony_celigo_v2.ilp" --output_format=tiff --export_source="Probabilities" --output_filename_format='/allen/aics/microscopy/brian_whitney/temp_output/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um_rescale_probabilities.tiff' '/allen/aics/microscopy/brian_whitney/temp_output/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um/3500005266_Scan_11-30-2022-8-50-15-AM_Well_G11_Ch1_-1um_rescale.tiff'

# need to remove refrences to things on the isilon. Currently cannot import these with package.