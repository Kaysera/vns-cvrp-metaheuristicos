from random import shuffle, randint
from math import sqrt, pow, inf
from itertools import permutations, product
from copy import deepcopy

MAX_ATTEMPTS = 50


def distance(origin, dest):
    '''
    Funcion para calcular la distancia euclidea entre dos puntos

    Parameters
    ----------
        origin: dict
            Diccionario con las coordenadas x e y del origien

        dest: dict
            Diccionario con las coordenadas x e y del destino

    Returns
    -------
        distance: float
            Distancia euclidea entre los dos puntos en dos dimensiones

    '''
    return sqrt(pow((origin['x'] - dest['x']), 2) + pow((origin['y'] - dest['y']), 2))


def route_length(stops, coord_map):
    '''
    Funcion para calcular la longitud de una ruta
    Tiene en cuenta la salida del punto de partida y el retorno
    Si la ruta esta vacia devuelve 0

    Parameters
    ----------
        stops: list
            Lista con las paradas que hace cada ruta

        coord_map: dict
            Diccionario con las coordenadas de cada parada

    Returns
    -------
        length: float
            Longitud total de la ruta

    '''
    if len(stops) == 0:
        return 0
    
    length = distance(coord_map[1], coord_map[stops[0]])

    for i in range(0, len(stops) - 1):
        length += distance(coord_map[stops[i]], coord_map[stops[i+1]])
    
    length += distance(coord_map[stops[len(stops)-1]], coord_map[1])
    return length

def validate_route(route, capacity, coord_map):
    '''
    Funcion para validar una ruta

    Parameters
    ----------
        route: list
            Lista con las paradas que hace cada ruta

        capacity: int
            Distancia maxima que puede recorrer un camion

        coord_map: dict
            Diccionario con las coordenadas de cada parada

    Returns
    -------
        valid: boolean
            Validez de la ruta, es decir, si la longitud de la ruta
            es menor que la distancia maxima que puede recorrer 
            un camion

    '''
    length = route_length(route, coord_map)
    return length < capacity

def augerat_parser(path): 
    '''
    Funcion para leer los ficheros de las instancias Augerat

    Parameters
    ----------
        path: string
            Ruta donde se encuentra el fichero a leer

    Returns
    -------
        coord_map: dict
            Diccionario con las paradas y sus coordenadas en el plano
            La primera parada es el deposito de donde parten y a donde
            llegan todos los camiones
    '''
    with open(path) as file:
        coord_map = {}
        flag = False
        for line in file.readlines(): 
            if 'DEMAND_SECTION' in line:
                return coord_map
            if flag:
                node = line.split(' ')
                coord_map[int(node[1])] = {'x': int(node[2]), 'y': int(node[3][:-1])}
            if 'NODE_COORD_SECTION' in line: 
                flag = True

def routes_score(routes, coord_map):
    '''
    Funcion para calcular la puntuacion de todas las rutas

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

    Returns
    -------
        score: float
            Suma de las longitudes de todas las rutas

    '''
    score = 0
    for route in routes:
        score += route_length(route['stops'], coord_map)
    
    return score

def intra_swap(route, first_element, second_element):
    '''
    Intercambia dos elementos de la misma ruta

    Parameters
    ----------
        route: list
            Lista con las paradas de la ruta

        first_element: int
            Indice del primer elemento
        
        second_element: int
            Indice del segundo elemento

    Returns
    -------
        new_route: list
            Lista con las paradas de la ruta despues del intercambio

    '''
    new_route = route[:]

    aux = new_route[first_element]
    new_route[first_element] = new_route[second_element]
    new_route[second_element] = aux

    return new_route

def intra_shift(route, elem_index, shift_index): 
    '''
    Desplaza un elemento de una ruta a una posicion

    Parameters
    ----------
        route: list
            Lista con las paradas de la ruta

        elem_index: int
            Indice del elemento a desplazar
        
        shift_index: int
            Posicion donde se va a insertar el elemento

    Returns
    -------
        new_route: list
            Lista con las paradas de la ruta despues del desplazamiento

    '''
    new_route = route[:]

    new_route.insert(elem_index, new_route.pop(shift_index))

    return new_route


def inter_swap(origin_route, dest_route, first_element, second_element):
    '''
    Intercambia dos elementos de distintas rutas

    Parameters
    ----------
        origin_route: list
            Lista con las paradas de la ruta de origen
        
        dest_route: list
            Lista con las paradas de la ruta de destino

        first_element: int
            Indice del elemento de la ruta de origen
        
        second_element: int
            Indice del elemento de la ruta de destino

    Returns
    -------
        (new_origin_route, new_dest_route): tuple
            Tupla con las listas de las paradas de las rutas despues
            del intercambio

    '''
    new_origin_route = origin_route[:]
    new_dest_route = dest_route[:]

    aux = new_origin_route[first_element]
    new_origin_route[first_element] = new_dest_route[second_element]
    new_dest_route[second_element] = aux

    return (new_origin_route, new_dest_route)

def inter_shift(origin_route, dest_route, elem_index, shift_index): 
    '''
    Inserta un elemento de una ruta a una posicion de otra ruta

    Parameters
    ----------
        origin_route: list
            Lista con las paradas de la ruta de origen

        dest_route: list
            Lista con las paradas de la ruta de destino

        elem_index: int
            Indice del elemento a desplazar de la ruta de origen
        
        shift_index: int
            Posicion donde se va a insertar el elemento den la ruta de destino

    Returns
    -------
        (new_origin_route, new_dest_route): tuple
            Tupla con las listas de las paradas de las rutas despues
            del intercambio

    '''
    new_origin_route = origin_route[:]
    new_dest_route = dest_route[:]

    new_dest_route.insert(shift_index, new_origin_route.pop(elem_index))

    return (new_origin_route, new_dest_route)

def sequence_exchange(origin_route, dest_route, first_element, second_element, sequence_length):
    '''
    Intercambia una secuencia de elementos de distintas rutas

    Parameters
    ----------
        origin_route: list
            Lista con las paradas de la ruta de origen
        
        dest_route: list
            Lista con las paradas de la ruta de destino

        first_element: int
            Indice del primer elemento de la ruta de origen
        
        second_element: int
            Indice del primer elemento de la ruta de destino
        
        sequence_length: int
            Longitud de la secuencia a intercambiar

    Returns
    -------
        (new_origin_route, new_dest_route): tuple
            Tupla con las listas de las paradas de las rutas despues
            del intercambio

    '''
    new_origin_route = origin_route[:]
    new_dest_route = dest_route[:]

    for i in range(0, sequence_length):
        new_origin_route, new_dest_route = inter_swap(new_origin_route, new_dest_route, first_element + i, second_element + i)
    
    return (new_origin_route, new_dest_route)

def VND_movement(routes, coord_map, capacity, inter_movements, intra_movements):
    '''
    Realiza un movimiento en varios vecindarios que mejore la solucion actual

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
        inter_movements: list
            Lista con los moviminentos entre distintas rutas que puede realizar

        intra_movements: list
            Lista con los movimientos dentro de la misma ruta que puede realizar

    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza
            despues de mejorar
        
        improvement: boolean
            En caso de no mejorar devuelve False

    '''
    new_routes = deepcopy(routes)
    shuffle(inter_movements)
    shuffle(intra_movements)

    for route in new_routes:
        rl = route_length(route['stops'], coord_map)

        for movement in intra_movements:
            # For each pair of elements in the same route
            for i, j in permutations(range(0,len(route['stops'])), 2):
                new_route = movement(route['stops'], i, j)
                if (route_length(new_route, coord_map) < rl) and validate_route(new_route,capacity, coord_map):
                    route['stops'] = new_route
                    return new_routes
            
    
    for first_route, second_route in permutations(new_routes, 2):
        rl = route_length(first_route['stops'], coord_map) + route_length(second_route['stops'], coord_map) 

        for movement in inter_movements:
            # For each pair of elements of the two routes selected
            for i, j in product(range(0, len(first_route['stops'])), range(0,len(second_route['stops']))):
                new_first_route, new_second_route = movement(first_route['stops'], second_route['stops'], i, j)

                if (route_length(new_first_route, coord_map) + route_length(new_second_route, coord_map) < rl) and validate_route(new_first_route,capacity, coord_map) and validate_route(new_second_route,capacity, coord_map):
                    improvement = True
                    first_route['stops'] = new_first_route
                    second_route['stops'] = new_second_route
                    return new_routes

    return False


def VND(routes, coord_map, capacity, inter_movements, intra_movements):
    '''
    Realiza movimientos en varios vecindarios mientras mejoren la solucion actual

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
        inter_movements: list
            Lista con los moviminentos entre distintas rutas que puede realizar

        intra_movements: list
            Lista con los movimientos dentro de la misma ruta que puede realizar

    Returns
    -------
        improvement: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza
            despues de mejorar. En caso de no mejorar, devuelve las rutas originales
    '''

    improvement = VND_movement(routes, coord_map, capacity, inter_movements, intra_movements)
    if not improvement:
        return routes
    while improvement:
        proposal = VND_movement(improvement, coord_map, capacity, inter_movements, intra_movements)
        if proposal:
            improvement = proposal
        else:
            return improvement

def MC2(routes, coord_map, capacity):
    '''
    Realiza dos movimientos aleatorios que generen una serie de rutas validas

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones


    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza
            despues de realizar los movimientos

    '''
    new_routes = deepcopy(routes)
    intra_movements = [intra_swap, intra_shift]
    inter_movements = [inter_swap, inter_shift]

    for i in range(0,2):
        valid_route = False
        while not valid_route:

            movement_type = randint(0,1)
            if movement_type == 0: # Intra_movement
                movement = randint(0,len(intra_movements)-1)
                route_index = randint(0,len(new_routes)-1)
                route = new_routes[route_index]

                while len(route['stops']) < 2:
                    route_index = randint(0,len(new_routes)-1)
                    route = new_routes[route_index]

                rl = len(route['stops'])-1

                first_index = randint(0,rl)
                second_index = randint(0,rl)

                while first_index == second_index:
                    second_index = randint(0,rl)

                new_route = intra_movements[movement](route['stops'], first_index, second_index)
                valid_route = validate_route(new_route,capacity, coord_map)

                if valid_route:
                    route['stops'] = new_route
                    # No se pueden realizar dos movimientos iguales
                    intra_movements.pop(movement)
            
            else:
                movement = randint(0,len(inter_movements)-1)
                origin_route_index = randint(0,len(new_routes)-1)
                origin_route = new_routes[origin_route_index]

                while len(origin_route['stops']) < 1:
                    origin_route_index = randint(0,len(new_routes)-1)
                    origin_route = new_routes[origin_route_index]

                dest_route_index = randint(0,len(new_routes)-1)
                dest_route = new_routes[dest_route_index]

                while origin_route_index == dest_route_index or len(dest_route['stops']) < 1:
                    dest_route_index = randint(0,len(new_routes)-1)
                    dest_route = new_routes[dest_route_index]

                origin_rl = len(origin_route['stops'])-1
                dest_rl = len(dest_route['stops'])-1

                first_index = randint(0,origin_rl)
                second_index = randint(0,dest_rl)

                new_origin_route, new_dest_route = inter_movements[movement](origin_route['stops'], dest_route['stops'], first_index, second_index)
                valid_route = validate_route(new_origin_route,capacity, coord_map) and validate_route(new_dest_route,capacity, coord_map) 

                if valid_route:
                    origin_route['stops'], dest_route['stops'] = new_origin_route, new_dest_route
                    # No se pueden realizar dos movimientos iguales
                    inter_movements.pop(movement)
    
    return new_routes


def SE_MOVEMENT(routes, coord_map, capacity, sequence_length):
    '''
    Realiza un intercambio de secuencia

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
        sequence_length: int
            Longitud de la secuencia a intercambiar

    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion despues de intercambiar la secuencia

    '''
    new_routes = deepcopy(routes)
    valid_route = False
    attempts = 0

    # Limitamos los intentos a un maximo, ya que dependiendo de otros factores puede tardar demasiado en converger
    while not valid_route and attempts < MAX_ATTEMPTS:
        attempts += 1
        origin_route_index = randint(0,len(new_routes)-1)
        origin_route = new_routes[origin_route_index]

        while len(origin_route['stops']) <= sequence_length:
            origin_route_index = randint(0,len(new_routes)-1)
            origin_route = new_routes[origin_route_index]

        dest_route_index = randint(0,len(new_routes)-1)
        dest_route = new_routes[dest_route_index]

        while origin_route_index == dest_route_index or len(dest_route['stops']) <= sequence_length:
            dest_route_index = randint(0,len(new_routes)-1)
            dest_route = new_routes[dest_route_index]

        # La parada que se puede escoger como origen tiene que permitir que se intercambie toda la secuencia
        origin_rl = len(origin_route['stops']) - 1 - sequence_length
        dest_rl = len(dest_route['stops']) - 1 - sequence_length

        # Si la ruta tiene tantos elementos como la secuencia, el indice debe ser 0 forzosamente
        # En caso contrario, es aleatorio
        first_index = 0 if origin_rl == 0 else randint(0,origin_rl)
        second_index = 0 if dest_rl == 0 else randint(0,dest_rl)

        new_origin_route, new_dest_route = sequence_exchange(origin_route['stops'], dest_route['stops'], first_index, second_index, sequence_length)
        valid_route = validate_route(new_origin_route, capacity, coord_map) and validate_route(new_dest_route, capacity, coord_map) 

        if valid_route:
            origin_route['stops'], dest_route['stops'] = new_origin_route, new_dest_route
        
    return new_routes

def SE2(routes, coord_map, capacity):
    '''
    Wrapper de SE_MOVEMENT con una secuencia de dos
    Usado para tener un formato de movimiento comun en Shake

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion despues de intercambiar la secuencia

    '''
    return SE_MOVEMENT(routes, coord_map, capacity, 2)

def SE3(routes, coord_map, capacity):
    '''
    Wrapper de SE_MOVEMENT con una secuencia de tres
    Usado para tener un formato de movimiento comun en Shake

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion despues de intercambiar la secuencia

    '''
    return SE_MOVEMENT(routes, coord_map, capacity, 3)


def shake(routes, coord_map, capacity, k):
    '''
    Genera un nuevo conjunto de rutas aleatorio en un vecindario
    Existen 6 vecindarios, determinados por las tres funciones
    MC2, SE2 y SE3, que se pueden ejecutar una o dos veces. 

    Parameters
    ----------
        routes: dict
            Diccionario con las rutas que hace cada camion, y el camion que las realiza

        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
        k: int
            Numero de cambios de vecindario a realizar
        
    Returns
    -------
        new_routes: dict
            Diccionario con las rutas que hace cada camion despues de cambiar de vecindario

    '''
    new_routes = deepcopy(routes)
    neighbours = [MC2, SE2, SE3]

    for i in range(0,k):
        neighbour = randint(0,len(neighbours)-1)
        movements = randint(1,2)
        for j in range(0,movements):
            new_routes = neighbours[neighbour](routes, coord_map, capacity)

    return new_routes




def build_routes(coord_map, trucks):
    '''
    Metodo greedy para construir rutas dado un numero de camiones
    Genera una lista aleatoria con las paradas, y las asigna iterativamente
    al camion cuya ruta se quede mas corta tras la asignacion

    Parameters
    ----------
        coord_map: dict
            Diccionario con las coordenadas de cada parada

        trucks: int
            Numero de camiones
        
    Returns
    -------
        routes: dict
            Diccionario con las rutas que hace cada camion

    '''
    routes = []
    for truck in range(1, trucks+1):
        route = {
            'truck': truck,
            'stops': []
        }
        routes.append(route)

    # La primera parada es el deposito, asi que no se asigna a ningun camion
    stop_list = [i for i in range(2, len(coord_map)+1)]
    shuffle(stop_list)

    while stop_list:
        new_stop = stop_list.pop()
        min_length = inf
        next_route = {}
        for route in routes:
            stops = route['stops'][:]
            stops.append(new_stop)
            rl = route_length(stops, coord_map)
            if rl < min_length:
                min_length = rl
                next_route = route
        
        next_route['stops'].append(new_stop)

    return routes

def build_initial_solution(coord_map, capacity):
    '''
    Metodo iterativo para construir una solucion inicial
    Incrementa el numero de camiones con el que se llama
    al metodo greedy hasta que se genera una solucion valida

    Parameters
    ----------
        coord_map: dict
            Diccionario con las coordenadas de cada parada

        capacity: int
            Capacidad maxima de los camiones
        
    Returns
    -------
        routes: dict
            Diccionario con las rutas que hace cada camion

    '''
    valid_routes = False
    trucks = 0
    while not valid_routes:
        trucks += 1
        routes = build_routes(coord_map, trucks)
        valid_routes = True
        for route in routes:
            valid_routes = valid_routes and validate_route(route['stops'], capacity, coord_map)

    print(f"Starting with {trucks} trucks")
    return routes


def general_VNS(path, k_max, capacity, inter_movements, intra_movements, verbose=0):
    '''
    Metodo que ejecuta un VNS general sobre una instancia del problema VRP definido por
    Augerat. 

    Parameters
    ----------
        path: string
            Ruta donde se encuentra el fichero de la instancia
        
        k_max: int
            Numero maximo de cambios de vecindario que se pueden realizar

        capacity: int
            Capacidad maxima de los camiones
        
        inter_movements: list
            Lista con los moviminentos entre distintas rutas que puede realizar el VND

        intra_movements: list
            Lista con los movimientos dentro de la misma ruta que puede realizar el VND

        verbose: int
            Nivel de verbose del codigo. 0 muestra el resultado, 1 muestra algun paso 
            intermedio, 2 muestra todos los pasos intermedios

        
    Returns
    -------
        score: int
            Puntuacion final de las rutas del algoritmo

    '''
    k = 1
    coord_map = augerat_parser(path)
    routes = build_initial_solution(coord_map, capacity)
    score = routes_score(routes, coord_map)


    while k < k_max:
        new_routes = shake(routes, coord_map, capacity, k)
        if verbose > 1:
            print(f'Shake score: {routes_score(new_routes, coord_map)} for k: {k}')

        new_routes = VND(new_routes, coord_map, capacity, inter_movements, intra_movements)
        new_score = routes_score(new_routes, coord_map)
        if verbose > 1:
            print(f'VND score: {new_score}')

        if new_score < score:
            if verbose > 0:
                print(f'The score has improved by {score - new_score}')
                print(f'Current score: {new_score}')
            k = 1
            routes = new_routes 
            score = routes_score(routes, coord_map)

        else:
            k += 1

    if verbose > 0:
        for route in routes:
            print(f"Route {route['truck']} with score {route_length(route['stops'], coord_map)}")

    print(f"Best score: {score}")
    return score

def general_VNS_small(path, k_max, capacity, verbose=0):
    '''
    Wrapper que ejecuta un VNS general sobre una instancia del problema VRP definido por
    Augerat con dos movimientos para el VND. 

    Parameters
    ----------
        path: string
            Ruta donde se encuentra el fichero de la instancia
        
        k_max: int
            Numero maximo de cambios de vecindario que se pueden realizar

        capacity: int
            Capacidad maxima de los camiones

        verbose: int
            Nivel de verbose del codigo. 0 muestra el resultado, 1 muestra algun paso 
            intermedio, 2 muestra todos los pasos intermedios

        
    Returns
    -------
        score: int
            Puntuacion final de las rutas del algoritmo

    '''
    inter_movements = [inter_swap]
    intra_movements = [intra_swap]
    return general_VNS(path, k_max, capacity, inter_movements, intra_movements, verbose)

def general_VNS_mid(path, k_max, capacity, verbose=0):
    '''
    Wrapper que ejecuta un VNS general sobre una instancia del problema VRP definido por
    Augerat con tres movimientos para el VND. 

    Parameters
    ----------
        path: string
            Ruta donde se encuentra el fichero de la instancia
        
        k_max: int
            Numero maximo de cambios de vecindario que se pueden realizar

        capacity: int
            Capacidad maxima de los camiones

        verbose: int
            Nivel de verbose del codigo. 0 muestra el resultado, 1 muestra algun paso 
            intermedio, 2 muestra todos los pasos intermedios

        
    Returns
    -------
        score: int
            Puntuacion final de las rutas del algoritmo

    '''
    inter_movements = [inter_swap, inter_shift]
    intra_movements = [intra_swap]
    return general_VNS(path, k_max, capacity, inter_movements, intra_movements, verbose)


def general_VNS_big(path, k_max, capacity, verbose=0):
    '''
    Wrapper que ejecuta un VNS general sobre una instancia del problema VRP definido por
    Augerat con cuatro movimientos para el VND. 

    Parameters
    ----------
        path: string
            Ruta donde se encuentra el fichero de la instancia
        
        k_max: int
            Numero maximo de cambios de vecindario que se pueden realizar

        capacity: int
            Capacidad maxima de los camiones

        verbose: int
            Nivel de verbose del codigo. 0 muestra el resultado, 1 muestra algun paso 
            intermedio, 2 muestra todos los pasos intermedios

        
    Returns
    -------
        score: int
            Puntuacion final de las rutas del algoritmo

    '''
    inter_movements = [inter_swap, inter_shift]
    intra_movements = [intra_swap, intra_shift]
    return general_VNS(path, k_max, capacity, inter_movements, intra_movements, verbose)