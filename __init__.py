import os
import re
import sys
import json
import math
import time
import pickle
import random
import datetime
import operator as op
import functools as ft
import itertools as it
from collections import Counter, deque, defaultdict as dd
from types import SimpleNamespace as NS
from operator import attrgetter as agt, itemgetter as igt

from .files import *
from .strings import *

pm = sys.modules[__name__]

home_dir = os.path.expanduser('~').replace('\\', '/').replace('C:', '')
cd = lambda p=home_dir: os.chdir(p)
d60 = lambda n: divmod(n, 60)
d64 = lambda n: divmod(n, 64)
dm = divmod
fact = math.factorial
get_default = lambda l, i, d=None: l[i] if len(l) > i else d
ident = lambda arg: arg
is_seq = lambda obj: isinstance(obj, (list, tuple))
is_col = lambda obj: isinstance(obj, (list, tuple, set, frozenset))
kilo = lambda n=1: pow(1024, n)
log = math.log
log2 = math.log2
log10 = math.log10
noop = lambda *args, **kwargs: None
pdir = lambda o: [i for i in dir(o) if not i.startswith('_')]
print_lines = lambda *s, **kw: print(*s, **kw, sep='\n')
print_log = lambda *s, **kw: print(*s, **kw, file=sys.stderr)
pvars = lambda o: [i for i in vars(o) if not i.startswith('_')]
pwd = lambda: os.getcwd().replace('\\', '/')
rand_elem = lambda l, n=None: random.sample(l, n) if n else random.choice(l)
shuffle = random.shuffle
sortset = lambda l: sorted(set(l))
sqrt = math.sqrt
starmap = lambda *args: list(it.starmap(*args))
strip_nums = lambda s, invert=False: ''.join(c for c in s if (c.isalpha() ^ invert))
tup = tpl = lambda o: (o,)
uniq = lambda l: list(dict.fromkeys(l))

true, false = True, False
inf, nan = float('inf'), float('nan')
pi = math.pi

def println(*l, **kw):
    for arg in l:
        print(*arg, **kw, sep='\n')

def list_diff(l):
    if len(l) < 2:
        return []
    return [l[i+1] - l[i] for i in range(len(l)-1)]

def first_diff(a, b):
    for (n, (i, j)) in enumerate(zip(a, b)):
        if i != j:
            return n
    return -1

def iter_diffs(a, b):
    return (n for (n, (i, j)) in enumerate(zip(a, b)) if i != j)

def all_same(it):
    try:
        return not it or it.count(it[0]) == len(it)
    except:
        it = iter(it)
        try:
            first = next(it)
        except StopIteration:
            return True
        return all(first == rest for rest in it)

def ilen(it):
    try:
        return len(it)
    except:
        return sum(1 for i in it)

def split_list(arr, *nums):
    ret = []
    current = 0
    for n in nums:
        if n == -1:
            ret.append(arr[current:])
        else:
            ret.append(arr[current:current+n])
        current += n
    return ret

def group_list(arr, key=None, sort=False):
    if sort:
        arr = sorted(arr, key=key)
    if isinstance(key, str):
        key = agt(key)
    elif isinstance(key, int):
        key = igt(key)
    return [list(j) for (i, j) in it.groupby(arr, key)]

def split_pred(arr, key=None):
    if key is None:
        key = lambda i: i
    yes = []
    no = []
    yes_a = yes.append
    no_a = no.append
    for elem in arr:
        if key(elem):
            yes_a(elem)
        else:
            no_a(elem)
    return yes, no

def flatten(arr):
    return [obj for sub in arr for obj in sub]

def filter_counter(c, threshold=1):
    n = Counter()
    for i in c:
        if c[i] > threshold:
            n[i] = c[i]
    return n

def count_dups(itr):
    c = Counter(itr)
    return filter_counter(c)

def get_all_longest(it):
    m_len = 0
    ret = []
    for elem in it:
        l = len(elem)
        if l > m_len:
            m_len = l
            ret = [elem]
        elif l == m_len:
            ret.append(elem)
    return ret

def eat(iterator, n=None):
    if n is None:
        deque(iterator, maxlen=0)
    else:
        next(it.islice(iterator, n, n), None)

def get_item(objs, name, key=repr, default=None):
    if isinstance(key, str):
        key = agt(key)
    elif isinstance(key, int):
        key = igt(key)
    return next((i for i in objs if key(i) == name), default)

def pluck(objs, attr):
    return list(map(agt(attr), objs))

def setattrs(objs, attr, value):
    for obj in objs:
        setattr(obj, attr, value)

def key_confirm(prompt='', keys=b'\ry', file=sys.stdout, echo=True):
    '''Returns pressed key if keys is None, otherwise returns True if key was 'y' or Enter'''
    import msvcrt
    if prompt:
        prompt = prompt.rstrip() + ' '
    print(prompt, end='', file=file, flush=True)
    if echo:
        key = msvcrt.getche()
        if key == b'\r' and keys:
            print(f'{prompt}y', end='', file=file, flush=True)
    else:
        key = msvcrt.getch()
    if key == b'\x03':
        raise KeyboardInterrupt
    print(file=file)
    if keys is None:
        return key
    return key in keys

def mean(seq):
    total = 0
    num = 0
    for num, i in enumerate(seq, 1):
        total += i
    return total/num

def median(data, key=None):
    data = sorted(data, key=key)
    n = len(data)
    if not n:
        raise ValueError('Empty dataset')
    if n % 2:
        return data[n//2]
    else:
        i = n//2
        return (data[i-1] + data[i])/2

def sort_keys(d, key=None, reverse=False):
    d = d.items()
    if key:
        _key = key
        def key(tup):
            return _key(tup[0])
    d = sorted(d, key=key, reverse=reverse)
    return dict(d)

def sort_values(d, key=None, reverse=False):
    d = d.items()
    if key:
        _key = key
        def key(tup):
            return _key(tup[1])
    else:
        key = igt(1)
    d = sorted(d, key=key, reverse=reverse)
    return dict(d)

def sort_items(d, key=None, reverse=False):
    d = d.items()
    d = sorted(d, key=key, reverse=reverse)
    return dict(d)

def rgb(r, g=0, b=0, a=1):
    if isinstance(r, str):
        s = r.replace('#', '')
        if len(s) >= 6:
            s = [s[i:i+2] for i in range(0, len(s), 2)]
            tup = tuple(int(i, 16) for i in s)
        else:
            tup = tuple(int(i, 16)*17 for i in s)
        if len(tup) == 4:
            r, g, b, a = tup
            return (r, g, b, round(a/255, 2))
        return tup
    if isinstance(r, (list, tuple)):
        try:
            r, g, b = r
        except ValueError:
            r, g, b, a = r
    if a != 1:
        a = '%02x' % round(255 * a)
    else:
        a = ''
    return f'#{r:02x}{g:02x}{b:02x}{a}'

def is_idle():
    return 'idlelib' in sys.modules

def is_interactive():
    return bool(sys.flags.interactive) or 'idlelib' in sys.modules or hasattr(sys, 'ps1')

def get_sig(obj):
    from inspect import signature as sig
    fmt = '%s%s'
    try:
        name = obj.__name__
    except:
        name = repr(obj)
    try:
        return fmt % (name, sig(obj))
    except Exception as e:
        if callable(obj):
            return fmt % (name, sig(obj.__call__))
        else:
            raise e from None

def load_var(*args, key=repr, gl):
    for obj in args:
        gl[key(obj)] = obj

def load_vars(*args, key=repr, gl):
    for arg in args:
        for obj in arg:
            gl[key(obj)] = obj

def hide_traces():
    def hook(tpe, value, traceback):
        print(f'{tpe.__name__}: {value}')
    sys.excepthook = hook

def show_traces():
    sys.excepthook = sys.__excepthook__

def XOR_encrypt(data, key):
    return bytes(i^j for (i, j) in zip(data, it.cycle(key)))

def skeleton(obj):
    if isinstance(obj, (list, tuple, set, frozenset)):
        return type(obj)(map(skeleton, obj))
    if isinstance(obj, dict):
        return {key: skeleton(val) for (key, val) in obj.items()}
    return obj.__class__.__name__

def gen_dunder(attr, method):
    method = '__%s__' % method
    def func(self, *args, **kwargs):
        obj = getattr(self, attr)
        function = getattr(obj, method)
        return function(*args, **kwargs)
    return func

def dunder(method, attr):
    def decorator(cls):
        name = '__%s__' % method
        setattr(cls, name, gen_dunder(attr, method))
        return cls
    return decorator

class NamedFunction:
    def __init__(self, func):
        self.func = func
        ft.update_wrapper(self, func)
        try:
            self.repr = get_sig(func)
        except:
            self.repr = func.__name__
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    def __repr__(self):
        return self.repr or '<NamedFunction>'

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
    @classmethod
    def deep_convert(cls, obj):
        if isinstance(obj, dict):
            return cls((i, cls.deep_convert(obj[i])) for i in obj)
        elif isinstance(obj, (list, tuple, set)):
            return type(obj)(cls.deep_convert(i) for i in obj)
        else:
            return obj

class GroupDict(dict):
    def __init__(self, itr=tuple(), *, cls=list, **kwargs):
        if cls not in (list, set):
            raise ValueError('Default factory must be list or set')
        self.default_factory = cls
        add = list.append if cls is list else set.add
        for key, value in itr:
            add(self[key], value)
        super().__init__(**kwargs)
    def __missing__(self, key):
        value = self.default_factory()
        self[key] = value
        return value

class CaptureOut:
    def __enter__(self):
        from io import StringIO
        self.orig = sys.stdout
        sys.stdout = self.out = StringIO()
        return self
    def __exit__(self, tpe, val, tb):
        self.result = self.out.getvalue()
        sys.stdout = self.orig
        self.out.close()

class Container:
    def __new__(cls, obj):
        if isinstance(obj, dict):
            return super().__new__(cls)
        elif isinstance(obj, (list, tuple, set)):
            return type(obj)(map(cls, obj))
        else:
            return obj
    def __init__(self, obj):
        for key in obj:
            value = obj[key]
            setattr(self, key, Container(value))
    def __repr__(self):
        itr = iter(self.__dict__)
        keys = [i for (i, j) in zip(itr, range(5))]
        s = ', '.join(keys)
        if next(itr) is not None:
            s += '...'
        return '%s(%s)' % (self.__class__.__name__, s)
    def __str__(self):
        s = ', '.join(self.__dict__)
        return '%s(%s)' % (self.__class__.__name__, s)
    def __iter__(self):
        return iter(self.__dict__)
    def __contains__(self, arg):
        return arg in self.__dict__
    def __len__(self):
        return len(self.__dict__)
    def __getitem__(self, arg):
        return getattr(self, str(arg))

class Sentinel:
    count = 0
    def __init__(self):
        self.num = Sentinel.count
        Sentinel.count += 1
    def __repr__(self):
        return '<sentinel #%d>' % self.num

class Getter:
    _sentinel = Sentinel()
    __slots__ = ('__names')
    def __init__(self, names=tuple()):
        self.__names = tuple(names)
    def __getattr__(self, arg):
        tup = (*self.__names, (arg, 'attr'))
        return Getter(tup)
    def __getitem__(self, arg):
        tup = (*self.__names, (arg, 'item'))
        return Getter(tup)
    def __neg__(self):
        return self.__getattr__('__neg__')()
    def __call__(self, obj=_sentinel, *, args=tuple(), kwargs=dict()):
        if obj is Getter._sentinel:
            tup = ((args, kwargs), 'func')
            return Getter(self.__names + (tup,))
        for name, tpe in self.__names:
            if tpe == 'attr':
                obj = getattr(obj, name)
            elif tpe == 'func':
                _args, _kwargs = name
                obj = obj(*_args, **_kwargs)
            elif tpe == 'item':
                obj = obj[name]
        return obj
    def __eq__(self, other):
        if isinstance(other, Getter):
            return self.__names == other.__names
        return NotImplemented
    def __hash__(self):
        return hash(self.__names)
    def __repr__(self):
        if not self.__names:
            return '%s()' % self.__class__.__name__
        rep = ['gtr']
        for name, tpe in self.__names:
            if tpe == 'attr':
                rep.append('.' + name)
            elif tpe == 'func':
                if rep[-1] == '.__neg__':
                    rep.pop()
                    rep.insert(0, '-')
                    continue
                args, kwargs = name
                terms = [repr(i) for i in args]
                terms += ['%s=%r' % tup for tup in kwargs.items()]
                terms = ', '.join(terms)
                rep.append(f'({terms})')
            elif tpe == 'item':
                if isinstance(name, slice):
                    idx = [name.start, name.stop, name.step]
                    if name.step is None:
                        idx.pop()
                    idx = ['' if i is None else repr(i) for i in idx]
                    rep.append('[%s]' % ':'.join(idx))
                else:
                    rep.append('[%r]' % (name,))
        return ''.join(rep)

gtr = Getter()

class Quitter:
    def __init__(self, func=None):
        self.enabled = True
        self.func = func
    def __getattr__(self, name):
        self.enabled = False
        return None
    def __call__(self, code=None):
        if self.func:
            self.func()
        print()
        try:
            sys.stdin.close()
        except:
            pass
        raise SystemExit(code)
    def __repr__(self):
        if not self.enabled:
            return '%s()' % self.__class__.__name__
        self()
        return ''
    def __str__(self):
        return 'Quitter'

if is_interactive():
    _len = len
    #@ft.wraps(_len)
    def lens(first, *rest):
        if rest:
            return [_len(first), *(_len(i) for i in rest)]
        return _len(first)
    qw = wq = pl = Quitter()
