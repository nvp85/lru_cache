import sys
from collections import OrderedDict


def lru_cache(input=sys.stdin, output=sys.stdout):
    size = None
    cache = OrderedDict()
    while not size:
        size_input = input.readline().strip().split(' ')
        if size_input[0] == 'SIZE' and len(size_input) == 2:
            try:
                size = int(size_input[1])
                output.write('SIZE OK\n')
            except (TypeError, ValueError):
                output.write('Size must be integer\n')
        else:
            output.write('You should set size of a cache:\n')
    for s in input:
        s = s.strip().split(' ')
        if len(s) > 0:
            command = s[0]
            if command == 'EXIT':
                break
            elif command == 'SET':
                if len(s) == 3:
                    key, value = s[1], s[2]
                    cache[key] = value
                    output.write('SET OK\n')
                    if len(cache) > 3:
                        cache.popitem(last=False)
                else:
                    output.write('ERROR\n')
            elif command == 'GET':
                if len(s) == 2:
                    key = s[1]
                    try:
                        value = cache.pop(key)
                        output.write('GOT {0}\n'.format(value))
                        cache[key] = value
                    except KeyError:
                        output.write('NOTFOUND\n')
                else:
                    output.write('ERROR\n')


if __name__ == "__main__":
    lru_cache()
