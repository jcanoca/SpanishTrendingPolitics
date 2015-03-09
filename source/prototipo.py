# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 19:20:42 2015

@author: jccan
"""

from __future__ import division
import nltk
import re
import os
import math
import json

os.chdir('/Users/jccan/Dropbox/Datascience/SpanishTrendingPolitics')

# Funciones


def N_mas_comunes(txt, vocab, n=20):
    l = [(w, text.count(w)) for w in vocab]
    l = sorted(l, key=lambda t: t[1])
    return l[-n:]

#
# Lectura de ficheros externos
fl = open("./data/doc.txt", 'r')

# Cargamos stop words en español
# tomados de https://code.google.com/p/stop-words
fl_stw1 = open("./data/stop-words_spanish_1_es.txt", 'r')
fl_stw2 = open("./data/stop-words_spanish_2_es.txt", 'r')

raw = fl.read()
# falta limpiar el texto
puntc = [',', '.', ';', '-', '!', '?', '¿', '¡']

for p in puntc:
    raw = raw.replace(p, ' ')

# Tokenizamos
tokens = nltk.word_tokenize(raw)

raw_stw1 = fl_stw1.read()
stop_words_1 = nltk.word_tokenize(raw_stw1)

raw_stw2 = fl_stw2.read()
stop_words_2 = nltk.word_tokenize(raw_stw2)

quitar = [w for w in tokens if re.search(r'^[^a-zA-Z]+$', w)]

# Eliminamos palabras no alfanuméricas
tokens = [w for w in tokens if w not in quitar]

# Normalizamos todo a minúscualas
words = [w.lower() for w in tokens]
words2 = [w for w in words if w not in stop_words_1 + stop_words_2]
words = words2

# Construimos un vocabulario ordenado
vocab = sorted(set(words))

# Contamos las N palabras más comunes en el texto
text = nltk.Text(words)
count_words = N_mas_comunes(text, vocab, 20)

# Construimos el JSON para el "Bubble Chart"

laux = []
for ele in count_words:
    laux.append(dict(name=ele[0], size=ele[1]))

dc = dict(name="PartidoPopular", children=laux)
fout = open("./data/discurso.json", 'w')
fout.write(json.dumps(dc))
fout.close()
