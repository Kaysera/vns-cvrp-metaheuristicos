from os import listdir
from os.path import isfile, join

mypath = './results'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

with open('final_results.csv', 'w') as file:
    for f in onlyfiles:
        with open(f'{mypath}/{f}') as ff:
            file.writelines(ff.readlines())

