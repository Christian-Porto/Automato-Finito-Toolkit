import tree     # Importa o módulo 'tree' que contém funções para manipular árvores de autômatos
import parser   # Importa o módulo 'parser' que contém funções para analisar arquivos de entrada
import pprint   # Importa o módulo 'pprint' para impressão formatada de estruturas de dados

pp = pprint.PrettyPrinter(indent=2)  # Cria um objeto PrettyPrinter com indentação de 2 espaços para impressão organizada

def test_first_pass():
    # Analisa o arquivo de entrada 'input.txt' e obtém a representação intermediária do autômato
    parsed_graph = parser.parse_file("dev/input.txt")
    # Constrói a estrutura base do autômato a partir da representação intermediária
    base_graph = parser.build_base_tree(parsed_graph)

    # Executa a primeira passagem para expandir transições épsilon e construir a árvore completa
    st = tree.first_pass(base_graph)

    # Define o resultado esperado após a primeira passagem
    expected_result = {
        'A': {
            '0': {'B': {'0': {'B': {'0': 'B'}}}},
            '1': {'D': {'1': 'D', 'epsilon': 'E'}},
            'epsilon': {
                'C': {'0': {'D': {'1': 'D', 'epsilon': 'E'}}},
                'F': {}
            }
        },
        'B': {'0': {'B': {'0': 'B'}}},
        'C': {'0': {'D': {'1': 'D', 'epsilon': 'E'}}},
        'D': {
            '1': {'D': {'1': 'D', 'epsilon': 'E'}},
            'epsilon': {'E': {'1': 'F'}}
        },
        'E': {'1': {'F': {}}},
        'F': {}
    }

    # Verifica se o resultado obtido é igual ao esperado
    assert st == expected_result

def test_find_state_e_closure():
    # Analisa o arquivo de entrada e constrói a estrutura base do autômato
    parsed_graph = parser.parse_file("dev/input.txt")
    base_graph = parser.build_base_tree(parsed_graph)

    # Executa a primeira passagem para expandir transições épsilon
    st = tree.first_pass(base_graph)
    # Encontra o fecho épsilon do estado 'A'
    r = tree.find_state_e_closure(st, "A")
    # Verifica se o fecho épsilon obtido corresponde ao esperado
    assert r == ["A", "C", "F"]

def test_mount():
    # Analisa o arquivo de entrada e constrói a estrutura base do autômato
    parsed_graph = parser.parse_file("dev/input.txt")
    base_graph = parser.build_base_tree(parsed_graph)

    # Executa a primeira passagem
    fp = tree.first_pass(base_graph)
    # Monta o autômato determinístico a partir do não-determinístico
    graph = tree.mount(base_graph, fp)["rr"]
    # Define o resultado esperado após a montagem
    expected_result = {
        'ACF': {'0': ["B", "D", "E"], '1': ["D", "E"]},
        'B': {'0': ['B'], '1': []},
        'BDE': {'0': ['B'], '1': ["D", "E", "F"]},
        'DE': {'0': [], '1': ["D", "E", "F"]},
        'DEF': {'0': "", '1': ["D", "E", "F"]}
    }
    # Verifica se o grafo montado corresponde ao esperado
    assert graph == expected_result

def test_clean_final():
    # Analisa o arquivo de entrada e constrói a estrutura base do autômato
    parsed_graph = parser.parse_file("dev/input.txt")
    base_graph = parser.build_base_tree(parsed_graph)

    # Executa a primeira passagem
    fp = tree.first_pass(base_graph)
    # Monta o autômato determinístico
    graph = tree.mount(base_graph, fp)["rr"]
    # Limpa a estrutura final do autômato, simplificando os estados
    res = tree.clean_up_final_tree(graph)
    # Define o resultado esperado após a limpeza
    expected_result = {
        'ACF': {'0': "BDE", '1': "DE"},
        'B': {'0': 'B', '1': ""},
        'BDE': {'0': 'B', '1': "DEF"},
        'DE': {'0': "", '1': "DEF"},
        'DEF': {'0': "", '1': "DEF"}
    }
    # Verifica se o resultado limpo corresponde ao esperado
    assert res == expected_result

def test_flow():
    # Analisa o arquivo de entrada e constrói a estrutura base do autômato
    parsed_graph = parser.parse_file("dev/input.txt")
    base_graph = parser.build_base_tree(parsed_graph)

    # Executa todo o fluxo de conversão do NFA para o DFA
    res = tree.flow(base_graph)["r"]
    # Define o resultado esperado após a conversão
    expected_result = {
        'ACF': {'0': "BDE", '1': "DE"},
        'B': {'0': 'B', '1': ""},
        'BDE': {'0': 'B', '1': "DEF"},
        'DE': {'0': "", '1': "DEF"},
        'DEF': {'0': "", '1': "DEF"}
    }
    print("\n---res")
    # Imprime o resultado obtido
    print(res)
    # Verifica se o resultado corresponde ao esperado
    assert res == expected_result

def test_flow_again():
    # Analisa um segundo arquivo de entrada 'input2.txt'
    parsed_graph = parser.parse_file("dev/input2.txt")
    # Constrói a estrutura base do autômato
    base_graph = parser.build_base_tree(parsed_graph)

    print("\n---base_graph")
    # Imprime a estrutura base do autômato
    pp.pprint(base_graph)
    # Executa o fluxo de conversão do NFA para o DFA
    res = tree.flow(base_graph)["r"]
    # Define o resultado esperado após a conversão
    expected_result = {
        'ABCDEFGHI': {'0': 'ABCDEGHI', '1': 'ABCDEFGHI'},
        'ABCDEFI': {'0': 'ABCDEGI', '1': 'ABCDEFI'},
        'ABCDEGHI': {'0': 'ABCDEGHI', '1': 'ABCDEFGHI'},
        'ABCDEGI': {'0': 'ABCDEGHI', '1': 'ABCDEFGHI'},
        'ABCDEI': {'0': 'ABCDEI', '1': 'ABCDEFI'}
    }
    print("\n---res")
    # Imprime o resultado obtido
    pp.pprint(res)
    # Verifica se o resultado corresponde ao esperado
    assert res == expected_result

def test_for_input3():
    # Analisa o arquivo de entrada 'input3.txt'
    parsed_graph = parser.parse_file("dev/input3.txt")
    # Constrói a estrutura base do autômato
    base_graph = parser.build_base_tree(parsed_graph)

    print("\n---base_graph")
    # Imprime a estrutura base do autômato
    pp.pprint(base_graph)
    # Executa o fluxo de conversão do NFA para o DFA
    res = tree.flow(base_graph)["r"]
    # Define o resultado esperado após a conversão
    expected_result = {
        'AC': {'0': 'D', '1': 'BC'},
        'BC': {'0': 'D', '1': 'BC'},
        'D': {'0': '', '1': ''}
    }
    print("\n---res")
    # Imprime o resultado obtido
    pp.pprint(res)
    # Verifica se o resultado corresponde ao esperado
    assert res == expected_result

def test_for_input4():
    # Analisa o arquivo de entrada 'input4.txt'
    parsed_graph = parser.parse_file("dev/input4.txt")
    # Constrói a estrutura base do autômato
    base_graph = parser.build_base_tree(parsed_graph)

    print("\n---base_graph")
    # Imprime a estrutura base do autômato
    pp.pprint(base_graph)
    # Executa o fluxo de conversão do NFA para o DFA
    res = tree.flow(base_graph)["r"]
    # Define o resultado esperado após a conversão
    expected_result = {
        'ABC': {'0': 'D', '1': 'D'},
        'D': {'0': '', '1': 'E'},
        'E': {'0': '', '1': ''}
    }
    print("\n---res")
    # Imprime o resultado obtido
    pp.pprint(res)
    # Verifica se o resultado corresponde ao esperado
    assert res == expected_result

# Comentário: Teste adicional comentado, possivelmente usado para depuração ou desenvolvimento
# def test_mount2():
#     parsed_graph = parser.parse_file("dev/input2.txt")
#     base_graph = parser.build_base_graph(parsed_graph)

#     fp = tree.first_pass(base_graph)
#     graph = tree.mount(base_graph, fp)
#     expected_result = {
#         "ABCDEI": {"0": "ABCDEI", "1": "ABCDEFI"},
#         "ABCDEFI": {"0": "ABCDEGHI", "1": "ABCDEFI"},
#         "ABCDEGHI": {"0": "ABCDEGHI", "1": "ABCDEFGHI"},
#         "ABCDEFGHI": {"0": "ABCDEGHI", "1": "ABCDEFGHI"}
#     }
#     print("\n--")
#     print(graph)
#     assert graph == expected_result
