import gzip
import os
#os.chdir(r"E:\Red_deer_SPARROW\Fluxmaster\Flow")
filepath = r"E:\Red_deer_SPARROW\Fluxmaster\Flow"
filepath = r"E:\WaterQualityData\NutrientSaskRivPaper_Analysi\Fluxmaster\Flow"
filepath = r"E:\SouthSaskRiv_SPARROW\Fluxmaster\Fluxmaster_TP\Flow"
for files in os.listdir(filepath):
    if files.endswith(".rdb"):
        print files
        dummy = filepath + "\\" + files
        f_in = open(dummy, 'rb')
        dummy = filepath + "\\" + files + ".gz"
        f_out = gzip.open(dummy, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
