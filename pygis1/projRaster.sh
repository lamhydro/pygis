#!/bin/bash

#./projRaster.sh /media/Data3/saskRiverDeltaModel/data/gis/srtm_16_02/clipped_srtm_16_02.tif EPSG:26910


echo 'Input raster file = ' $1
echo 'Projection = ' $2

dir=$(dirname "$1")
#echo "${dir}"
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"

outputRaster=${dir}/${filename}_prj.$extension
#echo ${outputRaster}

gdalwarp -t_srs $2 $1 $outputRaster

