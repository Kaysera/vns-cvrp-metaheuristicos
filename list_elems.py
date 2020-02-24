
from os import listdir
from os.path import isfile, join
mypath = './instances'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
with open('commands.txt', 'w') as file: 
    for f in onlyfiles:
        file.write(f'py vns_experiments.py {mypath}/{f}\n')