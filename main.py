import parser          # Importa o módulo 'parser' para análise do arquivo de entrada NFA
import tree            # Importa o módulo 'tree' para manipulação da estrutura do autômato
import visualize       # Importa o módulo 'visualize' para gerar visualizações do autômato
import argparse        # Importa o módulo 'argparse' para manipular argumentos de linha de comando
import word            # Importa o módulo 'word' para verificar a aceitação de palavras pelo autômato

if __name__ == "__main__":
    # Cria um parser de argumentos de linha de comando com uma descrição do programa
    argparser = argparse.ArgumentParser(
        description="DFA to NFA converter",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Adiciona o argumento '-i' ou '--input' para especificar o caminho do arquivo NFA de entrada
    argparser.add_argument(
        "-i", "--input",
        required=False,
        help="Path to the NFA input file"
    )
    # Adiciona o argumento '-m' ou '--mode' para selecionar o modo de operação (visualização ou aceitação)
    argparser.add_argument(
        "-m", "--mode",
        default="visualize",
        choices=["visualize", "acceptance"],
        help=(
            "Output mode\n"
            "-visualize: for a visualization of the generated DFA\n"
            "-acceptance: to check if words are accepted by the generated DFA"
        )
    )
    # Adiciona o argumento '-w' ou '--words' para especificar o caminho do arquivo com palavras a serem verificadas
    argparser.add_argument(
        "-w", "--words",
        required=False,
        help="Path to the words input file"
    )

    # Analisa os argumentos fornecidos na linha de comando
    args = argparser.parse_args()
    config = vars(args)  # Converte os argumentos em um dicionário para fácil acesso

    input_path = "dev/input.txt"  # Define um caminho padrão para o arquivo NFA de entrada

    output_mode = config["mode"]  # Obtém o modo de operação selecionado

    # Se um caminho de arquivo de entrada foi fornecido, atualiza o caminho do arquivo NFA
    if config["input"] is not None:
        input_path = config["input"]

    words = config["words"]  # Obtém o caminho do arquivo de palavras, se fornecido

    # Verifica se o modo 'acceptance' foi selecionado sem um arquivo de palavras
    if output_mode == "acceptance" and words is None:
        print(
            "Error: You can only use the acceptance mode if you provide"
            " a path containing a list of words to verify"
        )
        exit(1)  # Encerra o programa com um código de erro

    try:
        # Analisa o arquivo NFA de entrada e constrói a estrutura base do autômato
        parsed_tree = parser.parse_file(input_path)
        built_tree = parser.build_base_tree(parsed_tree)
        # Executa o fluxo principal para converter o NFA em DFA
        st = tree.flow(built_tree)

        # Obtém a tabela de estados, o estado final e o estado inicial do DFA
        state_table = st["r"]
        final_key = st["final_key"]
        starting_key = st["starting_key"]

        if output_mode == "visualize":
            # Gera a visualização do DFA usando o módulo 'visualize'
            visualization_graph = visualize.build_visualization(
                state_table, final_key, starting_key
            )
            print("Visualization Graph:\n")
            print(visualization_graph)  # Imprime a representação do grafo
            visualization_graph.view()  # Abre a visualização em um visualizador externo
        elif output_mode == "acceptance":
            # Informa que irá verificar as palavras do arquivo fornecido contra o DFA gerado
            print(
                "Checking words from file: " + words + " against DFA generated"
                " from file " + input_path
            )

            starting_state_key = built_tree["rt"]["start"]  # Obtém o estado inicial do NFA
            # Verifica se as palavras do arquivo são aceitas pelo DFA
            word.check_words_from_file(words, st, starting_state_key)

    except Exception as e:
        # Captura qualquer exceção que ocorra durante a execução e informa ao usuário
        print("An error occurred. Please check your NFA input file")
        print("Error: " + str(e))
