from tools.utils import edfile, reif, reg, cl
from tools.design import menu_simples, color

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

# Padrao usando apenas o mac + nome

def_eid = [['{mac.upper()} {name}', r'..:(..):(..):(..):..:.. (VIVO(FIBRA)?|GVT)-(\w+)', r'$1$2$3$6'],
           ['{mac.upper()} {name}', r'..:..:(..):..:..:.. (NET|CLARO)_[25]G(\w+)', r'$1$3'],
           ['{mac} {name}', r'..:(..):(..):..:..:(..) VIVO-(\w+)-[25]G', r'$1$2$4$3']]


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
        nets = eval(nets)[1]

    return nets


# Copia texto
def clip(string):
    droid.setClipboard(string)


# Tenta obter a senha padrão com o mac + nome_da_rede
def getkeys(mac, name):
    passwd = []
    global def_eid

    for mask in def_eid:
        mask[0] = eval(f"f'{mask[0]}'")
        key = reg(*mask)

        if mask[0] != key:
            passwd = key

    return passwd

getkeys('11:aa:bb:cc:EE:dd', 'VIVO-1234')
# Programa Principal

# while True:
#     for net in nets:
#         eid = net['ssid']
#         menu_simples( prompt='>>> ', mask=color(':n::vm:[{i}]--:az:[{r}]::'))
