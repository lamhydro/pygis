#!/bin/bash


echo 'Input raster file = ' $1
echo 'x_min = ' $2
echo 'y_min = ' $3
echo 'x_max = ' $4
echo 'y_max = ' $5

dir=$(dirname "$1")
echo "${dir}"
basen=$(basename "$1")
echo "${basen}"
outputRaster=${dir}/clipped_${basen}
echo ${outputRaster}

gdalwarp -te $2 $3 $4 $5 $1 $outputRaster
