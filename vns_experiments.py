from vns_cvrp import general_VNS_small, general_VNS_big, general_VNS_mid
from random import seed
from statistics import mean, median
from datetime import datetime
from sys import argv


def run_experiment(function, path, k_max, max_length, samples):
    '''
    Funcion que ejecuta un tipo de VNS sobre un fichero cambiando la semilla
    un determinado numero de veces

    Parameters
    ----------
        function: funcion
            Funcion VNS que se va a ejecutar

        path: string
            Ruta donde se encuentra el fichero de la instancia
        
        k_max: int
            Numero maximo de cambios de vecindario que se pueden realizar

        max_length: int
            Distancia maxima que recorren los camiones

        samples: int
            Numero de veces que se va a ejecutar el algoritmo
    '''
    results = []
    folder = './instances'
    print(f'Filename: {path}, VNS: {function.__name__}, timestamp: {datetime.now().strftime("%H:%M:%S")}')
    for i in range(0,samples):
        print(f'Experiment {i}')
        seed(i)
        results.append(function(f'{folder}/{path}', k_max, max_length, verbose=0))

    print(f'Mean: {mean(results)}, median: {median(results)}, best: {min(results)}')
    with(open(f'./results/{path.split(".")[0]}_results.csv', 'a+')) as file:
        file.write(';'.join([function.__name__, path, str(mean(results)), str(median(results)), str(min(results)), '\n']))




k_max = 50
max_distance = 300
samples = 30
mypath = './instances'
vns_variants = [general_VNS_small, general_VNS_mid, general_VNS_big]

if argv[1]:
    file = argv[1].split('\\')[2]
    for vns in vns_variants:
        run_experiment(vns, file, k_max, max_distance, samples)
else:
    print('No arguments were given')