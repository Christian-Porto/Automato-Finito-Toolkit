def is_final_state(state_name, starting_final_state):
    is_final = False  # Inicializa a variável indicando se é um estado final
    for letter in state_name:
        # Verifica se alguma letra do nome do estado está nos estados finais iniciais
        if letter in starting_final_state:
            is_final = True  # Marca como estado final se encontrar uma correspondência
    return is_final  # Retorna True se for estado final, caso contrário False

def build_final_state_list(state_table, starting_final_state):
    final_list = []  # Cria uma lista para armazenar os estados finais
    for state in state_table:
        # Verifica se o estado atual é um estado final
        if is_final_state(state, starting_final_state):
            final_list.append(state)  # Adiciona o estado à lista de estados finais

    return final_list  # Retorna a lista completa de estados finais
