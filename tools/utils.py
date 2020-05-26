#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def sh(cmd):
    from subprocess import call
    return call(cmd)


def cl():
    if __file__[1] == ':':
        sh('cls')
    else:
        sh('clear')


def rsh(cmd):
    from subprocess import getstatusoutput
    return getstatusoutput(cmd)


def pip(command, pkg):
    sh(f'pip {command} {pkg}')


def reg(string, regex, replace=None):
    """
    Busca ou substituí expressões regulares

    :param string:      Texto a ser usado
    :param regex:       Expressão Regular a ser buscada
    :param replace:     Substitui padrões equivalentes e usa '(grupos)' -> \1 \2 \3... ou $1 $2 $3...

    :return:            Retorna lista de padrões encontrados ou a string substituída

    Exemplo:

    reg('Teste123', r'[^\\d]+\\d+')
    ['Teste123']

    reg('Teste123', r'([^\\d]+)(\\d+)')
    [('Teste', '123')]

    reg('Teste123', r'([^\\d]+)(\\d+)', r'\\2 $1')
    123 Teste
    """
    from re import findall, sub

    if replace is None:
        return findall(regex, string)

    else:
        replace = sub(r'\$(\d+)', r'\\\1', replace)

        return sub(regex, replace, string)


def reif(string, regex):
    return len(reg(string, regex)) > 0


def edfile(path, w='', append=False, encoding='utf-8'):
    if w == '':
        file = open(path, encoding=encoding)
        return file.read()

    elif append:
        file = open(path, 'a', encoding=encoding)
        file.write(w)

    else:
        file = open(path, 'w', encoding='utf-8')
        file.write(w)

    file.close()


def pyargs():
    from sys import argv

    if '.py' in argv[0]:
        del argv[0]
    else:
        del argv[0:1]

    return argv


def shargs(func):
    from inspect import signature as sig
    from sys import argv

    if '.py' in argv[0]:
        del argv[0]
    else:
        del argv[0:1]

    if argv[0] in ('-h', '--help'):
        help(func)
        exit()

    sig = sig(func)
    params = sig.parameters.values()

    args = []
    kwargs = {}

    for par in params:
        key = par.name
        mod = par.kind
        typ = 0

        if len(dir(par.default)) != 26:
            typ = type(par.default)
        elif len(dir(par.annotation)) != 26:
            typ = par.annotation

        if typ not in [str, int, float, bool, list, tuple]:
            del typ

        _arg = par.POSITIONAL_OR_KEYWORD
        _args = par.VAR_POSITIONAL
        _kwargs = par.VAR_KEYWORD

        _pos = par.POSITIONAL_ONLY
        _key = par.KEYWORD_ONLY

        if len(argv) > 0:

            if mod in (_arg, _pos):
                if f'--{key}' in argv:
                    i = argv.index(f'--{key}')

                    if 'typ' in locals():
                        val = typ(argv[i + 1])
                    else:
                        val = argv[i + 1]

                    args.append(val)
                    del argv[i]
                    del argv[i]

                else:

                    if 'typ' in locals():
                        val = typ(argv[0])
                    else:
                        val = argv[0]

                    args.append(val)
                    del argv[0]

            elif mod == _args:

                s = e = 0
                for a in argv:

                    if 'typ' in locals():
                        val = typ(a)
                    else:
                        val = a

                    if f'--' in a:
                        break
                    else:
                        args.append(val)
                        e += 1

                del argv[s:e]

            else:
                if f'--{key}' in argv:
                    i = argv.index(f'--{key}')

                    if 'typ' in locals():
                        val = typ(argv[i + 1])
                    else:
                        val = argv[i + 1]

                    kwargs[key] = val

    return func(*args, **kwargs)


def regfile(path, regex, replace=None, encoding='utf-8'):
    text = edfile(path)

    if replace is None:
        text = reg(text, regex)

    else:
        text = reg(text, regex, replace)
        edfile(path, text, encoding=encoding)

    return text


def suglob(path, recursive=False):
    from glob import glob
    from os.path import expanduser

    path = expanduser(path)

    paths = glob(path, recursive=recursive)

    return paths


def openbrowser(url, new=2):
    from webbrowser import open

    open(url, new=new)


def sysname():
    from platform import system

    return system()
