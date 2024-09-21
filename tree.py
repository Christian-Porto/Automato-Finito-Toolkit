import parser          # Importa o módulo 'parser' para analisar arquivos de entrada
import copy            # Importa o módulo 'copy' para realizar cópias profundas de objetos
from functools import reduce  # Importa 'reduce' do módulo 'functools' para funções de redução
import pprint          # Importa o módulo 'pprint' para impressão formatada de estruturas de dados
import sys             # Importa o módulo 'sys' para manipulações do sistema

sys.setrecursionlimit(3000)  # Define o limite máximo de recursão para 3000

pp = pprint.PrettyPrinter(indent=2)  # Cria um objeto PrettyPrinter com indentação de 2 espaços
known_input_keys = ["0", "1", "epsilon"]  # Chaves de entrada conhecidas (símbolos do autômato)

def get_in(dictionary, keys, default=None):
    """
    Recupera um valor de um dicionário aninhado dado uma lista de chaves.
    """
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys,
        dictionary
    )

def nested_set(dic, keys, value):
    """
    Define um valor em um dicionário aninhado dado uma lista de chaves.
    """
    for key in keys[:-1]:
        if isinstance(dic, str):
            dic = {}  # Se o dicionário atual é uma string, redefine como dicionário vazio
        else:
            dic = dic.setdefault(key, {})  # Avança para o próximo nível do dicionário
    dic[keys[-1]] = value  # Define o valor na chave final

def assoc_in(result_tree, path, val):
    """
    Associa um valor em um dicionário aninhado somente se o caminho não existir.
    """
    if get_in(result_tree, path) is None:
        nested_set(result_tree, path, val)

def follow_transitions(state_tree, state_key, result_tree, calling_state_key=None, path=[]):
    """
    Segue recursivamente as transições de um estado e constrói uma árvore de resultados
    que representa as transições do autômato.
    """
    state = state_tree.get(state_key, None)  # Obtém o estado atual
    if state is not None:
        for possible_transition in known_input_keys:
            state_possible_transition = state.get(possible_transition, None)

            if not state_possible_transition:
                # Não há transição para este símbolo
                path += [state_key]
                cleaned_up_state = {}
                for key in state:
                    cleaned_up_state[key] = state[key][0]  # Obtém o primeiro elemento da lista
                if calling_state_key is None:
                    # Se não há estado chamador, redefine o caminho
                    path = [state_key]
                    continue
                return {"state": cleaned_up_state, "path": path}

            elif state_possible_transition[0] == calling_state_key:
                # Evita ciclos verificando se a transição leva de volta ao estado chamador
                path += [state_key]
                cleaned_up_state = {}
                for key in state:
                    cleaned_up_state[key] = state[key][0]
                return {"state": cleaned_up_state, "path": path}
            else:
                # Continua seguindo as transições recursivamente
                for target_state_key in state_possible_transition:
                    new_path = path
                    if target_state_key == calling_state_key:
                        new_path = path + [possible_transition]
                    elif path and not calling_state_key:
                        new_path = [state_key] + [possible_transition]
                    else:
                        new_path = path + [state_key] + [possible_transition]
                    state_traversal = follow_transitions(
                        state_tree, target_state_key, result_tree, state_key, new_path
                    )
                    if state_traversal.get("state") is None:
                        continue
                    traversed_state = state_traversal["state"]
                    n_path = state_traversal["path"]
                    assoc_in(result_tree, n_path, traversed_state)
    return result_tree

def build_tree(base_map):
    """
    Constrói a árvore de transições do autômato a partir do mapa base.
    """
    tree = {}
    for state_key in base_map:
        tree[state_key] = {}
        follow_transitions(base_map, state_key, tree)
    return tree

"""
                0  ┌─┐epsilon ┌─┐ 1   ┌─┐
            ┌─────►│C├───────►│D├────►│F│
            │      └┬┘        └┬┘     └─┘
       0   ┌┴┐      │          │
   ┌──────►│A│      │          │  0   ┌─┐
   │       └─┘      │          └─────►│E│
┌──┴──┐             │                 └─┘
│state│           1 │
└──┬──┘             │
   │   1   ┌─┐      │
   └──────►│B│◄─────┘
           └─┘

   A -> C -> E

   A { 0: C { epsilon: D { 1: F {}, 0: E {}}
              1: B {}}

O objetivo é seguir cada estado e todas as suas transições.
"""

def first_pass(base_tree):
    """
    Realiza a primeira passagem para limpar a árvore base e construir a árvore de transições inicial.
    """
    cleaned_up_base_tree = copy.deepcopy(base_tree["rt"])  # Copia profunda da árvore base
    del cleaned_up_base_tree["start"]  # Remove o estado inicial
    del cleaned_up_base_tree["end"]    # Remove o estado final

    tree = build_tree(cleaned_up_base_tree)  # Constrói a árvore de transições
    return tree

def find_state_e_closure(tree, state_key, result=[]):
    """
    Encontra o fecho épsilon de um estado dado.
    """
    if state_key not in result:
        result = []
    state = tree.get(state_key)
    e_transition = state.get("epsilon")
    if e_transition is None:
        # Não há transições épsilon; o fecho é o próprio estado
        result = [state_key]
        return result

    for transition in e_transition:
        transition_state = e_transition.get(transition)
        result += state_key
        if not transition_state:
            result += transition
            continue

        r = find_state_e_closure(tree, transition, result)
        if r is not None:
            result += r[0]
    return sorted(set(result))

def get_leaf_states(tree, state_e_closure):
    """
    Obtém os estados folha alcançáveis a partir do fecho épsilon de um estado para cada símbolo de entrada.
    """
    result = {"0": [], "1": []}
    for state_name in state_e_closure:
        state = tree.get(state_name)

        for input_key in ["0", "1"]:
            input_transition = state.get(input_key, None)
            if input_transition:
                transition_name = list(input_transition.keys())[0]
                transition = input_transition.get(transition_name)
                epsilon_transition = transition.get("epsilon", None)
                result[input_key] += transition_name
                if epsilon_transition is not None:
                    if isinstance(epsilon_transition, str):
                        result[input_key] += epsilon_transition

    return result

def to_name(state_keys):
    """
    Converte uma lista de chaves de estado em um único nome de estado (string).
    """
    if isinstance(state_keys, list):
        return "".join(sorted(set(state_keys)))
    else:
        return state_keys

def clean_transitions(transition_map):
    """
    Limpa o mapa de transições removendo duplicatas e ordenando as transições.
    """
    t_map = copy.deepcopy(transition_map)
    for transition_input in transition_map:
        transitions = transition_map[transition_input]
        cleaned_up = sorted(set(transitions))
        t_map[transition_input] = cleaned_up
    return t_map

"""
O que temos até o momento:
- Obter o fecho épsilon de um estado
- Obter os estados que o fecho épsilon pode alcançar
Exemplo:
> "Dê-me o fecho épsilon de A"
>> ["A", "C", "F"]
> "Dê-me as folhas que posso alcançar"
>> {"0": ["B", "D", "E"], "1": ["D", "E"]}

O que precisamos fazer agora:
- Armazenar o fecho épsilon do estado em um dicionário
- Armazenar suas transições/folhas
- Para cada uma das folhas, repetir o processo acima
"""

def recur(tree, state_key, result):
    """
    Constrói recursivamente a tabela de transições do autômato.
    """
    if isinstance(state_key, list):
        state_name = to_name(state_key)
        r = {"0": [], "1": []}
        if state_name in list(result.keys()):
            return {}

        for state in state_key:
            state_closure = []
            state_closure = find_state_e_closure(tree, state)
            state_leaves = get_leaf_states(tree, state_closure)

            for transition in state_leaves:
                leaves = sorted(set(state_leaves[transition]))
                r[transition] += leaves
        cleaned_transitions = clean_transitions(r)

        result[state_name] = cleaned_transitions
        return result

    # Para um único estado
    state_e_closure = find_state_e_closure(tree, state_key)
    state_name = to_name(state_e_closure)
    leaves = get_leaf_states(tree, state_e_closure)
    result[state_name] = leaves
    return result

def handle_recur(tree, state, rr={}, first_key=None):
    """
    Lida com a construção recursiva da tabela de transições.
    """
    leaves = recur(tree, state, rr)
    state_e_transitions = []
    if isinstance(state, list):
        state_e_transitions = state
    else:
        state_e_transitions = find_state_e_closure(tree, state)

    transition_name = to_name(state_e_transitions)
    if first_key is None or first_key in transition_name:
        first_key = transition_name
    next_states = leaves.get(transition_name)
    if next_states:
        for input_transition in next_states:
            next_state = next_states[input_transition]
            if next_state:
                if next_state != state:
                    handle_recur(tree, next_state, rr, first_key)

    return {"rr": rr, "fk": first_key}

def clean_up_final_tree(tree):
    """
    Limpa a árvore final convertendo as transições em nomes de estados.
    """
    res = copy.deepcopy(tree)
    for state_name in tree:
        state = tree[state_name]
        for transition_key in state:
            transition = state[transition_key]
            transition_name = to_name(transition)
            res[state_name][transition_key] = transition_name
    return res

def compare_letters(w, s):
    """
    Compara duas strings e conta o número de letras correspondentes.
    """
    match_count = 0
    for l in w:
        for j in s:
            if l == j:
                match_count += 1
    return match_count

def is_reached_by(tree, state_name):
    """
    Determina quais estados alcançam um determinado estado.
    """
    reached_by = []
    for s in tree:
        state = tree[s]
        for transition_input in state:
            transition = state[transition_input]
            transition_name = to_name(transition)
            if transition_name == state_name and state_name != s:
                reached_by += [s]
    return reached_by

def mount(base_tree, tree):
    """
    Monta o autômato lidando com transições recursivas a partir do estado inicial.
    """
    start = base_tree["rt"]["start"]

    xu = handle_recur(tree, start, {})
    return xu

def get_root(tree, target_state, last=None, res={}, visited=[]):
    """
    Encontra os estados raiz que alcançam o estado alvo.
    """
    for state_name in tree:
        state = tree[state_name]
        for transition_input in state:
            transition = state[transition_input]
            transition_name = to_name(transition)
            last = transition_name
            if last != state_name:
                if transition_name == target_state:
                    if not res.get(last):
                        res[last] = []
                    res[last] += [state_name]
                    if state_name not in visited:
                        visited += [state_name]
                        get_root(tree, state_name, last, res, visited)
    return res

def check_for_loop(child_state, parent_state, child_name, parent_name):
    """
    Verifica se há um loop entre estados filho e pai.
    """
    child_reaches = child_state.values()
    parent_reaches = parent_state.values()
    if child_name in parent_reaches and parent_name in child_reaches:
        return True
    return False

def verifier(tree, state_key):
    """
    Verifica se um estado pode ser mesclado ou removido com base em certas condições.
    """
    for s in tree:
        parent_state = tree.get(s)
        child_state = tree.get(state_key)
        if parent_state is None or child_state is None:
            return {"s": False, "st": s, "ce": False}

        child_state_vals = set(child_state.values())
        parent_state_vals = set(parent_state.values())
        diff = child_state_vals - parent_state_vals
        if state_key in s and state_key != s:
            if child_state == parent_state:
                return {"s": True, "st": s, "ce": True}

            if s in set(child_state.values()) - set(parent_state.values()):
                return {"s": True, "st": s, "ce": False}
        elif s in diff and len(diff) <= 1:
            return {"s": True, "st": s}
        else:
            if child_state == parent_state and state_key != s:
                return {"s": True, "st": s, "ce": True}

def get_reachable_states(tree, state_list):
    """
    Obtém todos os estados alcançáveis a partir de uma lista de estados.
    """
    l = []
    for state_name in state_list:
        state = tree[state_name]
        reachable = list(state.values())
        l += reachable
    return list(set(l))

def in_nested_list(my_list, item):
    """
    Verifica se um item está em uma lista aninhada.
    """
    if item in my_list:
        return True
    else:
        return any(in_nested_list(sublist, item) for sublist in my_list if isinstance(sublist, list))

def list_checker(l1, l2):
    """
    Verifica se algum item em l1 está presente em l2, que pode ser aninhada.
    """
    for item in l1:
        if in_nested_list(l2, item):
            return True
    return False

def paths_for_key(tree, key):
    """
    Encontra todos os caminhos que levam a uma determinada chave na árvore.
    """
    paths = []
    for k in tree:
        state = tree[k]
        for transition_input in state:
            transition = state[transition_input]
            if transition == key:
                paths += [[k, transition_input]]
    return paths

def quadros(tree, to_walk, r={}):
    """
    Realiza a minimização de estados no autômato.
    """
    if to_walk == []:
        return r

    n_walk = sorted(to_walk)
    head, tail = n_walk[0], n_walk[1:]
    xss = verifier(r, head)
    if xss:
        stn_is_reached_by = is_reached_by(r, head)
        if r.get(head) and not stn_is_reached_by:

            if xss["st"] in list(r.keys()):
                parent = xss["st"]
                parent_state = r.get(parent)
                head_state = r.get(head)
                if parent_state == head_state:
                    available = list(r.keys())
                    available_without_current = list(filter(lambda sttt: sttt != head and sttt != parent, available))

                    reachable = get_reachable_states(r, available_without_current)
                    if parent in reachable:
                        to_walk_again = list(r.get(head).values())
                        tail += to_walk_again
                        del r[head]
                    else:
                        comparison = compare_letters(parent, head)
                        if comparison == len(head):
                            del r[head]
                else:
                    available = list(r.keys())
                    available_without_current = list(filter(lambda sttt: sttt != head and sttt != parent, available))
                    reachable = get_reachable_states(tree, available_without_current)
                    if parent in reachable:
                        to_walk_again = list(r.get(head).values())
                        tail += to_walk_again
                        del r[head]
                    else:
                        comparison = compare_letters(parent, head)
                        if comparison == len(head):
                            to_walk_again = list(r.get(head).values())
                            tail += to_walk_again
                            del r[head]
                    quadros(tree, tail, r)
            else:
                parent = xss["st"]
                if r.get(head) == r.get(parent):
                    available = list(r.keys())
                    available_without_current = list(filter(lambda sttt: sttt != head and sttt != parent, available))
                    reachable = get_reachable_states(tree, available_without_current)
                    if parent in reachable and r.get(head):
                        del r[head]

                    quadros(tree, tail, r)
        elif r.get(head) and xss.get("ce"):
            reached_by_set = set(stn_is_reached_by)
            available_states = set(list(r.keys()))
            if reached_by_set.isdisjoint(available_states):
                to_walk_again = list(r.get(head).values())
                tail += to_walk_again
                del r[head]
            else:
                if len(stn_is_reached_by) == 1:
                    available_states = set(list(r.keys()))
                    if xss["st"] in available_states and xss["ce"]:
                        xst = xss["st"]
                        comparison = compare_letters(head, xst)
                        is_loop = check_for_loop(r.get(head), r.get(xst), head, xst)

                        if comparison == len(head) and r.get(head) and not is_loop:
                            paths_to_head = paths_for_key(r, head)
                            paths_to_xst = paths_for_key(r, xst)
                            list_check = list_checker(paths_to_head, paths_to_xst)

                            xst_paths2 = []
                            for n in paths_to_head:
                                xst_paths2 += [to_name(n[0])]
                            if len(paths_to_head) == 1:
                                path1 = paths_to_head[0][0]
                            if list_check or head in xst_paths2:
                                for state_name in r:
                                    state = r[state_name]
                                    for transition_input in state:
                                        transition = state[transition_input]
                                        transition_name = to_name(transition)
                                        if transition_name == head:
                                            r[state_name][transition_input] = xst
                                del r[head]
            quadros(tree, tail, r)
        else:
            quadros(tree, tail, r)
    else:
        quadros(tree, tail, r)
    return r

def flow(base_tree):
    """
    Função principal para processar a árvore base e produzir o autômato minimizado.
    """
    fp = first_pass(base_tree)
    result = mount(base_tree, fp)

    resulting_tree = result["rr"]

    dc = resulting_tree
    dd = clean_up_final_tree(dc)
    my_res = dd
    mt_tree = copy.deepcopy(my_res)

    r1 = copy.deepcopy(mt_tree)
    r1d = {}
    for kr in sorted(r1, key=len):
        r1d[kr] = r1[kr]

    xis = quadros(mt_tree, list(r1d), r1d)

    return {
        "r": xis,
        "final_key": base_tree["rt"]["end"],
        "starting_key": base_tree["rt"]["start"]
    }

if __name__ == "__main__":
    parsed_file = parser.parse_file("dev/input4.txt")  # Analisa o arquivo de entrada
    base_tree = parser.build_base_tree(parsed_file)    # Constrói a árvore base a partir do arquivo analisado
    flow(base_tree)  # Executa a função principal para processar o autômato
