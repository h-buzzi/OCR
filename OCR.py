# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 13:14:05 2021

@author: hbuzzi
"""
import cv2
import sys
import numpy as np

def show_contours(image, contours):
    cv2.drawContours(image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.imshow('a',image)
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        sys.exit()
    return
    

def create_alphabetTemplate(contours, alph_image):
    alphabet = {}
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        roi_letter = alph_image[y:y+h,x:x+w]
        cv2.imshow('bla', roi_letter)
        letter = ['waiting']
        key = 0
        while True:
            aux = roi_letter.copy()
            key = cv2.waitKey(0)
            if key == 13:
                alphabet.update({letter[0]: np.float64(roi_letter)})
                break
            if key == 32:
                while key != 13 and key != ord('R') and key != ord('r'):
                    key = cv2.waitKey(0)
                if key == 13:
                    break
                else:
                    continue
            del letter[0]
            letter.append(chr(key))
            print(letter[0])
            cv2.destroyAllWindows()
            cv2.putText(aux, letter[0], ((aux.shape[1]//2)-10,(aux.shape[0]//2)+10), cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,0),2, cv2.LINE_AA)
            cv2.putText(aux, letter[0], ((aux.shape[1]//2)-10,(aux.shape[0]//2)+10), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255),1, cv2.LINE_AA)
            cv2.imshow(letter[0], aux)
        cv2.destroyAllWindows()
    return alphabet



def textGenerate_letterMatching(bin_image, dictionary, space_words, method = 'sad', line_strech = 10000):
    def detect_line(bin_image, line_strech):
        rect = cv2.getStructuringElement(cv2.MORPH_RECT, (line_strech,1))
        img_line = cv2.dilate(bin_image, rect, iterations = 1)
        contours, _ = cv2.findContours(image = img_line, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        line = []
        text_lines = {}
        for cont in contours:
            x,y,w,h = cv2.boundingRect(cont)
            roi_line = bin_image[y:y+h,x:x+w]
            text_lines.update({y: roi_line})
            line.append(y)
        line.sort()
        return text_lines, line
    
    def detect_letters(text_lines,line):
        for l in line:
            contours, _ = cv2.findContours(image = text_lines[l], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            letter = {}
            pos = []
            width = {}
            for cont in contours:
                x,y,w,h = cv2.boundingRect(cont)
                roi_letter = text_lines[l][y:y+h,x:x+w]
                letter.update({x:roi_letter})
                pos.append(x)
                width.update({x:w})
            letter.update({'pos':pos})
            letter.update({'width':width})
            text_lines[l] = letter
        return text_lines
    
    def dictionary_of_text(text_lines, line, space_words, method):
        def alphabet_matching(dictionary,letter, method):
            letter = np.float64(letter)
            Id = {}
            if(method == 'sad'):
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape[::-1], interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(np.abs(letter - T))})
                return min(Id, key=Id.get)
            elif(method == 'zsad'):
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(np.abs((letter - np.mean(letter)) - (T - np.mean(T))))})
                return min(Id, key=Id.get)
            elif(method == 'ssd'):
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum((letter - T)**2)})
                return min(Id, key=Id.get)
            elif(method == 'zssd'):
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(((letter - np.mean(letter)) - (T - np.mean(T)))**2)})
                return min(Id, key=Id.get)
            elif(method == 'ncc'):
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    Id.update({L:np.sum(letter*T)/np.sqrt(np.sum(letter**2)*np.sum(T**2))})
                return max(Id, key=Id.get)
            elif(method == 'zncc'):
                m_l = np.mean(letter)
                for L in dictionary:
                    T = dictionary[L]
                    T = cv2.resize(T, letter.shape, interpolation = cv2.INTER_CUBIC)
                    m_T = np.mean(T)
                    Id.update({L:np.sum((letter-m_l)*(T-m_T))/np.sqrt(np.sum((letter-m_l)**2)*np.sum((T-m_T)**2))})
                return max(Id, key=Id.get)
            else:
                raise RuntimeError('Invalid Method Selected for alphabet_matching')
                sys.exit()
            return
    
        texto = {}
        for i in range(len(line)):
            pos = text_lines[line[i]]['pos']
            pos.sort()
            texto_line = {}
            ant = float('inf')
            space = 0
            dif = [] #Remover
            for j in range(len(pos)):
                dif.append(pos[j]-ant) #Remover
                if(pos[j]-ant > space_words):
                    texto_line.update({j+space:' '})
                    space += 1
                letter = text_lines[line[i]][pos[j]]
                response = alphabet_matching(alphabet,letter,method)
                texto_line.update({j+space:response})
                ant = pos[j]+text_lines[line[i]]['width'][pos[j]]
            texto_line.update({'dif':dif}) #Remover
            texto.update({i:texto_line})    
        return texto
        
    
    
    text, line_pos = detect_line(bin_image, line_strech)
    text = detect_letters(text, line_pos)
    text = dictionary_of_text(text, line_pos, space_words, method)
    return text
    ## Até aqui me gerou um dicionário com todas as letras, separadas por line e distância x
    

alph_template = cv2.imread('templates_letras.png')
text = cv2.imread('texto_1.png')
ret, bin_image = cv2.threshold(cv2.cvtColor(alph_template, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(image=bin_image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
show_contours(alph_template,contours)
alphabet = create_alphabetTemplate(contours, bin_image)

ret, bin_image = cv2.threshold(cv2.cvtColor(text, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY_INV)
text = textGenerate_letterMatching(bin_image,alphabet,20)




    


