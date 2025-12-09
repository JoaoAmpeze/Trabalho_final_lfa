import csv

class Automato:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = {} 
        self.estado_inicial = None
        self.estados_finais = set()

    def adicionar_transicao(self, origem, simbolo, destino):
        if origem not in self.transicoes:
            self.transicoes[origem] = {}
        if simbolo not in self.transicoes[origem]:
            self.transicoes[origem][simbolo] = set()
        self.transicoes[origem][simbolo].add(destino)
        
        self.estados.add(origem)
        self.estados.add(destino)
        
        if simbolo and simbolo != 'ε':
            self.alfabeto.add(simbolo)

def carregar_gramatica(caminho_arquivo):
    print(f"--- Carregando e Validando Gramática de {caminho_arquivo} ---")
    afn = Automato()
    estado_aceitacao = "Z_FINAL"
    erros = []

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8-sig') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        raise ValueError(f"[ERRO CRÍTICO] O arquivo '{caminho_arquivo}' não foi encontrado.")

    primeira_linha = True

    for numero_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        if not linha:
            continue

        if "::=" not in linha:
            erros.append(f"Linha {numero_linha}: faltando '::=' em '{linha}'")
            continue

        lado_esq, lado_dir = linha.split("::=", 1)
        origem = lado_esq.strip()

        if not (origem.startswith('<') and origem.endswith('>')):
            erros.append(f"Linha {numero_linha}: lado esquerdo '{origem}' deve estar entre < > (ex: <S>)")
            continue

        if primeira_linha:
            afn.estado_inicial = origem
            primeira_linha = False

        producoes = [p.strip() for p in lado_dir.split("|")]

        for prod in producoes:
            if prod == 'ε' or prod == '':
                afn.estados_finais.add(origem)
            elif '<' in prod and '>' in prod:
                if prod.count('<') > 1:
                    erros.append(f"Linha {numero_linha}: produção '{prod}' tem mais de um não-terminal (GR aceita apenas um).")
                try:
                    partes = prod.split('<')
                    terminal = partes[0].strip()
                    destino = '<' + partes[1]
                    if not destino.endswith('>'):
                        erros.append(f"Linha {numero_linha}: faltando '>' em '{prod}'")
                        continue
                    if terminal:
                        afn.adicionar_transicao(origem, terminal, destino)
                    else:

                        pass
                except IndexError:
                    erros.append(f"Linha {numero_linha}: formato inválido em '{prod}'")
            else:
                afn.adicionar_transicao(origem, prod, estado_aceitacao)
                afn.estados_finais.add(estado_aceitacao)

    if erros:
        resumo = "\n".join(f"[ERRO DE SINTAXE] {e}" for e in erros)
        raise ValueError(f"Erros encontrados na gramática:\n{resumo}")

    return afn

def converter_afn_para_afd(afn):
    print("--- Convertendo GR (AFN) para AFD ---")
    afd = Automato()
    afd.alfabeto = afn.alfabeto
    
    # Verifica se encontrou estado inicial, senão pega o primeiro que aparecer
    if not afn.estado_inicial and afn.estados:
        afn.estado_inicial = list(afn.estados)[0]

    fila = [tuple([afn.estado_inicial])]
    processados = set()
    
    afd.estado_inicial = str(tuple([afn.estado_inicial]))
    
    while fila:
        estados_atuais = fila.pop(0)
        nome_estado_atual = str(estados_atuais)
        
        if nome_estado_atual in processados:
            continue
        processados.add(nome_estado_atual)
        
        for sub_estado in estados_atuais:
            if sub_estado in afn.estados_finais:
                afd.estados_finais.add(nome_estado_atual)
                break
        
        for simbolo in sorted(list(afn.alfabeto)):
            proximos_estados = set()
            for sub_estado in estados_atuais:
                if sub_estado in afn.transicoes and simbolo in afn.transicoes[sub_estado]:
                    proximos_estados.update(afn.transicoes[sub_estado][simbolo])
            
            if proximos_estados:
                proximos_ordenados = tuple(sorted(list(proximos_estados)))
                nome_proximo = str(proximos_ordenados)
                afd.adicionar_transicao(nome_estado_atual, simbolo, nome_proximo)
                
                if nome_proximo not in processados:
                    fila.append(proximos_ordenados)
    return afd

def minimizar_afd(afd):
    print("--- Minimizando AFD ---")

    alcancaveis = set()
    fila = [afd.estado_inicial]
    alcancaveis.add(afd.estado_inicial)
    
    idx = 0
    while idx < len(fila):
        atual = fila[idx]
        idx += 1
        if atual in afd.transicoes:
            for simb in afd.transicoes[atual]:
                destinos = afd.transicoes[atual][simb]
                for d in destinos:
                    if d not in alcancaveis:
                        alcancaveis.add(d)
                        fila.append(d)
    
    novos_estados = alcancaveis
    novos_finais = {e for e in afd.estados_finais if e in alcancaveis}
    novas_transicoes = {e: v for e, v in afd.transicoes.items() if e in alcancaveis}
    
    
    P = [novos_finais, novos_estados - novos_finais]
    P = [g for g in P if g]

    while True:
        novo_P = []
        for grupo in P:
            if len(grupo) <= 1:
                novo_P.append(grupo)
                continue
            
            subgrupos = {}
            for estado in grupo:
                assinatura = []
                for simbolo in sorted(list(afd.alfabeto)):
                    destino = None
                    if estado in novas_transicoes and simbolo in novas_transicoes[estado]:
                        dest = list(novas_transicoes[estado][simbolo])[0]
                        for i, g_verif in enumerate(P):
                            if dest in g_verif:
                                destino = i
                                break
                    assinatura.append((simbolo, destino))
                assinatura = tuple(assinatura)
                
                if assinatura not in subgrupos:
                    subgrupos[assinatura] = set()
                subgrupos[assinatura].add(estado)
            
            for sub in subgrupos.values():
                novo_P.append(sub)
        
        if len(novo_P) == len(P):
            break
        P = novo_P

    # Reconstroi
    afd_min = Automato()
    mapa_estados = {}
    
    for i, grupo in enumerate(P):
        nome_grupo = f"Q{i}"
        for estado in grupo:
            mapa_estados[estado] = nome_grupo
        if any(e in novos_finais for e in grupo):
            afd_min.estados_finais.add(nome_grupo)
            
    afd_min.estado_inicial = mapa_estados[afd.estado_inicial]
    afd_min.alfabeto = afd.alfabeto
    
    # refaz o processo sobre transições antigas para criar as novas
    for estado_antigo, trans in novas_transicoes.items():
        novo_origem = mapa_estados[estado_antigo]
        for simb, destinos in trans.items():
            destino_antigo = list(destinos)[0]
            if destino_antigo in mapa_estados:
                novo_destino = mapa_estados[destino_antigo]
                afd_min.adicionar_transicao(novo_origem, simb, novo_destino)
                
    return afd_min

def salvar_csv(afd, nome_arquivo):
    print(f"--- Salvando resultado em {nome_arquivo} ---")

    alfabeto_ordenado = sorted(list(afd.alfabeto))
    fieldnames = ['estado', 'inicial', 'final'] + alfabeto_ordenado

    # MUDANÇA IMPORTANTE: delimiter=';' para Excel em Português
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        estados_ordenados = sorted(list(afd.estados))

        for estado in estados_ordenados:
            linha = {
                'estado': estado,
                'inicial': '1' if estado == afd.estado_inicial else '0',
                'final': '1' if estado in afd.estados_finais else '0'
            }

            transicoes_estado = afd.transicoes.get(estado, {})

            for simbolo in alfabeto_ordenado:
                destinos = transicoes_estado.get(simbolo)
                if destinos:
                    linha[simbolo] = list(destinos)[0]
                else:
                    linha[simbolo] = '-'

            writer.writerow(linha)


if __name__ == "__main__":
    afn = carregar_gramatica("entrada.txt")
    afd = converter_afn_para_afd(afn)
    afd_minimo = minimizar_afd(afd)
    salvar_csv(afd_minimo, "saida_afd.csv")
    print("Sucesso! Abra o arquivo saida_afd.csv")