import re

VERSION = '0.4.0'


def compare_version(a, b, separator='.', ignorecase=True):
    def _preprocess(v, separator, ignorecase):
        if ignorecase:
            v = v.lower()
        return [int(x) if x.isdigit() else [int(y) if y.isdigit() else y for y in re.findall("\d+|[a-zA-Z]+", x)] for x in v.split(separator)]
    a = _preprocess(a, separator, ignorecase)
    b = _preprocess(b, separator, ignorecase)
    return (a > b) - (a < b)
