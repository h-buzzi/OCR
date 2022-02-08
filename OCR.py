# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 13:14:05 2021

@author: hbuzzi
"""
import cv2
import sys
import numpy as np

def create_alphabetTemplate(alph_image):
    '''Encontra cada letra da figura de template de letras do alfabeto, fazendo com que o usuário informe o identificador da letra que o programa encontrar
    
    Input: Imagem binária com todas as letras do alfabeto desejado
    
    Output: Dicionário com cada template/imagem da letra e sua letra identificadora
    
    Modo de usar: Insira o input corretamente. Após isso, a imagem com cada uma letra contornada deverá aperecer, se este for o caso, apenas feche esta janela. Após isto, uma janela aparecerá com 1 das letras encontradas. Pressione a tecla no teclado para informar ao algoritmo qual letra é a que está aparecendo. Após a letra aparecer sobscrita, pressione Enter para confirmar. Repita para toda letra que aparecer'''
    def show_contours(image, contours):
        '''Mostra o template com cada contorno encontrado, para o usuário conferir se todas as letras foram encontradas
        
        Input: Imagem binária do alfabeto e os contornos da letra
        
        Output: Janela com a imagem e seus contornos'''
        cv2.drawContours(image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA) #Desenha os contornos na imagem
        cv2.imshow('a',image) #Mostra a imagem
        key = cv2.waitKey(0)
        if key == 27: #Se apertar ESC, deleta e sai do programa
            cv2.destroyAllWindows()
            sys.exit()
        return
    contours, hierarchy = cv2.findContours(image=alph_image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE) #Pega os contornos dos objetos na imagem binária
    show_contours(alph_template,contours) #Mostra os contornos do alfabeto para o usuário poder verificar se está tudo correto
    alphabet = {} #Pré alocação do dicionário do alfabeto
    for cnt in contours: #Itera sobre cada contorno da figura
        x,y,w,h = cv2.boundingRect(cnt) #Pega as posições da BoundingBox do contorno (neste caso letra)
        roi_letter = alph_image[y:y+h,x:x+w] #Seleciona apenas a região de interesse, tendo uma imagem com apenas a letra
        cv2.imshow('waiting', roi_letter) #Mostra a letra encontrada
        letter = ['waiting'] #Pré-alocação da letra apresentada
        key = 0 #Garante condições iniciais da tecla
        while True: #Loop que espera o usuário identificar a letra apresentada
            aux = roi_letter.copy() #Cria uma cópia da letra para poder escrever informações sobre
            key = cv2.waitKey(0) #Espera a tecla
            if key == 13: #Se pressionar enter
                alphabet.update({letter[0]: np.float64(roi_letter)}) #Adiciona ao dicionário a identificação da letra e o seu template
                break #sai do loop que espera pela identificação da letra
            del letter[0] #deleta a letra anterior
            letter.append(chr(key)) #Coloca a nova letra
            print(letter[0]) #printa no console
            cv2.destroyAllWindows() #Destroi a janela que mostra a figura da letra com sua identificação anterior
            cv2.putText(aux, letter[0], ((aux.shape[1]//2)-10,(aux.shape[0]//2)+10), cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,0),2, cv2.LINE_AA) #Cria a letra de identificação em preto
            cv2.putText(aux, letter[0], ((aux.shape[1]//2)-10,(aux.shape[0]//2)+10), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255),1, cv2.LINE_AA) #Cria a letra de identificação em branco sobre a letra em preto, fazendo com que a mesma agora tenha uma borda
            cv2.imshow(letter[0], aux) #Mostra a letra com sua identificação
        cv2.destroyAllWindows() #Quando for para próxima letra, fecha a janela da letra anterior
    return alphabet #Retorna o dicionário do alfabeto



def textGenerate_letterMatching(bin_image, dictionary, space_words, method = 'sad', line_strech = 10000):
    '''Algortimo que lê a imagem do texto e gera um dicionário que reproduz o texto da imagem em formato escrito
    
    Input: Imagem binária do texto que deseja ser lido, dicionário com as letras do alfabeto (gerado pelo algoritmo create_alphabetTemplate), valor inteiro que representa o espaço entre palavras (definido pelo usuário, é necessário fine tuning), uma string que escolhe o método, e uma variável inteira para dilatação das letras para captura das linhas.
    
    Output: Dicionário com o texto transcrito da imagem
    
    Modo de usar: Forneça a imagem binária do texto, com o texto como binário alto e o fundo como binário baixo, bem como um valor teorizado de quantos pixels existe entre uma palavra e outra. É possível escolher o método de preferência para o template matching, tendo as opção 'sad', 'ssd' e 'ncc', bem como suas versões zero-offset usando 'zsad', 'zssd' e 'zncc'. O último parâmetro opcional que pode-se fornecer é para dilatar as letras e formar a linha. Caso a linha não esteja sendo reconhecida corretamente, pode-se aumentar o valor do parâmetro'''
    def detect_line(bin_image, line_strech):
        '''Encontra cada linha de texto dilatando os caracteres da linha para que se unam em uma única barra horizontal, produzindo um objeto de linha
        
        Input: Imagem binária do texto e o parâmetro que irá dilatar as letras para formar uma única linha
        
        Output: Dicionário com as imagens com cada linha de texto, e um vetor com suas respectivas posições
        '''
        rect = cv2.getStructuringElement(cv2.MORPH_RECT, (line_strech,1)) #Cria o retângulo horizontalmente 'infinito'
        img_line = cv2.dilate(bin_image, rect, iterations = 1) #Dilata usando o retângulo
        contours, _ = cv2.findContours(image = img_line, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE) #Encontra o contorno das linhas
        line = [] #Pré alocação do vetor de posição das linhas
        text_lines = {} #Pré alocação do dicionário que salva a posição e a imagem da linha
        for cont in contours: #Para cada linha encontrada
            x,y,w,h = cv2.boundingRect(cont) #Pega as coordenadas retangulares do objeto
            roi_line = bin_image[y:y+h,x:x+w] #Pega a imagem retangular da linha
            text_lines.update({y: roi_line}) #Salva a imagem com sua respectiva posição
            line.append(y) #Salva a posição de cada linha
        line.sort() #Coloca a posição das linhas em ordem ascendente
        return text_lines, line #Retorna as linhas e posições ordenadas
    
    def detect_letters(text_lines,line):
        '''Visita cada linha encontrada anteriormente e encontra cada uma das letras
        
        Input: Dicionário com as imagens de linha, bem como as posições de cada linha
        
        Output: Dicionário com cada letra encontrada em sua respectiva linha, dentro do dicionário tem-se também a posição e comprimento de cada letra em cada linha'''
        for l in line: #Para cada posição de linha encontrada
            contours, _ = cv2.findContours(image = text_lines[l], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE) #Acessa a imagem de linha dessa posição e encontra o contorno de cada letra
            letter = {} #Pré-alocação do dicionário das letras
            pos = [] #Pré-alocação do vetor de posição de letras
            width = {} #Pré-alocação do vetor de comprimento de cada letra
            for cont in contours: #Para cada contorno de letra encontrada
                x,y,w,h = cv2.boundingRect(cont) #Pega sua boundingbox
                roi_letter = text_lines[l][y:y+h,x:x+w] #Salva a imagem da letra
                letter.update({x:roi_letter}) #Salva sua posição como identificador e a imagem
                pos.append(x) #Salva a posição
                width.update({x:w}) #Salva o comprimento de cada letra com a posição como identifcador
            letter.update({'pos':pos}) #Salva dentro do dicionário as posições, para retonar todas as informações em 1 só elemento
            letter.update({'width':width}) #Salva dentro do dicionário as posições, para retonar todas as informações em 1 só elemento
            text_lines[l] = letter #Como não será mais necessário a imagem da linha, salva as letras da linha sobre o dicionário da linha
        return text_lines #Retorna o dicionário das linhas com cada uma de suas letras
    
    def dictionary_of_text(text_lines, alphabet, line, space_words, method):
        '''Pega cada letra, realiza seu template_matching, e vê se a distância entre uma letra e outra é grande o suficiente pra ser considerado uma nova palavra
        
        Input: Dicionário com cada letra em cada linha, dicionário com o alfabeto de letras, vetores de posições de cada linha, parâmetro que determina que quantidade de pixels entre palavras, string do método
        
        Output: Dicionário com o texto identificado e transcrito da imagem'''
        def alphabet_matching(dictionary,letter, method):
            '''Algoritmo de template_matching implementado com 6 métodos diferentes
            
            Input: Dicionário do alfabeto, letra que está sendo identificada, métododo
            
            Output: Caractere que identifica a letra'''
            letter = np.float64(letter) #Transforma a matriz de imagem da letra em float64 para que as computações matemáticas ocorram corretamente
            Id = {} #Pré-alocação do dicionário de valores de identificação
            if(method == 'sad'): #Método Sum of Absolute Differences
                for L in dictionary: #Para cada letra do template do alfabeto
                    T = dictionary[L] #Pega a letra do template
                    T = cv2.resize(T, letter.shape[::-1], interpolation = cv2.INTER_CUBIC) #Transforma a letra do template para o mesmo tamanho que a letra encontrada no texto
                    Id.update({L:np.sum(np.abs(letter - T))}) #Realiza o cálculo matemático de similaridade e salva em sua respectiva posição de letra
                return min(Id, key=Id.get) #Retorna qual posição do alfabeto foi calculado o menor valor
            elif(method == 'zsad'): #Método SAD com zero-offset
                #Funcionamento idêntico ao descrito no método SAD, apenas alterando o cálculo matemático para verificação da diferença das letras
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(np.abs((letter - np.mean(letter)) - (T - np.mean(T))))})
                return min(Id, key=Id.get)
            elif(method == 'ssd'): #Método Sum of Squared Differences
                #Funcionamento idêntico ao descrito no método SAD, apenas alterando o cálculo matemático para verificação da diferença das letras
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum((letter - T)**2)})
                return min(Id, key=Id.get)
            elif(method == 'zssd'): #Método SSD com zero-offset
                #Funcionamento idêntico ao descrito no método SAD, apenas alterando o cálculo matemático para verificação da diferença das letras
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(((letter - np.mean(letter)) - (T - np.mean(T)))**2)})
                return min(Id, key=Id.get)
            elif(method == 'ncc'): #Método Normalized Cross Correlation
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(letter*T)/np.sqrt(np.sum(letter**2)*np.sum(T**2))})
                return max(Id, key=Id.get) #A diferença do método NCC é que o valor máximo que indica a melhor similaridade
            elif(method == 'zncc'): #Método NCC com zero-offset
                m_l = np.mean(letter)
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    m_T = np.mean(T)
                    Id.update({L:np.sum((letter-m_l)*(T-m_T))/np.sqrt(np.sum((letter-m_l)**2)*np.sum((T-m_T)**2))})
                return max(Id, key=Id.get)
            else: #Se informou uma string inválida para o método retorna erro
                raise RuntimeError('Invalid Method Selected for alphabet_matching')
                sys.exit()
            return
    
        texto = {} #pré-alocação do dicionário de texto
        for i in range(len(line)): #Percorre cada linha
            pos = text_lines[line[i]]['pos'] #Pega a posição de cada letra da linha
            pos.sort() #Coloca em ordem ascendente (ou seja, parar percorrer da esquerda pra direita)
            texto_line = {} #Pré-alocação do texto da linha atual
            ant = float('inf') #Pré-alocação da distância da letra anterior
            space = 0 #Contador de espaços encontrados
            for j in range(len(pos)): #Percorre cada uma das letras
                if(pos[j]-ant > space_words): #Se a distância da letra atual para anterior for maior que a distância definida para o espaço:
                    texto_line.update({j+space:' '}) #Detecta como espaço e adiciona no texto o espaço
                    space += 1 #Incrementa o contador
                letter = text_lines[line[i]][pos[j]] #Pega a imagem da letra acessando sua linha, e então sua posição da letra
                response = alphabet_matching(alphabet,letter,method) #Realiza o template matching e descobre a letra do alfabeto
                texto_line.update({j+space:response}) #Salva a letra na ordem que foi encontrada (contabilizando os espaços encontrados também)
                ant = pos[j]+text_lines[line[i]]['width'][pos[j]] #Salva a posição final da letra anterior adicionando sua posição ao seu comprimento
            texto.update({i:texto_line}) #Salva as letras, palavras e consequentemente, todo o texto da linha em sua respectiva posição no dicionário   
        return texto
        
    
    
    text, line_pos = detect_line(bin_image, line_strech)
    text = detect_letters(text, line_pos)
    text = dictionary_of_text(text, alphabet, line_pos, space_words, method)
    return text 

alph_template = cv2.imread('templates_letras.png') #Importação da figura do alfabeto/template de letras
text = cv2.imread('texto_1.png') #Importação da figura de texto a ser lido
ret, bin_image = cv2.threshold(cv2.cvtColor(alph_template, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY_INV) #Criação da imagem binária do template
alphabet = create_alphabetTemplate(bin_image) #Criação do template de cada letra em conjunto com sua identificação

ret, bin_image = cv2.threshold(cv2.cvtColor(text, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY_INV) #Criação da imagem binária do texto
text = textGenerate_letterMatching(bin_image,alphabet,20) #Geração do texto




    


