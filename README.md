# Trabalho para a disciplina Linguagens formais e autômatos

## Como usar:

``` sh
git clone git@github.com:arthurbarroso/automata.git
cd automata
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Check help messages
python main.py -h 
# Generate graphviz visualization of generated DFA
python main.py -i "dev/input.txt"
# Check if words in `words.txt` are accepted by the DFA generated from `input.txt`
python main.py -i "dev/input.txt" -m acceptance -w "dev/words.txt" 
```

## Definições
### Converter um AFND (com movimentos vazios) em um AFD.
- Alfabeto: {0,1}
- Entrada: um arquivo com a tabela do AFND.
- Formato do arquivo de entrada:
  - Linha 0: a sequência de estados separados por espaço. EX: A B C D E F
  - Linha 1: estado inicial
  - Linha 2: estados finais separados por espaço ( se houver mais de um estado final)
  - Linha 3 em diante: estado atual, espaço, caractere lido, espaço, próximo estado

#### Comando:

``` sh
python main.py -i "<caminho-para-o-nfa>"
# ex: python main.py -i "dev/input.txt"
```

### Dado um conjunto de palavras, determinar se a palavra é reconhecida ou não pelo AFD equivalente gerado na parte 1
- Alfabeto: {0,1}
- Entrada: um arquivo com as palavras a serem reconhecidas
- Uma palavra por linha.
- Saída: um arquivo com todas as palavras e na frente de cada palavra por aceito ou não aceito (reconhecido ou não reconhecido). Por uma palavra por linha.

``` 
Ex: Na linha 1: qwefr aceito
    Na linha 2: abder não aceito
```

#### Comando:
``` sh
python main.py -i "<caminho-para-o-nfa>" -m acceptance -w "caminho-para-o-arquivo-com-palavras"
# ex: python main.py -i "dev/input.txt" -m acceptance -w "dev/words.txt"
```
