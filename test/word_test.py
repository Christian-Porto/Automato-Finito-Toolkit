import pytest          # Importa o módulo pytest para escrever e executar testes
import tree            # Importa o módulo 'tree' para manipulação de árvores de autômatos
import sys             # Importa o módulo sys (não está sendo utilizado neste código)
import parser          # Importa o módulo 'parser' para análise de arquivos de entrada
import word            # Importa o módulo 'word' para verificar se uma palavra é aceita pelo autômato
import common          # Importa o módulo 'common' que contém funções auxiliares

def test_word_is_accepted_for_input_one():
    # Analisa o arquivo 'input.txt' e constrói a árvore base do autômato
    parsed_tree = parser.parse_file("dev/input.txt")
    built_tree = parser.build_base_tree(parsed_tree)
    
    # Obtém o estado inicial do autômato
    starting_state_key = built_tree["rt"]["start"]
    
    # Executa o fluxo principal para converter o NFA (Autômato Finito Não Determinístico)
    # em um DFA (Autômato Finito Determinístico)
    st = tree.flow(built_tree)
    
    # Extrai a tabela de estados resultante e a chave do estado final
    state_table = st["r"]
    final_key = st["final_key"]
    
    # Constrói a lista de estados finais a partir da tabela de estados
    final_state_list = common.build_final_state_list(state_table, final_key)
    
    # Verifica se as palavras fornecidas são aceitas pelo autômato
    word1_accepted = word.is_word_accepted(state_table, "01111111111", starting_state_key, final_state_list)
    word2_accepted = word.is_word_accepted(state_table, "0", starting_state_key, final_state_list)
    word3_accepted = word.is_word_accepted(state_table, "000", starting_state_key, final_state_list)
    word4_accepted = word.is_word_accepted(state_table, "011", starting_state_key, final_state_list)
    word5_accepted = word.is_word_accepted(state_table, "", starting_state_key, final_state_list)
    
    # Verifica se os resultados estão de acordo com o esperado
    assert word1_accepted        # Deve ser True (palavra aceita)
    assert word2_accepted        # Deve ser True (palavra aceita)
    assert not word3_accepted    # Deve ser False (palavra não aceita)
    assert word4_accepted        # Deve ser True (palavra aceita)
    assert not word5_accepted    # Deve ser False (palavra não aceita)

def test_word_is_accepted_for_input_two():
    # Analisa o arquivo 'input2.txt' e constrói a árvore base do autômato
    parsed_tree = parser.parse_file("dev/input2.txt")
    built_tree = parser.build_base_tree(parsed_tree)
    
    # Obtém o estado inicial do autômato
    starting_state_key = built_tree["rt"]["start"]
    
    # Executa o fluxo principal para converter o NFA em DFA
    st = tree.flow(built_tree)
    
    # Extrai a tabela de estados resultante e a chave do estado final
    state_table = st["r"]
    final_key = st["final_key"]
    
    # Constrói a lista de estados finais a partir da tabela de estados
    final_state_list = common.build_final_state_list(state_table, final_key)
    
    # Verifica se as palavras fornecidas são aceitas pelo autômato
    word1_accepted = word.is_word_accepted(state_table, "11000110", starting_state_key, final_state_list)
    word2_accepted = word.is_word_accepted(state_table, "0", starting_state_key, final_state_list)
    word3_accepted = word.is_word_accepted(state_table, "0001", starting_state_key, final_state_list)
    word4_accepted = word.is_word_accepted(state_table, "010", starting_state_key, final_state_list)
    word5_accepted = word.is_word_accepted(state_table, "0101", starting_state_key, final_state_list)
    word6_accepted = word.is_word_accepted(state_table, "01011", starting_state_key, final_state_list)
    word7_accepted = word.is_word_accepted(state_table, "010110", starting_state_key, final_state_list)
    
    # Verifica se os resultados estão de acordo com o esperado
    assert word1_accepted    # Deve ser True
    assert word2_accepted    # Deve ser True
    assert word3_accepted    # Deve ser True
    assert word4_accepted    # Deve ser True
    assert word5_accepted    # Deve ser True
    assert word6_accepted    # Deve ser True
    assert word7_accepted    # Deve ser True

if __name__ == "__main__":
    # Executa os testes se o script for executado diretamente
    test_word_is_accepted_for_input_one()
    test_word_is_accepted_for_input_two()
    print("\n----[WORD_TEST] TESTS RAN FINE [WORD_TEST]----")  # Imprime uma mensagem indicando que os testes foram bem-sucedidos
