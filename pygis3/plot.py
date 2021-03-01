import os
import pandas as pd
import matplotlib.pyplot as plt

def readFile(filename):


    with open(filename) as f:
        x = []
        y = []
        for line in f:
            a = line.split()
            #print(a)
            x.append(float(a[0]))
            y.append(float(a[1]))

    return x, y

def plotProfiles():
    """
    """

    curr_dir_name = os.getcwd()
    #dirNames = [x[0] for x in os.walk(path)]
    base_filename = "P_01_014400"
    filename_suffix = "TXT"
    fig, ax = plt.subplots()
    i = 0
    for dir_name in [x[0] for x in os.walk(curr_dir_name)]:
        filename = os.path.join(dir_name, base_filename + "." + filename_suffix)
        if os.path.isfile(filename):

            #df = pd.read_csv(filename, sep="\t", header=None)
            x ,y = readFile(filename)
            print(x[0],y[0], i)
            #print(df.head())
            #ax.plot(x, y, color='green')
            ax.plot(x, y, color=plt.cm.cool(i))
            #print(len(df.columns))
            #print(df[0,])
            print(filename)
            i += 1

    ax.grid()
    ax.set_xlabel('Chainage (m)')
    ax.set_ylabel('Elevation (m a.s.l.)')
    #ax.set_title('f(x) = x * x')
    plt.show()
        #files = os.listdir(dirName)
        #for file in os.listdir(dirName):
        #    if file.endswith(".TXT"):
        #        print(dirName)
    #print(dirNames)


if __name__ == "__main__":
    plotProfiles()
