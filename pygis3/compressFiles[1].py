import gzip
import os
#os.chdir(r"C:\SPARROW\Qu'Appelle River Load est\1. Moose Jaw\Fluxmaster_TN\Flow")
filepath = r"C:\SPARROW\Qu'Appelle River Load est\1. Moose Jaw\Fluxmaster_TN\Flow"
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
