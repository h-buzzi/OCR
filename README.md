### Produzido por Henrique Eissmann Buzzi ###

# Software para Optical Character Recognition (OCR).

## Modo de usar:

Terá que se fornecer 2 imagens binárias das imagens. A primeira imagem será a imagem do alfabeto, ou seja, o template de letras que deseja-se utilizar. Com isto, o programa irá detectar automaticamente cada uma das letras e apresentá-las, uma por uma, em uma janela para o usuário. O usuário então terá que pressionar no teclado, qual é a letra que está sendo mostrada. Isto é feito para ensinar o algoritmo, fazendo-o conseguir relacionar o template a sua letra. Com isto, o algoritmo irá pegar a segunda imagem fornecida, que é a imagem do texto que será lido. Ele irá detectar as letras, palavras, linhas, e realizar a leitura do texto, produzindo sua versão escrita no terminal.

Para a leitura do texto, utiliza-se a função criada 'textGenerate_letterMatching', nela, o projetista/usuário fornece obrigatoriamente o parâmetro 'space_words', que é o entre cada palavra do texto. Isto é utilizado para o algoritmo entender quando é apenas a próxima letra da palavra, ou quando terminou uma palavra e começou-se outra (visto que o espaço entre letras é menor que o espaço entre palavras). Outra opção que pode ser modificada, mas que são raros os casos, é o 'line_strech', que seria basicamente o quão comprida é cada linha do texto. Como o valor padrão já é suficientemente grande, funcionará para maioria dos textos, mas caso precise alterar para eventuais erros, ou caso deseja-se diminuir para melhor tempo de execução (visto que pode ser desnecessário para alguns textos um valor tão grande). O usuário/projetista também pode escolher o método de template matching que deseja-se utilizar (sad, zsad, ssd, zssd, ncc, zncc).

## Conceitos aplicados

OCR, Template Matching, Operações Morfológicas.
