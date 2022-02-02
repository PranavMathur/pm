import re
import math
import codecs

utf8 = 'utf-8'
utf = 'utf-8'
ansi = 'ansi'
xmlrep = 'xmlcharrefreplace'

def input_strings(n=0, msg='Enter strings:'):
    l = []
    print(msg)
    c = 0
    while True:
        try:
            s = input()
        except EOFError:
            break
        if not s:
            break
        l += [s]
        c += 1
        if n and c >= n:
            break
    return l

def rot(o):
    enc = lambda i: codecs.encode(i, 'rot_13')
    if isinstance(o, str):
        return enc(o)
    elif isinstance(o, (list, tuple, set)):
        return type(o)(enc(i) for i in o)
    elif isinstance(o, dict):
        return {enc(i): rot(o[i]) for i in o}

def replace_table(s, d):
    for i in d:
        s = s.replace(i, d[i])
    return s

def re_count(pattern, string, flags=0):
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    return sum(1 for m in pattern.finditer(string))

def match_context(m, ctxt=30):
    start, end = m.span()
    return m.string[start-ctxt:end+ctxt]

def strip_lines(s):
    s = s.split('\n')
    s = [i.strip() for i in s]
    return '\n'.join(s)

def char(arg):
    try:
        return ord(arg)
    except:
        return chr(arg)

def test_encoding(i, encoding='ascii', errors='strict'):
    if encoding == ascii:
        encoding = 'ascii'
    try:
        if isinstance(i, bytes):
            i.decode(encoding, errors)
        else:
            i.encode(encoding, errors)
        return True
    except:
        return False

def get_encoding(i, encs=['ascii', 'utf-8', 'ANSI', 'latin-1']):
    for enc in encs:
        if enc == ascii:
            enc = 'ascii'
        if test_encoding(i, enc):
            return enc
    return 'Unknown'

def escape_utf(s):
    if not isinstance(s, str):
        raise TypeError('escape_utf takes string, not %s' % type(s))
    try:
        return s.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    except UnicodeError:
        return s

def print_cols(strings, transpose=False):
    import shutil
    if not isinstance(strings, list):
        strings = list(strings)
    maxlen = max(len(str(i)) for i in strings) + 2
    maxcols = shutil.get_terminal_size().columns
    cols = maxcols//maxlen
    length = len(strings)
    ldc = math.ceil(length/cols)
    if transpose:
        strings = [strings[i:i+cols] for i in range(0, length, cols)]
    else:
        strings = [strings[i::ldc] for i in range(ldc)]
    strings = [[str(i).ljust(maxlen) for i in row] for row in strings]
    for row in strings:
        print(''.join(row))

def color_context(match, *, ctxt=30, color=None):
    import colorama
    if color is None:
        color = colorama.Fore.RED
    RESET = colorama.Fore.RESET
    orig, start, end = match.string, match.start(), match.end()
    if ctxt != -1:
        pre = orig[start-ctxt:start]
        post = orig[end:end+ctxt]
    else:
        pre = orig[:start]
        post = orig[end:]
    context = pre + color + match[0] + RESET + post
    return context.replace('\n', ' ')

class IntRep:
    def __init__(self, rep, *, ctxt=30, once=False):
        import colorama
        colorama.init()
        self.stopped = False
        self.rep = rep
        def replace_func(match):
            if self.stopped:
                return match[0]
            context = color_context(match, ctxt=ctxt)
            confirm = key_confirm(context + ':', keys=None, file=sys.stdout, echo=True)
            if confirm in b'\ry':
                if once:
                    self.stopped = True
                if callable(rep):
                    return rep(match)
                return match.expand(rep)
            elif confirm in b'qs\x1b':
                self.stopped = True
                return match[0]
            elif confirm in b'\x03\x04\x1a':
                raise EOFError
            return match[0]
        self.func = replace_func
    def __call__(self, match):
        return self.func(match)
    def __repr__(self):
        rep = self.rep
        try:
            rep = rep.__name__
        except:
            pass
        tup = (self.__class__.__module__, self.__class__.__qualname__, rep)
        return '%s.%s(%s)' % tup
