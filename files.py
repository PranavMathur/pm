import os
import re
import json
import pickle

def read_file(filename, encoding=None, errors=None):
    '''Returns a string from a file'''
    if encoding == ascii:
        encoding = 'ascii'
    if not filename:
        raise FileNotFoundError('Filename empty')
    with open(filename, 'r', encoding=encoding, errors=errors) as f:
        return f.read()

def read_lines(filename, encoding=None, errors=None):
    '''Returns an array of lines from a file'''
    if encoding == ascii:
        encoding = 'ascii'
    if not filename:
        raise FileNotFoundError('Filename empty')
    with open(filename, 'r', encoding=encoding, errors=errors) as f:
        return f.read().splitlines()

def read_bytes(filename):
    '''Returns a bytes representation of a file'''
    if not filename:
        raise FileNotFoundError('Filename empty')
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, s, encoding=None, errors=None):
    '''Writes a string to a file'''
    assert '\n' not in filename, 'Filename cannot have newlines'
    if encoding == ascii:
        encoding = 'ascii'
    if not filename:
        raise FileNotFoundError('Filename empty')
    with open(filename, 'w', encoding=encoding, errors=errors) as f:
        f.write(s)

def write_lines(filename, lines, encoding=None, errors=None):
    '''Writes an array of strings to a file, separated by newlines'''
    assert '\n' not in filename, 'Filename cannot have newlines'
    if encoding == ascii:
        encoding = 'ascii'
    if not filename:
        raise FileNotFoundError('Filename empty')
    with open(filename, 'w', encoding=encoding, errors=errors) as f:
        f.write('\n'.join(lines))

def write_bytes(filename, b):
    '''Writes bytes to a file'''
    if not filename:
        raise FileNotFoundError('Filename empty')
    assert '\n' not in filename, 'Filename cannot have newlines'
    with open(filename, 'wb') as f:
        f.write(b)

def read_json(filename, encoding=None, errors=None, var=False):
    if not var:
        with open(filename, 'r', encoding=encoding, errors=errors) as f:
            return json.load(f)
    else:
        file = read_file(filename, encoding=encoding, errors=errors)
        if '=' in file[:20]:
            file = file[file.index('=')+1:]
        if ';' in file[-20:]:
            file = file[:file.rindex(';')]
##        try:
##            file = re.search(r'((\[)|(\{)).*(?(2)\]|\})', file, re.S)[0]
##        except TypeError:
##            raise ValueError(f'Could not find JSON in {filename}')
        return json.loads(file)

def write_json(filename, obj, indent='\t', var=None, **kwargs):
    with open(filename, 'w') as f:
        if var:
            f.write(f'var {var} = ')
        json.dump(obj, f, indent=indent, **kwargs)
        if var:
            f.write(';\n')

def read_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def write_pickle(filename, obj, **kwargs):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, **kwargs)

def file_size(s, unit='B'):
    if isinstance(unit, str):
        scale = {
            'G': 1024**3,
            'M': 1024**2,
            'K': 1024**1,
            'B': 1024**0,
            'GB': 1000**3,
            'MB': 1000**2,
            'KB': 1000**1
        }.get(unit.upper(), 1)
    elif isinstance(unit, int):
        scale = 1024 ** unit if unit < 10 else unit
    if scale == 1:
        return os.path.getsize(s)
    return os.path.getsize(s)/scale

def file_time(s, creation=False, access=False):
    if creation:
        return os.path.getctime(s)
    if access:
        return os.path.getatime(s)
    return os.path.getmtime(s)

def touch_file(s, mtime=None):
    atime = file_time(s, access=True)
    if mtime is None:
        os.utime(s)
        return
    os.utime(s, (atime, mtime))

def list_files(loc='.', end='', recursive=False):
    if isinstance(end, (list, set)):
        end = tuple(end)
    def check_end(name):
        return name.endswith(end)
    loc = loc.rstrip('/')
    if not file_exists(loc):
        raise FileNotFoundError(loc)
    if not recursive:
        walk = os.walk(loc)
        try:
            (dirpath, dirnames, filenames) = next(walk)
        except StopIteration:
            raise FileNotFoundError(loc) from None
        dirpath = dirpath.replace('\\', '/') + '/'
        if dirpath == './':
            dirpath = ''
        files = []
        for name in dirnames:
            i = dirpath + name + "/"
            if check_end(i):
                files += [i]
        for name in filenames:
            i = dirpath + name
            if check_end(i):
                files += [i]
        return files
    else:
        return [d[0].replace('\\','/')+'/'+i
                for d in os.walk(loc)
                for i in d[2]
                if check_end(i)]

def ls_iter(loc='.', end='', recursive=False):
    if isinstance(end, (list, set)):
        end = tuple(end)
    def check_end(name):
        return name.endswith(end)
    loc = loc.rstrip('/')
    if not file_exists(loc):
        raise FileNotFoundError(loc)
    if not recursive:
        walk = os.walk(loc)
        try:
            (dirpath, dirnames, filenames) = next(walk)
        except StopIteration:
            raise FileNotFoundError(loc) from None
        dirpath = dirpath.replace('\\', '/') + '/'
        if dirpath == './':
            dirpath = ''
        for name in dirnames:
            i = dirpath + name + "/"
            if check_end(i):
                yield i
        for name in filenames:
            i = dirpath + name
            if check_end(i):
                yield i
    else:
        for d in os.walk(loc):
            for i in d[2]:
                if check_end(i):
                    yield d[0].replace('\\', '/') + '/' + i

ls = list_files
ls_files = list_files
file_exists = os.path.exists
is_file = os.path.isfile
is_dir = os.path.isdir
rm_file = os.remove
mv_file = os.replace
