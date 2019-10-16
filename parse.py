from yaml import load, Loader

import itertools

def make_is_options(key):
    return [key[3:]+',', 'not'+key[2:]+',']
def make_by_options(val):
    return [x + ',' for x in parse_subtree(val)]

def parse_subtree(subtree):
    classlist = []
    cartesian = None
    for key, val in subtree.items():
        if key.startswith('is '):
            if cartesian is None:
                cartesian = make_is_options(key)
            else:
                cartesian = [x + y for x, y in  itertools.product(cartesian, make_is_options(key))]
        elif key.startswith('by '):
            if cartesian is None:
                cartesian = make_by_options(val)
            else:
                cartesian = [x + y for x, y in  itertools.product(cartesian, make_by_options(val))]
        elif val is None:
            classlist.append(key)
        else:
            classlist += [key + '/' + item for item in parse_subtree(val)]
    if cartesian is not None:
        classlist += [x[:-1] for x in cartesian]
    return classlist

def parse_classdef(path='classdef.yml'):
    with open('classdef.yml', 'r') as f:
        classdef = load(f, Loader)
        classdef = {line:idx for idx, line in enumerate(parse_subtree(classdef))}
    return classdef
