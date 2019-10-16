from collections import namedtuple
from parse import parse_classdef
from yaml import load, Loader

import sys
import re

Item = namedtuple('Item', 'name origin_id unified_ids')


class MapDef:

    _CLASSDEF = parse_classdef()

    def __init__(self, map_file):
        with open(map_file, 'r') as f:
            mapdef = load(f, Loader)
        self.dict_by_name = {}
        self.dict_by_id = {}
        for km, vm in mapdef.items():
            ids = []
            for uri in vm['uri']:
                if any(ch in uri for ch in '.*+['):
                    ids += [vc for kc, vc in self._CLASSDEF.items() if re.match(uri, kc)]
                else:
                    ids += [vc for kc, vc in self._CLASSDEF.items() if kc.startswith(uri)]
            item = Item(name=km, origin_id=vm['id'], unified_ids=ids)
            self.dict_by_name[item.name] = item
            self.dict_by_id[item.origin_id] = item

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.dict_by_id[idx]
        if isinstance(idx, str):
            return self.dict_by_name[idx]

    def keys(self):
        return self.dict_by_name.keys()

    def items(self):
        return self.dict_by_name.items()

if __name__ == '__main__':
    try:
        MAP_FILE = sys.argv[1]
        mapdef = MapDef(MAP_FILE)

        for k, v in mapdef.items():
            print(k, ':', v)
    except:
        print("Usage: python map.py <map_file>")

