from yaml import load, Loader

from parse import parse_subtree

with open('classdef.yml', 'r') as f:
    classdef = load(f, Loader)
    for idx, line in enumerate(parse_subtree(classdef)):
        print('%03d' % idx, line)
