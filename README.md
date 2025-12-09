# Conversor de Gramática Regular para AFD Mínimo

Trabalho de Linguagens Formais e Autômatos - Conversor de GR para AFD Mínimo

## Estrutura do Projeto

- `entrada.txt` - Arquivo contendo a gramática regular em formato BNF
- `main.py` - Script Python principal que realiza a conversão
- `saida_afd.csv` - Arquivo de saída gerado com o AFD mínimo (criado após execução)

## Como Usar (CLI)

1. **Certifique-se de ter Python instalado** (versão 3.6 ou superior)

2. **Edite o arquivo `entrada.txt`** com sua gramática regular no formato:
   ```
   <S> ::= a<A> | e<A> | i<A> | o<A> | u<A>
   <A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | ε
   ```

3. **Execute o script:**
   ```bash
   python main.py
   ```
   ou
   ```bash
   py main.py
   ```
   ou
   ```bash
   python3 main.py
   ```

4. **Verifique o resultado** no arquivo `saida_afd.csv` gerado

## Como Usar (API + Front)

1. Instale dependências do servidor:
   ```bash
   py -m pip install flask
   ```

2. Inicie o backend (porta 5000):
   ```bash
   py server.py
   ```

3. Abra o front (Vue) em `frontend/index.html` no navegador.

4. Selecione o arquivo de gramática `.txt`, clique em **Converter** e baixe o `saida_afd.csv` gerado.

## Formato de Entrada

A gramática deve seguir o formato BNF (Backus-Naur Form):
- Não-terminais entre `<` e `>`
- Produções separadas por `|`
- Terminal seguido de não-terminal: `a<A>`
- Epsilon (vazio): `ε`

## Formato de Saída

O arquivo CSV (separador `;` para Excel em PT-BR) contém:
- `estado`: nome do estado (ex.: Q0, Q1)
- `inicial`: `1` se inicial, `0` caso contrário
- `final`: `1` se final, `0` caso contrário
- Uma coluna para cada símbolo do alfabeto, com o estado de destino ou `-`

## Algoritmos Implementados

1. **Carregamento de Gramática**: Parser BNF que converte regras em autômato finito não-determinístico (AFN)

2. **Determinização (AFN → AFD)**: Algoritmo de construção de subconjuntos (Subset Construction)

3. **Minimização**: Algoritmo baseado em particionamento (similar a Hopcroft):
   - Remoção de estados inalcançáveis
   - Agrupamento de estados equivalentes
   - Refinamento iterativo até convergência

## Exemplo de Execução

Para a gramática de exemplo:
```
<S> ::= a<A> | e<A> | i<A> | o<A> | u<A>
<A> ::= a<A> | e<A> | i<A> | o<A> | u<A> | ε
```

O programa:
1. Carrega a gramática
2. Converte para AFD
3. Minimiza o AFD
4. Salva o resultado em `saida_afd.csv`

## Observações

- O primeiro não-terminal encontrado no arquivo é considerado o símbolo inicial
- Estados finais são identificados por produções com `ε` ou terminais sem não-terminal seguinte
- Estados minimizados são renomeados como Q0, Q1, Q2, etc.

