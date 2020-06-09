import json


def load_json(str):
    with open(str, 'r') as file:
        load_dict = json.load(file)

    n = load_dict['n']
    m = load_dict['m']
    k = load_dict['k']
    L = load_dict['L']
    dest = load_dict['dest']
    coordinates = load_dict['coordinates']
    pb = load_dict['pb']
    pc = load_dict['pc']
    cr = load_dict['cr']
    cb = load_dict['cb']
    return n, m, k, L, dest, coordinates, pb, pc, cr, cb


def dump_json(str, n, m, k, L, dest, coordinates, pb, pc, cr, cb):
    dump_dict = {'n': n, 'm': m, 'k': k, 'L': L, 'dest': dest, 'coordinates': coordinates,
                 'pb': pb, 'pc': pc, 'cr': cr, 'cb': cb}
    with open(str, 'w') as file:
        json.dump(dump_dict, file)


if __name__ == '__main__':
    pass
