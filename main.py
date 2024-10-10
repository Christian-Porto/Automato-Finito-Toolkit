class Automato:
    def __init__(self):
        # Inicializa os componentes do autômato: estados, transições, estado inicial e estados finais
        self.estados = set()
        self.transicoes = {}
        self.estado_inicial = None
        self.estados_finais = set()

    def adicionar_estado(self, estado, final=False):
        # Adiciona um novo estado ao autômato
        # Se o estado for final, ele é adicionado ao conjunto de estados finais
        self.estados.add(estado)
        if final:
            self.estados_finais.add(estado)

    def definir_transicao(self, estado_origem, simbolo, estado_destino):
        # Define uma transição entre estados com um determinado símbolo
        # Se o estado de origem ainda não tem transições, inicializa o dicionário
        if estado_origem not in self.transicoes:
            self.transicoes[estado_origem] = {}
        # Se não houver transição para o símbolo, cria uma nova lista de destinos
        if simbolo not in self.transicoes[estado_origem]:
            self.transicoes[estado_origem][simbolo] = []
        # Adiciona o estado de destino à lista de transições para o símbolo
        self.transicoes[estado_origem][simbolo].append(estado_destino)

    def set_estado_inicial(self, estado):
        # Define o estado inicial do autômato
        self.estado_inicial = estado

    def estados_alcancaveis_por_epsilon(self, estados):
        # Calcula o fecho-ε (ε-closure) para um conjunto de estados, ou seja, todos os estados
        # alcançáveis a partir dos estados dados, usando transições epsilon (representadas por 'h')
        estados_alcancados = set(estados)
        pilha = list(estados)

        # Enquanto houver estados na pilha, processa cada um para buscar novas transições epsilon
        while pilha:
            estado = pilha.pop()
            # Verifica se há transições epsilon ('h') a partir do estado atual
            if estado in self.transicoes and 'h' in self.transicoes[estado]:
                for proximo_estado in self.transicoes[estado]['h']:
                    # Se o estado de destino ainda não foi alcançado, adiciona à pilha e ao conjunto
                    if proximo_estado not in estados_alcancados:
                        estados_alcancados.add(proximo_estado)
                        pilha.append(proximo_estado)

        return estados_alcancados

    def verificar_se_aceita(self, palavra):
        # Verifica se o autômato aceita uma palavra
        # Começa pelo fecho-ε do estado inicial
        estados_alcancaveis = self.estados_alcancaveis_por_epsilon({self.estado_inicial})

        # Para cada símbolo da palavra, atualiza os estados alcançáveis
        for simbolo in palavra:
            novos_estados = set()
            for estado in estados_alcancaveis:
                # Se houver transições para o símbolo, adiciona os estados de destino
                if estado in self.transicoes and simbolo in self.transicoes[estado]:
                    novos_estados.update(self.transicoes[estado][simbolo])

            # Calcula o fecho-ε para os novos estados alcançáveis
            estados_alcancaveis = self.estados_alcancaveis_por_epsilon(novos_estados)

        # Verifica se algum dos estados finais foi alcançado após processar a palavra
        return any(estado in self.estados_finais for estado in estados_alcancaveis)

    # Função para transformar o AFND-ε em AFD
    def converter_para_afd(self):
        # Mapeia conjuntos de estados (tuplas) do AFND-ε para novos estados no AFD
        novos_estados = {}
        afd_transicoes = {}  # Armazena as transições do AFD
        afd_estados_finais = set()  # Armazena os estados finais do AFD

        # O estado inicial do AFD será o fecho-ε do estado inicial do AFND
        estado_inicial_afd = tuple(sorted(self.estados_alcancaveis_por_epsilon({self.estado_inicial})))
        novos_estados[estado_inicial_afd] = 'Q0'  # Nomeia o estado inicial do AFD como Q0
        pilha = [estado_inicial_afd]  # Usamos uma pilha para processar os novos estados

        # Obtém todos os símbolos do autômato, exceto as transições epsilon ('h')
        simbolos = set(s for trans in self.transicoes.values() for s in trans if s != 'h')

        contador_estado = 1  # Contador para nomear os novos estados do AFD
        while pilha:
            estado_atual = pilha.pop()
            afd_transicoes[novos_estados[estado_atual]] = {}  # Inicializa as transições do estado atual

            # Processa cada símbolo do alfabeto
            for simbolo in simbolos:
                novos_conjuntos = set()

                # Para cada estado no conjunto atual, segue as transições para o símbolo
                for estado in estado_atual:
                    if estado in self.transicoes and simbolo in self.transicoes[estado]:
                        novos_conjuntos.update(self.transicoes[estado][simbolo])

                # Calcula o fecho-ε do conjunto de estados alcançados
                novos_conjuntos = self.estados_alcancaveis_por_epsilon(novos_conjuntos)
                if novos_conjuntos:
                    # Organiza o conjunto de estados e transforma em tupla para garantir a unicidade
                    novos_conjuntos = tuple(sorted(novos_conjuntos))
                    if novos_conjuntos not in novos_estados:
                        # Cria um novo estado no AFD se ele ainda não existe
                        novos_estados[novos_conjuntos] = f'Q{contador_estado}'
                        contador_estado += 1
                        pilha.append(novos_conjuntos)  # Adiciona o novo estado à pilha para processar

                    # Adiciona a transição ao AFD
                    afd_transicoes[novos_estados[estado_atual]][simbolo] = novos_estados[novos_conjuntos]

        # Define os estados finais do AFD: se qualquer estado do conjunto original for final, o estado do AFD será final
        for conjunto, nome_estado in novos_estados.items():
            if any(estado in self.estados_finais for estado in conjunto):
                afd_estados_finais.add(nome_estado)

        # Imprime a definição do AFD gerado
        print("\n--- AFD Gerado ---")
        print(f"Estado Inicial: {novos_estados[estado_inicial_afd]}")
        print(f"Estados Finais: {afd_estados_finais}")
        print("Transições:")
        for estado, trans in afd_transicoes.items():
            for simbolo, destino in trans.items():
                print(f"{estado} -- {simbolo} --> {destino}")

        return afd_transicoes, novos_estados[estado_inicial_afd], afd_estados_finais


# Exemplo de uso do autômato
automato = Automato()

# Definindo estados no autômato AFND
automato.adicionar_estado('A')
automato.adicionar_estado('B')
automato.adicionar_estado('C')
automato.adicionar_estado('D')
automato.adicionar_estado('E', final=True)  # Estado E é um estado final
automato.adicionar_estado('F')
automato.adicionar_estado('G')
automato.adicionar_estado('I')

# Definindo as transições do AFND-ε (com transições epsilon representadas por 'h')
automato.definir_transicao('A', 'h', 'C')  # A -> ε -> C
automato.definir_transicao('A', '1', 'B')  # A -> 1 -> B
automato.definir_transicao('A', 'h', 'G')  # A -> ε -> G
automato.definir_transicao('B', '1', 'B')  # B -> 1 -> B
automato.definir_transicao('B', '0', 'F')  # B -> 0 -> F
automato.definir_transicao('C', '0', 'D')  # C -> 0 -> D
automato.definir_transicao('D', '1', 'D')  # D -> 1 -> D
automato.definir_transicao('D', '0', 'E')  # D -> 0 -> E
automato.definir_transicao('D', '0', 'I')  # D -> 0 -> I
automato.definir_transicao('F', 'h', 'G')  # F -> ε -> G
automato.definir_transicao('G', '1', 'I')  # G -> 1 -> I
automato.definir_transicao('I', '0', 'I')  # I -> 0 -> I
automato.definir_transicao('I', '1', 'E')  # I -> 1 -> E

# Definindo o estado inicial do AFND
automato.set_estado_inicial('A')

# Converter o AFND-ε em AFD e imprimir a definição do AFD
afd_transicoes, estado_inicial_afd, estados_finais_afd = automato.converter_para_afd()

# Testando o autômato AFND e AFD com as mesmas palavras
palavras = ['011110', '0111', '11101000', '00', '11', '10001', '00001', '11011', '11010001', '01110001']
print("\n--- Resultados ---")
for palavra in palavras:
    aceita = automato.verificar_se_aceita(palavra)
    print(f"A palavra '{palavra}' é aceita : {aceita}")


