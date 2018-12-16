import xml.etree.ElementTree as ET
import re
# -*- encoding: utf-8 -*-


def parse_with_lxml():
    tree = ET.parse('data.xml')
    root = tree.getroot()
    f = open ("limpiotest.txt","w")
    for content in root.findall('tweet'):
        cont = content.find('content').text
        C2 = cont.encode('utf8')
        for pola in content.findall('sentiment'):
            for value in pola.findall("./polarity/value"):
                f.write(value.text + " ")
        f.write(C2)
    f.close()

def detectar_polaridad(polaridad):
    val = polaridad.find("NONE")
    if val != -1:
        return "neu"
    val = polaridad.find("P")
    if val != -1:
        return "pos"
    return "neg"

def clasificar_tweet():
    f = open("limpio.txt","r")
    neg = open("tweets.neg","w")
    pos = open("tweets.pos","w")
    neu = open("tweets.neu","w")
    cont = 0
    dato = 0
    contenido = ''
    polaridad = ''
    tweet = ''
    tt = ""


    while cont < 1009:
        contenido = f.readline()
        if  len(contenido)>1:
            if dato == 0:
                polaridad = contenido
                dato = 1
            else:
                tweet = contenido
                dato = 2

        if dato == 2:
            polaridad = detectar_polaridad(polaridad)
            if polaridad == 'neg':
                neg.write(tweet)
            elif polaridad == 'pos':
                pos.write(tweet)
            else:
                neu.write(tweet)
            dato = 0
            cont = cont+1

    f.close()
    neu.close()
    neg.close()
    pos.close()

def parser_tweets_pos():
    cont = 0

    pos = open("tweets/tweets.pos", "r")
    pos_tweet = open("tweets/tweets_pos.pos","w")
    i = 0.0

    while  i < 21361:
        linea = pos.readline()
        print(linea)
        new_tweet = ''
        linea = linea.strip()
        for word in linea.split():
            # String preprocessing
            if re.match('^.*@.*', word):
                word = '<NAME/>'
            if re.match('^.*PORQUE.*', word):
                word = 'porque'
            if re.match('^.*JAJA.*', word):
                word = ' JA '
            if re.match('^.*http//.*', word):
                word = '<LINK/>'
            if re.match('^.*https//.*', word):
                word = '<LINK/>'
            word = word.replace('#', '<HASHTAG/> ')
            word = word.replace('&quot;', ' \" ')
            word = word.replace('&amp;', ' & ')
            word = word.replace('&gt;', ' > ')
            word = word.replace('&lt;', ' < ')
            word = word.replace(",", " , ")
            word = word.replace("!", " ! ")
            word = word.replace("\"", " ")
            word = word.replace("\(", " \( ")
            word = word.replace("\)", " \) ")
            word = word.replace("\?", " \? ")
            word = word.replace("???", "?")
            word = word.replace("??", "?")
            word = word.replace(" dl "," del ")
            word = word.replace("[^A-Za-z0-9(),!?\'\`]", " ")
            word = word.replace(" d "," de ")
            word = word.replace(" x "," por ")
            word = word.replace(" xq "," porque ")
            word = word.replace(" q "," que ")
            word = word.replace(" n "," no ")
            word = word.replace(" l "," la ")
            word = word.replace(";-)"," feliz ")
            word = word.replace(":-)"," feliz ")
            word = word.replace(";)"," feliz ")
            word = word.replace(":D"," sonriente ")
            word = word.replace(":(" ," triste ")
            word = word.replace(":)"," feliz ")
            word = word.replace(";)"," feliz ")
            word = word.replace(":*"," beso ")
            word = word.replace(":/"," confundido ")
            word = word.replace(":3"," santo ")
            word = word.replace(":p"," jugueton ")
            word = word.replace("aaaa", "a")
            word = word.strip().lower()
            new_tweet = ' '.join([new_tweet, word])
        linea = new_tweet.strip() + '\n'
        pos_tweet.write(linea)
        i =i+1.0
    print(i)
    pos.close()
    pos_tweet.close()

def parser_tweets_neg():
    cont = 0

    neg = open("tweets/tweets.neg", "r")
    neg_tweet = open("tweets/tweets_neg.neg","w")
    i = 0.0

    while  i < 122215:
        linea = neg.readline()
        print(linea)
        new_tweet = ''
        linea = linea.strip()
        for word in linea.split():
            # String preprocessing
            if re.match('^.*@.*', word):
                word = '<NAME/>'
            if re.match('^.*PORQUE.*', word):
                word = 'porque'
            if re.match('^.*JAJA.*', word):
                word = ' JA '
            if re.match('^.*http//.*', word):
                word = '<LINK/>'
            if re.match('^.*https//.*', word):
                word = '<LINK/>'
            word = word.replace('#', '<HASHTAG/> ')
            word = word.replace('&quot;', ' \" ')
            word = word.replace('&amp;', ' & ')
            word = word.replace('&gt;', ' > ')
            word = word.replace('&lt;', ' < ')
            word = word.replace(",", " , ")
            word = word.replace("!", " ! ")
            word = word.replace("\"", " ")
            word = word.replace("\(", " \( ")
            word = word.replace("\)", " \) ")
            word = word.replace("\?", " \? ")
            word = word.replace("???", "?")
            word = word.replace("??", "?")
            word = word.replace(" dl "," del ")
            word = word.replace("[^A-Za-z0-9(),!?\'\`]", " ")
            word = word.replace(" d "," de ")
            word = word.replace(" x "," por ")
            word = word.replace(" xq "," porque ")
            word = word.replace(" q "," que ")
            word = word.replace(" n "," no ")
            word = word.replace(" l "," la ")
            word = word.replace(";-)"," feliz ")
            word = word.replace(":-)"," feliz ")
            word = word.replace(";)"," feliz ")
            word = word.replace(":D"," sonriente ")
            word = word.replace(":(" ," triste ")
            word = word.replace(":)"," feliz ")
            word = word.replace(";)"," feliz ")
            word = word.replace(":*"," beso ")
            word = word.replace(":/"," confundido ")
            word = word.replace(":3"," santo ")
            word = word.replace(":p"," jugueton ")
            word = word.replace("aaaa", "a")
            word = word.strip().lower()
            new_tweet = ' '.join([new_tweet, word])
        linea = new_tweet.strip() + '\n'
        neg_tweet.write(linea)
        i =i+1.0
    print(i)
    neg.close()
    neg_tweet.close()

def parser_tweets_test():
    cont = 0

    pos = open("limpiotest.txt", "r")
    pos_tweet = open("test3.txt","w")
    i = 0.0

    while  i < 1690:
        linea = pos.readline()
        print(linea)
        new_tweet = ''
        linea = linea.strip()
        for word in linea.split():
            # String preprocessing
            if re.match('^.*@.*', word):
                word = '<NAME/>'
            if re.match('^.*http//.*', word):
                word = '<LINK/>'
            if re.match('^.*https//.*', word):
                    word = '<LINK/>'
            word = word.replace('#', '<HASHTAG/> ')
            word = word.replace('&quot;', ' \" ')
            word = word.replace('&amp;', ' & ')
            word = word.replace('&gt;', ' > ')
            word = word.replace('&lt;', ' < ')
            new_tweet = ' '.join([new_tweet, word])
        linea = new_tweet.strip() + '\n'
        pos_tweet.write(linea)
        i =i+1.0
    print(i)
    pos.close()
    pos_tweet.close()

if __name__ == '__main__':
    parse_with_lxml()  
    clasificar_tweet()
    parser_tweets_neg()
    parser_tweets_pos()
