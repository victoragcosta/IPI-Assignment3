# Trabalho 3 de Introdução ao Processamento de Imagens

Resolução de problemas propostos para o Trabalho de 3 de Introdução ao
Processamento de Imagens da Universidade de Brasília.

## Aluno
Nome                    | Matrícula
------------------------|-----------
Victor André Gris Costa | 16/0019311

## Ambiente
* O trabalho foi desenvolvido e testado utilizando Python versão 3.7.3 no Windows 10

Pacote        | Versão
--------------|---------
matplotlib    | 3.0.3
numpy         | 1.16.2
opencv-python | 4.0.0.21

## Modo de Execução

1. Acesse a pasta raiz do projeto
2. Execute os exercícios com o comando `python src/problema<1,2 ou 3>.py`
3. Dependendo do seu ambiente, para garantir a versão correta de python, troque
   `python` por `python3` ou `python3.7`

## Questões

### Questão 1

Faça um programa que segmente a imagem `img_cells.jpg`. Inicialmente, o programa
deve seguir os seguintes passos:
1. Binarizar a imagem, onde as células são pretas e o fundo é branco (utilizando
   métodos similares a questão 2.1)
2. Se necessário, utilize uma função para preencher espaços desconectados (tipo
   `bwareaopen` no matlab).
3. Se necessário faça um preenchimento de buracos (para preencher buracos pode
   ser necessário usar o negativo da imagem, nesse casso faça o negativo novamente
   antes de passar para o passo 4).
4. calcule a função de distância (função `bwdist` no Matlab, ou `distanceTransform`
   no openCV).
5. compute a segmentação watersheed, comente seus resultados.

### Questão 2

1. Crie um programa para ler a arquivos YUV. Sendo que a função deve assumir
   que o arquivo está em formato binário e em modo 4:2:0. Sendo que os primeiros
   MxN bytes correspondem aos pixels de luminância, seguindo de (M/2)x(N/2)
   bytes de crominância U, e (M/2)x(N/2) bytes de crominância V. Onde M,N são
   as dimensões da imagem. A função deve pedir o nome do arquivo, a quantidade
   de quadros (images) a serem lidos e a resolução (M,N). Exemplo: \[Y,U,V\] =
   ler_yuv('foreman.yuv',5,352,288). As saídas devem estar como matrizes de
   inteiros de 8 bits sem sinal.
2. Ler o primeiro quadro do vídeo foreman.
3. Realize uma máscara de segmentação que indique a parte de pele humana (pode
   usar qualquer técnica de segmentação vista em sala de aula).

### Questão 3

Utilize o leitor de YUV feito na questão anterior para fazer um codificador de
imagens.
1. Leia os dois primeiro quadro do vídeo "foreman.yuv" com a função feita na
   Questão 2.
2. Para o canal luminância (Y) do primeiro quadro faça o seguinte processamento:

    1. Quantize-o utilizando um passo de quantização de 5, 10 e 15.
    2. Faça um gráfico indicando Entropia x Quantização. Para isso pode utilizar
      funções prontas do Matlab ou OPENCV para calcular Entropia. No gráfico
      incluir a entropia da imagem SEM quantização.

3. Para o canal luminância (Y) do segundo quadro faça o seguinte processamento:

    1. Faça a diferença do Y do segundo quadro com o primeiro e some 128
    2. Quantize-o utilizando um passo de quantização de 5, 10 e 15.
    3. Faça um gráfico indicando Entropia x Quantização. Para isso pode utilizar
      funções prontas do Matlab ou OPENCV para calcular Entropia. No gráfico
      incluir a entropia da imagem SEM quantização.
