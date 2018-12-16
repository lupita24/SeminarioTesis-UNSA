from data_helpers import *
import itertools
from collections import Counter
import csv

def build_vocab(sentences):
    word_counts = Counter(itertools.chain(*sentences))
    # Mappea de index a word
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    # Mappea de word a index
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]

# Load and preprocess data
print 'vocab_builder: Cargando...'
sentences, labels = load_data_and_labels(1)  # 1 is passed so that load_data_and_labels() will parse the whole dataset
print 'vocab_builder: Ejecutando...'
sentences_padded = pad_sentences(sentences)
print 'vocab_builder: Creando vocabulario...'
vocabulary, vocabulary_inv = build_vocab(sentences_padded)

print 'vocab_builder: Escrbiendo vocabulario...'
voc = csv.writer(open('tweets/vocab.csv', 'w'))
voc_inv = csv.writer(open('tweets/vocab_inv.csv', 'w'))

for key, val in vocabulary.items():
    voc.writerow([key, val])
for val in vocabulary_inv:
    voc_inv.writerow([val])
