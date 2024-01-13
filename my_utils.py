from os import path
from re import match
from re import split as re_spl
from re import findall as re_find
from datetime import date
from dateutil.parser import parse as dtu_parse
from json import load, dumps

def eh_valido_para_remover_nones(o):
    tipos = [list, int, float, str]
    return any([isinstance(o, t) for t in tipos])


def remover_nones(d):
    try:
        if not isinstance(d, dict):
            d = d.__dict__
        return { k: remover_nones(v) for k, v in d.items() if eh_valido_para_remover_nones(v) }
    except:
        if isinstance(d, list):
            aux = []
            for i in d:
                if eh_valido_para_remover_nones(i):
                    aux.append(remover_nones(i))
            return aux
        if eh_valido_para_remover_nones(d):
            return d


def converter(o, tipo, default=None):
    try:
        return tipo(o)
    except:
        return default

class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def _dict(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

    def __init__(self, dct):
        if type(dct) is list:
            for d in dct:
                self._dict(d)
        else:
            self._dict(dct)


def dotdict(obj):
    if type(obj) is list:
        for d in obj:
            d = DotDict(d)
        return obj
    else:
        return DotDict(obj)


class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_json_file(self, file):
        with open(f'{self.base_path}{file}.json') as json_file:
            return dotdict(load(json_file))

    def set_json_file(self, file, any):
        with open(f'{self.base_path}{file}.json', 'w') as jsonFile:
            jsonFile.write(dumps(any))
    
    def join(self, *_subpaths):
        return path.join(self.base_path, *_subpaths)


def merge_lists(lists):
    merged_list = []
    for sublist in lists:
        for element in sublist:
            if element not in merged_list:
                merged_list.append(element)
    return merged_list


def isdate_to_iso(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def validate_startswith_to_date(_str):
    padrao = "^\d{4}-\d{2}-\d{2}"
    if match(padrao, _str):
        try:
            return dtu_parse(_str)
        except:
            pass
    return _str


def func_filter(_str, entity):
    padrao = r'(?:==|!=|>=|<=|>|<)+'
    try:
        chave, valor = re_spl(padrao, _str, maxsplit=1)
        if len(valor) != 10:
            return eval(f'entity.{_str}')
        obj_date = dtu_parse(valor)
        match re_find(padrao, _str)[0]:
            case '==':
                return eval(f'entity.{chave}') == obj_date
            case '!=':
                return eval(f'entity.{chave}') != obj_date
            case '>=':
                return eval(f'entity.{chave}') >= obj_date
            case '<=':
                return eval(f'entity.{chave}') <= obj_date
            case '<':
                return eval(f'entity.{chave}') < obj_date
            case '>':
                return eval(f'entity.{chave}') > obj_date
            case _:
                return eval(f'entity.{_str}')
    except:
        return eval(f'entity.{_str}')
