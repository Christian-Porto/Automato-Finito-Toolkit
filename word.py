import common  # Importa o módulo 'common' que contém funções auxiliares, como 'build_final_state_list'

def is_word_accepted(state_table, word, starting_state_key, final_states=[]):
    is_accepted = False  # Inicializa a variável que indica se a palavra é aceita

    # Obtém o nome do estado inicial a partir da tabela de estados
    starting_state_name = None
    for kr in sorted(state_table, key=len):
        # Verifica se a chave do estado inicial está contida no nome do estado atual
        if starting_state_key in kr:
            starting_state_name = kr  # Define o nome do estado inicial
            break

    current_state_name = starting_state_name  # Define o estado atual como o estado inicial

    if len(word) == 0:
        return False  # Se a palavra é vazia, retorna False (palavra não aceita)

    if len(word) == 1 and current_state_name in final_states:
        return True  # Se a palavra tem um caractere e o estado atual é final, retorna True

    # Itera sobre cada letra da palavra
    for letter in word:
        if letter != "0" and letter != "1":
            # Se a letra não é '0' ou '1', a palavra contém caracteres inválidos
            current_state_name = ""  # Reseta o estado atual
            is_accepted = False
            break  # Interrompe o loop, palavra não é aceita

        transitions = state_table[current_state_name]  # Obtém as transições do estado atual
        next_state = transitions.get(letter)  # Obtém o próximo estado com base na letra atual

        if next_state:
            current_state_name = next_state  # Atualiza o estado atual para o próximo estado
        else:
            # Se não há transição para a letra atual, a palavra não é aceita
            current_state_name = ""  # Reseta o estado atual
            is_accepted = False
            break  # Interrompe o loop

    # Após processar todas as letras, verifica se o estado atual é um estado final
    if current_state_name in final_states:
        is_accepted = True  # A palavra é aceita

    return is_accepted  # Retorna se a palavra é aceita ou não

def check_words_from_file(filename, st, starting_state_key):
    """
    Lê palavras de um arquivo e verifica se cada uma é aceita pelo autômato.

    Parâmetros:
    - filename: nome do arquivo contendo as palavras (uma por linha)
    - st: estrutura do autômato (contendo a tabela de estados e estados finais)
    - starting_state_key: chave do estado inicial do autômato
    """

    state_table = st["r"]  # Obtém a tabela de estados do autômato
    final_key = st["final_key"]  # Obtém a chave dos estados finais
    final_state_list = common.build_final_state_list(state_table, final_key)  # Constrói a lista de estados finais

    line_count = 0  # Inicializa o contador de linhas

    with open(filename) as file:
        line = file.readline()  # Lê a primeira linha do arquivo
        while line:
            clean_word = line.strip()  # Remove espaços em branco no início e fim da linha
            # Verifica se a palavra é aceita pelo autômato
            is_accepted = is_word_accepted(
                state_table, clean_word, starting_state_key, final_state_list
            )
            accepted_word = "sim" if is_accepted else "não"  # Define a resposta como 'sim' ou 'não'
            # Imprime o resultado para a palavra atual
            print(
                "[Linha " + str(line_count) + "] "
                + "Palavra: " + str(clean_word) + " é aceita? " + str(accepted_word)
            )
            line_count += 1  # Incrementa o contador de linhas

            line = file.readline()  # Lê a próxima linha do arquivo
