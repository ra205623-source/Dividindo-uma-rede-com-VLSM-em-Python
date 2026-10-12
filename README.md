Dividindo uma rede com VLSM em Python
O problema

Com uma rede 192.168.10.0/24 e quatro setores de tamanhos bem diferentes (100, 50, 25 e 2 hosts), a divisão em sub-redes iguais desperdiça endereço. Para atender o setor de 100 hosts, todas as sub-redes teriam que ser /25, e a ligação WAN, que precisa de 2 endereços, ficaria com 126.

O VLSM (Variable Length Subnet Masking) resolve isso dando a cada setor uma máscara do tamanho certo.

A ideia

O algoritmo tem três passos:

Ordenar do maior para o menor. Blocos grandes exigem alinhamento maior. Se os pequenos vierem primeiro, sobram buracos que o bloco grande não consegue usar.
Calcular o bloco mínimo. Cada sub-rede precisa de hosts + 2 endereços, por causa do endereço de rede e do broadcast. O tamanho do bloco é a menor potência de 2 que atende essa conta.
Alinhar e alocar. O início de um bloco de tamanho N precisa ser múltiplo de N. Se o ponteiro atual não for, ele avança até o próximo múltiplo.
O ponto principal do código

O cálculo dos bits de host costuma ser feito com ceil(log2(hosts + 2)). Aqui usei um atalho com inteiros:

python
bits = (hosts + 1).bit_length()

bit_length() devolve quantos bits são necessários para representar o número. Para hosts + 2 ser no máximo 2^bits, basta olhar hosts + 1. Isso evita ponto flutuante e erros de arredondamento. Alguns exemplos:

Hosts	hosts + 2	bits	Bloco	Prefixo
2	4	2	4	/30
25	27	5	32	/27
50	52	6	64	/26
100	102	7	128	/25

O alinhamento é uma linha:

python
if ini % tam:
    ini += tam - ini % tam

Se a posição atual já é múltiplo do bloco, nada acontece. Caso contrário, ela avança o mínimo necessário.

Resultado
Setor      Pedido                Rede          Máscara  Úteis
Vendas        100     192.168.10.0/25  255.255.255.128    126
TI             50   192.168.10.128/26  255.255.255.192     62
RH             25   192.168.10.192/27  255.255.255.224     30
Link WAN        2   192.168.10.224/30  255.255.255.252      2

Os blocos ocupam do .0 ao .227, sem sobreposição. Sobram 28 endereços (.228 a .255) para crescimento.

Limitações
O script trata só IPv4. A biblioteca ipaddress também aceita IPv6, mas a lógica de máscara e alocação seria diferente.
Quando falta espaço, o erro aparece como traceback. Em uma versão mais completa, o main deveria capturar o ValueError e mostrar uma mensagem simples.
Os pedidos estão fixos no código. Um próximo passo natural é ler de argumentos ou de um arquivo CSV.
Conclusão

Com ipaddress, ordenação e uma conta de alinhamento, dá para fazer um VLSM correto em cerca de 15 linhas. O que mais ajuda a entender o problema é perceber que alinhar blocos a potências de 2 é a mesma lógica que se faz à mão na prova de redes.
