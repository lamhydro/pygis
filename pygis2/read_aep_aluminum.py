#!/usr/bin/env python

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def readCSVfile(filename):
    """
    Read .csv file
    """

    data = []
    with open(filename) as f:
        header = f.readline().strip().split(',')
        #print(header)
        for line in f:
#            print line
            a = line.strip().split(',')

            #if len(a) != 6:
            #    print(len(a))
            data.append(a)
            #print(a)

    # Converting to dataframe
    df = pd.DataFrame(data, columns=header, dtype=None)
    return(df)

def plotDF(df):
    """

    """
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
                width=4E6, height=4E6,
                lat_0=49, lon_0=-100,)
    m.etopo(scale=0.5, alpha=0.5)

    # Map (long, lat) to (x, y) for plotting
    x, y = m(list(df['longitude']), list(df['latitude']))
    plt.plot(x, y, 'ok', markersize=2)
    #plt.text(x, y, df['parameter'], fontsize=12)
    plt.show()



if __name__ == '__main__':

    path = '/media/watersec/Luis/forZac'
    os.chdir(path)

    filename = 'aep_aluminum_total_quarantine.csv'

    # First way to read the file
    #df = readCSVfile(filename)
    #print(df.head())

    # Second way to read the file (FASTER!!!!)
    df = pd.read_csv(filename, sep=",", dtype={'latitude':float, 'longitude':float, 'date':str, 'parameter':str, 'measurement':float, 'units_of_measure':str})

    # Convert West to negative
    df['longitude'] = df['longitude']*-1.

    print(df.head())

    plotDF(df)

    #print(df['longitude']+df['latitude'])
    #print(df.dtypes)

    # data_transposed = zip(data)
    # df = p
