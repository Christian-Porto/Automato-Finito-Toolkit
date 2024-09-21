import graphviz           # Importa o módulo 'graphviz' para criar visualizações de grafos
import common             # Importa o módulo 'common' que contém funções auxiliares

def seegraph():
    # Função de exemplo para demonstrar a criação de um grafo simples
    dot = graphviz.Digraph(comment="My graph")  # Cria um objeto Digraph com um comentário

    # Adiciona nós ao grafo com identificadores e rótulos
    dot.node('A', 'Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    # Adiciona arestas entre os nós
    dot.edges(['AB', 'AL'])         # Cria arestas de 'A' para 'B' e de 'A' para 'L'
    dot.edge('B', 'L', constraint='false')  # Cria uma aresta de 'B' para 'L' sem restrição de layout
    print(dot.source)               # Imprime a definição do grafo em formato DOT

def build_visualization(state_table, starting_final_state, starting_key):
    """
    Constrói uma visualização do autômato finito determinístico (DFA) usando Graphviz.
    
    Parâmetros:
    - state_table: dicionário representando a tabela de transições do DFA
    - starting_final_state: lista dos estados finais do DFA
    - starting_key: estado inicial do DFA
    """
    processed = []                   # Lista para rastrear estados já processados
    g = graphviz.Digraph()           # Cria um objeto Digraph para o grafo

    # Determina o estado inicial a partir do starting_key
    for kr in sorted(state_table, key=len):
        print("r1dkr: " + str(kr))
        if starting_key in kr:
            starting_state = kr      # Define o estado inicial
            break

    # Itera sobre cada estado na tabela de estados
    for state_name in state_table:
        print("state_name: " + str(state_name) + " processed: " + str(processed))
        if state_name in processed:
            continue                 # Pula estados já processados
        processed += [state_name]    # Marca o estado como processado
        state = state_table[state_name]  # Obtém as transições para o estado atual
        for input_transition in state:
            next_state = state[input_transition]  # Obtém o estado seguinte para a transição atual
            if next_state:
                # Verifica se o estado atual é um estado final
                is_final = common.is_final_state(state_name, starting_final_state)
                # Adiciona o nó do estado atual ao grafo
                g.node(state_name, state_name)
                
                # Define a forma do nó (círculo para estados normais, duplo círculo para estados finais)
                shape_to_use = "circle" if not is_final else "doublecircle"
                g.node(state_name, shape=shape_to_use, arrow="normal")
                # Adiciona uma aresta do estado atual para o próximo estado com o rótulo da transição
                g.edge(state_name, next_state, label=input_transition)

    # Adiciona um nó inicial vazio e uma aresta para o estado inicial
    g.node("", shape="none")
    g.edge("", starting_state)
    return g                          # Retorna o objeto Digraph representando o grafo do DFA
