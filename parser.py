from lark import Lark, Transformer, Token  # Importa as classes necessárias da biblioteca Lark para parsing

class GrammarTransformer(Transformer):
    def STATE(self, items):
        (s,) = items  # Desempacota o item da lista
        return s      # Retorna o estado como uma string

    def EPSILON(self, item: Token):
        return item.value  # Retorna o valor do token EPSILON

    def CHARACTER_INPUT(self, items):
        (s,) = items       # Desempacota o item da lista
        return s           # Retorna o caractere de entrada ('0' ou '1')

    def state_sequence(self, items):
        return {"state_sequence": items}  # Retorna um dicionário com a sequência de estados

    def state_change(self, items):
        return {"state_change": items}    # Retorna um dicionário com a mudança de estado

    def description(self, items):
        return items  # Retorna os itens analisados

# Definição da gramática para analisar o arquivo de entrada
grammar = r"""
STATE: UCASE_LETTER                      // Define um estado como uma letra maiúscula
CHARACTER_INPUT: /[0-1]{1}/              // Define a entrada como '0' ou '1'
EPSILON: /epsilon/                       // Define a transição épsilon

?description: (state_sequence | state_change)*   // A descrição pode ser uma sequência de estados ou mudanças de estado
state_sequence: STATE (" " STATE)*               // Sequência de estados separados por espaços
state_change: STATE (" " (CHARACTER_INPUT | EPSILON) " " STATE)+  // Mudança de estado com entrada ou épsilon

%import common.WORD
%import common.NEWLINE
%import common.UCASE_LETTER
%ignore NEWLINE                           // Ignora quebras de linha
"""

# Dicionário que mapeia o número da linha para seu significado
line_count_meaning = {
    0: 'all_states',       # Linha 0 contém todos os estados
    1: 'initial_state',    # Linha 1 contém o estado inicial
    2: 'final_states',     # Linha 2 contém os estados finais
    3: 'state_transition'  # Linha 3 em diante contém as transições
}

def parse_file(filename):
    l = Lark(grammar, start="description")  # Cria um parser com a gramática definida
    line_count = 0
    tree = {}                               # Dicionário para armazenar a árvore sintática de cada linha

    with open(filename) as file:
        line = file.readline()              # Lê a primeira linha do arquivo
        while line:
            # Analisa a linha usando o parser
            parsed_line = l.parse(line)
            # Transforma a árvore sintática em uma estrutura de dados manipulável
            result_tree = GrammarTransformer().transform(parsed_line)
            # Obtém o significado da linha baseado no número da linha
            meaning = line_count_meaning.get(line_count, "state_transition")
            tree[line_count] = {}                   # Inicializa o dicionário para esta linha
            tree[line_count]['parsed_line'] = parsed_line  # Armazena a árvore sintática original
            tree[line_count]["tree"] = result_tree         # Armazena a árvore transformada
            tree[line_count]["meaning"] = meaning          # Armazena o significado da linha
            line_count += 1                        # Incrementa o contador de linhas
            line = file.readline()                 # Lê a próxima linha do arquivo
    return tree  # Retorna o dicionário com todas as linhas analisadas

def build_base_tree(tree):
    epsilon_transitions = {}  # Dicionário para armazenar transições épsilon
    rt = {}                   # Dicionário para representar a tabela de transições do autômato

    for node in tree:
        # Construção da estrutura do autômato a partir dos dados analisados
        if node == 0:
            # Linha 0: contém todos os estados do autômato
            for s in tree[node]['tree']['state_sequence']:
                rt[s] = {}  # Inicializa o dicionário de transições para cada estado
        if node == 1:
            # Linha 1: define o estado inicial
            rt['start'] = tree[node]['tree']['state_sequence'][0]  # Armazena o estado inicial
        if node == 2:
            # Linha 2: define os estados finais
            rt['end'] = tree[node]['tree']['state_sequence']  # Armazena a lista de estados finais
        if node > 2:
            # Linhas 3 em diante: definem as transições entre estados
            state_change = tree[node]['tree']['state_change']  # Obtém a transição
            starting_point = state_change[0]                   # Estado de origem
            transition_input = state_change[1]                 # Símbolo de entrada ou épsilon
            ending_point = state_change[2]                     # Estado de destino

            # Verifica se já existem transições para este estado com este símbolo de entrada
            existing_transitions_for_this_input = rt.get(starting_point).get(transition_input)

            if transition_input == 'epsilon':
                # Se a transição é épsilon, armazena em epsilon_transitions
                existing_epsilon_for_this_input = epsilon_transitions.get(starting_point)
                if existing_epsilon_for_this_input is None:
                    epsilon_transitions[starting_point] = [ending_point]  # Cria uma nova lista
                else:
                    existing_epsilon_for_this_input.append(ending_point)  # Adiciona à lista existente

            if existing_transitions_for_this_input is None:
                # Se não há transições existentes para este símbolo, cria uma nova entrada
                rt[starting_point][transition_input] = [ending_point]
            else:
                # Se já existe, adiciona o estado de destino à lista
                existing_transitions_for_this_input.append(ending_point)

    return {"rt": rt, "epsilon_transitions": epsilon_transitions}  # Retorna a estrutura completa do autômato
