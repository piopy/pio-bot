import random

dieta=''
uovo=False
legumi=False


def update(booleano):
    global uovo
    uovo=booleano

def scegli2(nome,lista):
    global legumi
    c=random.choice(lista) 
    if 'Pranzo' in nome and 'legumi' in c: legumi=True
    if legumi==True and 'Cena' in nome:
        ok=False
        while ok==False:
            if 'legumi' in c:
                c=random.choice(lista)
                c=c.replace('\n',' ')
            else: ok=True
    else: ok=True
    return c

def scegli(nome,componenti):
    if 'Alternativa senza' in nome: nome='Colazione'
    res=''+nome+': '
    componenti=componenti.split('+')
    for c in componenti:
        c=c.replace('\n',' ')
        if '$' in c:
            m_choice=c.split('$')
            sceltamul=scegli2(nome,m_choice)
            res+=sceltamul+' - '
        else: res+=c+' - '
    return res

if __name__ == "__main__":
    with open('diet_sample.txt','r',encoding='utf-8') as f:
        dieta=f.read()
    
    pasti=dieta.split('#')
    final=''
    if uovo:pasti.pop(1)
    else: pasti.pop(0)
    for p in pasti:
        p=p.split(':')
        nome=p[0]
        componenti=p[1]
        scelta=scegli(nome,componenti)
        final+=scelta+'\n'
    print(final)