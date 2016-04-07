import re


__re_permil = re.compile('\-*[0-9]+.*[0-9]*%{2}')
__re_percent = re.compile('\-*[0-9]+.*[0-9]*%{1}')
__re_float = re.compile('\-*[0-9]+\.{1}[0-9]+')
__re_int = re.compile('\-*[0-9]+\.{0}')


def str2num(s):
    if s is None:
        return None
    s = s.replace('+', '').replace(',', '')

    if __re_permil.match(s):
        res = float(s.replace('%%', '')) / 1000
    elif __re_percent.match(s):
        res = float(s.replace('%', '')) / 100
    elif __re_int.match(s):
        res = int(s)
    elif __re_float.match(s):
        res = float(s)
    else:
        res = s

    return res
