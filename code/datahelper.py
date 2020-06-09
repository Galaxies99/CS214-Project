import json


def load_json(str):
    with open(str, 'r') as file:
        load_dict = json.load(file)

    n = load_dict['n']
    m = load_dict['m']
    k = load_dict['k']
    L = load_dict['L']
    dest = load_dict['dest']
    departure_coordinate = load_dict['departure_coordinate']
    coordinates = [departure_coordinate]
    coordinates.extend(load_dict['destination_coordinates'])
    pb = load_dict['pb']
    pc = load_dict['pc']
    cr = load_dict['cr']
    cb = load_dict['cb']
    return n, m, k, L, dest, coordinates, pb, pc, cr, cb
