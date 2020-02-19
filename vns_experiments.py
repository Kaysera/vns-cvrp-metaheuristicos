from vns_cvrp import general_VNS_small, general_VNS_big, general_VNS_mid
from random import seed
from statistics import mean, median


def run_experiment(function, path, k_max, capacity, samples):
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

        capacity: int
            Capacidad maxima de los camiones

        samples: int
            Numero de veces que se va a ejecutar el algoritmo
    '''
    results = []
    for i in range(0,samples):
        print(f'Experiment {i}')
        seed(i)
        results.append(function(path, k_max, CAPACITY, verbose=0))

    print(f'Mean: {mean(results)}, median: {median(results)}, best: {min(results)}')
    with(open('results.csv', 'a+')) as file:
        file.write(';'.join([function.__name__, path.split('/')[2], str(mean(results)), str(median(results)), str(min(results)), '\n']))




k_max = 50
path = './instances/A-n32-k5.vrp'
CAPACITY = 300
samples = 30

run_experiment(general_VNS_small, path, k_max, CAPACITY, samples)
run_experiment(general_VNS_mid, path, k_max, CAPACITY, samples)
run_experiment(general_VNS_big, path, k_max, CAPACITY, samples)