def color_print(text: str, out=False):
    """

    Estilo:
        :negrito:    :n:
        :italico:    :i:
        :sublinhado: :s:
        :invertido:  :in:


    Cores:
        :branco:     :br:
        :vermelho:   :vm:
        :verde:      :vd:
        :amarelo:    :am:
        :azul:       :az:
        :roxo:       :rx:
        :ciano:      :ci:
        :cinza:      :cz:


    Fundo:
        :fbranco:    :fbc:
        :fvermelho:  :fvm:
        :fverde:     :fvd:
        :famarelo:   :fam:
        :fazul:      :faz:
        :froxo:      :frx:
        :fciano:     :fci:
        :fcinza:     :fcz:


    Finalizar:
        :fim:  :f:   ::

    :param   text: texto que pode receber parametros entre ':<cor>:'
    :param   out: por padrão não retorna
    :return: text com modificações de coloração
    """

    from tools.utils import reg

    # Estilos
    text = reg(text, r':n(egrito)?:', '\033[1m')
    text = reg(text, r':i(talico)?:', '\033[3m')
    text = reg(text, r':s(ublinhado)?:', '\033[4m')
    text = reg(text, r':in(vertido)?:', '\033[7m')

    # Cores
    text = reg(text, r':br(anco)?:', '\033[30m')
    text = reg(text, r':(vermelho|vm):', '\033[31m')
    text = reg(text, r':(verde|vd):', '\033[32m')
    text = reg(text, r':am(arelo)?:', '\033[33m')
    text = reg(text, r':az(ul)?:', '\033[34m')
    text = reg(text, r':(roxo|rx):', '\033[35m')
    text = reg(text, r':ci(ano)?:', '\033[36m')
    text = reg(text, r':(cinza|cz):', '\033[37m')

    # Cor de Fundo
    text = reg(text, r':fbr(anco)?:', '\033[40m')
    text = reg(text, r':(fvermelho|fvm):', '\033[41m')
    text = reg(text, r':(fverde|fvd):', '\033[42m')
    text = reg(text, r':fam(arelo)?:', '\033[43m')
    text = reg(text, r':faz(ul)?:', '\033[44m')
    text = reg(text, r':(froxo|frx):', '\033[45m')
    text = reg(text, r':fci(ano)?:', '\033[46m')
    text = reg(text, r':(fcinza|fcz):', '\033[47m')

    text = reg(text, r':f?(im)?:', '\033[m')

    if out:
        return text
    else:
        print(text)


def color(text):
    return color_print(text, True)


def lin(text='', sym='-', num=50, center=True):
    from re import findall, sub

    if text == '':
        print(sym * num)

    else:

        colors = findall(r'\x1b\[(?:[\d;]+)?m', text)
        csym = len(sub(r'\x1b\[(?:[\d;]+)?m', '', sym))

        cnum = int(num * csym)

        if len(colors) > 0:
            for n in colors:
                cnum += len(n)

        if center:
            text = text.center(cnum)

        print(sym * num)
        print(text)
        print(sym * num)


def menu_simples(*label, prompt='\n> ', mask='{i}) {r}'):
    from time import sleep as wait
    for i in range(0, len(label)):
        r = label[i]
        i = i + 1
        p = eval(f"f'{mask}'")
        print(p)

    while True:
        try:
            r = int(input(f'{prompt}'))
            if 0 < r <= len(label):
                return r
            else:
                color_print(':vm:Opção Inválida! Use uma das opões disponiveis.:f:')
                wait(1)

        except (ValueError, TypeError):
            color_print(':vm:Valor Inválido! Por favor use um número inteiro.:f:')
            wait(1)


def read_int(prompt='Digite um número inteiro'):
    while True:
        try:
            return int(input(prompt))
        except (ValueError, TypeError):
            color_print(':vm:Erro, digite um número inteiro.:f:')


def read_float(prompt='Digite um número real:'):
    while True:
        try:
            return float(input(prompt))
        except (ValueError, TypeError):
            color_print(':vm:Erro, digite um número real:f:')


