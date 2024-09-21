import pprint  # Importa o módulo pprint para impressão formatada de estruturas de dados
import parser  # Importa o módulo personalizado 'parser' para analisar o arquivo de entrada
from lark import Tree, Token  # Importa Tree e Token da biblioteca lark para trabalhar com árvores sintáticas

def test_parse_file():
    pp = pprint.PrettyPrinter(indent=2)  # Cria um objeto PrettyPrinter com indentação de 2 espaços
    expected_answer = {
        0: {
            'meaning': 'all_states',  # Significado: todos os estados do autômato
            'parsed_line': Tree(
                Token('RULE', 'state_sequence'),  # Árvore sintática representando uma sequência de estados
                [
                    Token('STATE', 'A'), Token('STATE', 'B'), Token('STATE', 'C'),
                    Token('STATE', 'D'), Token('STATE', 'E'), Token('STATE', 'F')
                ]
            ),
            'tree': {'state_sequence': ['A', 'B', 'C', 'D', 'E', 'F']}  # Representação simplificada da sequência de estados
        },
        1: {
            'meaning': 'initial_state',  # Significado: estado inicial do autômato
            'parsed_line': Tree(
                Token('RULE', 'state_sequence'),
                [Token('STATE', 'A')]
            ),
            'tree': {'state_sequence': ['A']}
        },
        2: {
            'meaning': 'final_states',  # Significado: estados finais do autômato
            'parsed_line': Tree(
                Token('RULE', 'state_sequence'),
                [Token('STATE', 'F')]
            ),
            'tree': {'state_sequence': ['F']}
        },
        3: {
            'meaning': 'state_transition',  # Significado: transição entre estados
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'A'), Token('CHARACTER_INPUT', '0'), Token('STATE', 'B')
                ]
            ),
            'tree': {'state_change': ['A', '0', 'B']}
        },
        4: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'B'), Token('CHARACTER_INPUT', '0'), Token('STATE', 'B')
                ]
            ),
            'tree': {'state_change': ['B', '0', 'B']}
        },
        5: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'A'), Token('EPSILON', 'epsilon'), Token('STATE', 'C')
                ]
            ),
            'tree': {'state_change': ['A', 'epsilon', 'C']}
        },
        6: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'C'), Token('CHARACTER_INPUT', '0'), Token('STATE', 'D')
                ]
            ),
            'tree': {'state_change': ['C', '0', 'D']}
        },
        7: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'A'), Token('CHARACTER_INPUT', '1'), Token('STATE', 'D')
                ]
            ),
            'tree': {'state_change': ['A', '1', 'D']}
        },
        8: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'D'), Token('CHARACTER_INPUT', '1'), Token('STATE', 'D')
                ]
            ),
            'tree': {'state_change': ['D', '1', 'D']}
        },
        9: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'D'), Token('EPSILON', 'epsilon'), Token('STATE', 'E')
                ]
            ),
            'tree': {'state_change': ['D', 'epsilon', 'E']}
        },
        10: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'E'), Token('CHARACTER_INPUT', '1'), Token('STATE', 'F')
                ]
            ),
            'tree': {'state_change': ['E', '1', 'F']}
        },
        11: {
            'meaning': 'state_transition',
            'parsed_line': Tree(
                Token('RULE', 'state_change'),
                [
                    Token('STATE', 'A'), Token('EPSILON', 'epsilon'), Token('STATE', 'F')
                ]
            ),
            'tree': {'state_change': ['A', 'epsilon', 'F']}
        }
    }

    actual_answer = parser.parse_file("dev/input.txt")  # Chama a função parse_file para analisar o arquivo de entrada
    print("\n[TEST_PARSE_FILE][ANSWER]:\n")
    pp.pprint(actual_answer)  # Imprime o resultado obtido de forma formatada
    assert actual_answer == expected_answer  # Verifica se o resultado obtido é igual ao esperado

def test_build_tree():
    pp = pprint.PrettyPrinter(indent=2)  # Cria um objeto PrettyPrinter com indentação de 2 espaços
    expected_answer = {
        'epsilon_transitions': {'A': ['C', 'F'], 'D': ['E']},  # Mapeia estados para suas transições épsilon
        'rt': {  # Tabela de transições regulares do autômato
            'A': {'0': ['B'], '1': ['D'], 'epsilon': ['C', 'F']},
            'B': {'0': ['B']},
            'C': {'0': ['D']},
            'D': {'1': ['D'], 'epsilon': ['E']},
            'E': {'1': ['F']},
            'F': {},
            'end': ['F'],  # Lista de estados finais
            'start': 'A'   # Estado inicial
        }
    }

    parsed_file = parser.parse_file("dev/input.txt")  # Analisa o arquivo de entrada e retorna a representação intermediária
    actual_answer = parser.build_base_tree(parsed_file)  # Constrói a estrutura do autômato a partir da representação intermediária
    print("\n[test_build_tree][answer]:\n")
    pp.pprint(actual_answer)  # Imprime a estrutura construída de forma formatada
    assert actual_answer == expected_answer  # Verifica se a estrutura construída corresponde ao esperado

if __name__ == "__main__":
    test_parse_file()  # Executa o teste para a função parse_file
    test_build_tree()  # Executa o teste para a função build_base_tree
    print("\n----[PARSER_TEST] TESTS RAN FINE [PARSER_TEST]----")  # Indica que os testes foram executados com sucesso
