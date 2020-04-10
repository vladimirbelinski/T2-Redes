# Redes de Computadores - Camada de Transporte

Trabalho apresentado ao Curso de Ciência da Computação da Universidade Federal
da Fronteira Sul - UFFS, Campus Chapecó, como requisito parcial para aprovação
no componente curricular Redes de Computadores - 2016.2, sob orientação do
professor Dr. Claunir Pavan.

## Solicitação do trabalho

Implemente dois programas na linguagem de sua eleição. Um se chamará
“cliente” e outro “servidor”.

**Cliente:**
- Inicia por linha de comando com três argumentos (ipserver, porta, pedido),
onde "ipserver" é o endereço de IP do servidor, “porta” é o número da porta
em que o servidor atende e “pedido” é um arquivo texto em que as linhas têm
o seguinte formato (produto, quantidade, valor unitario);
- O cliente usa TCP para se conectar ao servidor, lê o arquivo texto e envia
para o servidor.

**Servidor:**
- Inicia por linha de comando (pode usar porta dinâmica ou por argumento);
- Cria um socket na porta especificada, escuta e aceita conexões de clientes;
- Usa threads para manipular múltiplos clientes;
- Devolve o número de itens distintos (contar as linhas do arquivo) e a soma
com o valor total do pedido (somatório de (quantidade * valor)).


## Solução implementada

A implementação do trabalho da camada de transporte pode ser encontrada nos
arquivos servidor.py, cliente.py, thread.py, servidorgui.py e clientegui.py,
onde os dois últimos apresentam uma versão gráfica da aplicação proposta nos
dois primeiros.

### Preparação do ambiente

Para o funcionamento dos programas é necessário ter instalado na máquina o
Python3 e o Tkinter (pacote utilizado para a interface gráfica). Caso esteja
utilizando um ambiente LINUX (e.g. Ubuntu ou Elementary) basta fazer:

sudo apt-get update
sudo apt-get install python3-tk

### Execução

Os comandos abaixo foram testados no Elementary OS, uma distribuição de Linux
baseada em Ubuntu. Para outros SOs ou distribuições podem ser necessárias
algumas modificações.

- Para executar o servidor utilizando a interface gráfica basta inserir o
comando ./servidorgui.py

- Para executar o cliente utilizando a interface gráfica basta inserir o
comando ./clientegui.py ou ./cliente.py

- Para executar o servidor diretamente no prompt (sem interface gráfica)
insira o comando ./servidor.py. Nesse caso, o servidor será iniciado com os
valores default ('' para o endereço do servidor e 10000 para a porta).
Também podem ser passados os valores do endereço do servidor e da porta como
argumentos. Para isso, basta inserir um comando no formato
./servidor.py <endereçoServidor> <porta>

- Para executar o cliente diretamente no prompt (sem interface gráfica)
insira um comando no formato
./cliente.py <endereçoServidor> <porta> <caminhoDoArquivo>
