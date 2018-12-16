import numpy as np
import re
import random, csv
POS_DATASET_PATH = 'tweets/tweets_pos.pos'
NEG_DATASET_PATH = 'tweets/tweets_neg.neg'
VOC_PATH = 'tweets/vocab.csv'
VOC_INV_PATH = 'tweets/vocab_inv.csv'



def clean_str(string):
    string1 = string.replace(",", " , ")
    string1 = string.replace("!", " ! ")
    string1 = string.replace("\"", " ")
    string1 = string.replace("\(", " \( ")
    string1 = string.replace("\)", " \) ")
    string1 = string.replace("\?", " \? ")
    string1 = string.replace("???", "?")
    string1 = string.replace("??", "?")
    string1 = string.replace(" dl "," del ")
    string1 = string.replace("[^A-Za-z0-9(),!?\'\`]", " ")
    string1 = string1.replace(" d "," de ")
    string1 = string1.replace(" x "," por ")
    string1 = string1.replace(" xq "," porque ")
    string1 = string1.replace(" q "," que ")
    string1 = string1.replace(" n "," no ")
    string1 = string1.replace(" l "," la ")
    string1 = string1.replace(";-)"," feliz ")
    string1 = string1.replace(":-)"," feliz ")
    string1 = string1.replace(";)"," feliz ")
    string1 = string1.replace(":(" ," triste ")
    string1 = string1.replace(":)"," feliz ")
    string1 = string1.replace(";)"," feliz ")
    string1 = string1.replace(":/"," confundido ")
    string1 = string1.replace(":3"," santo ")
    string1 = string1.replace("aaaa", "a")

    return string1.strip().lower()


def sample_list(list, fraction):
    return random.sample(list, int(len(list) * fraction))


def load_data_and_labels(dataset_fraction):
    print "\tleyendo tweets positivos..."
    positive_examples = list(open(POS_DATASET_PATH).readlines())
    positive_examples = [s.strip() for s in positive_examples]
    print "\t[OK]"
    print "\tleyendo tweets negativos..."
    negative_examples = list(open(NEG_DATASET_PATH).readlines())
    negative_examples = [s.strip() for s in negative_examples]
    print "\t[OK]"

    positive_examples = sample_list(positive_examples, dataset_fraction)
    negative_examples = sample_list(negative_examples, dataset_fraction)

    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    x_text = [s.split(" ") for s in x_text]
    # Generate labels
    print "\tGenerando etiquetas..."
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    print "\t[OK]"
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def pad_sentences(sentences, padding_word="<PAD/>"):
    sequence_length = max(len(x) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences


def pad_sentences_to(sentences, pad_to, padding_word="<PAD/>"):
    sequence_length = pad_to
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences


def build_vocab():
    voc = csv.reader(open(VOC_PATH))
    voc_inv = csv.reader(open(VOC_INV_PATH))
    # Mapping from index to word
    vocabulary_inv = [x for x in voc_inv]
    # Mapping from word to index
    vocabulary = {x: i for x, i in voc}
    return [vocabulary, vocabulary_inv]


def build_input_data(sentences, labels, vocabulary):
    x = np.array([[vocabulary[word] for word in sentence]
                  for sentence in sentences])
    y = np.array(labels)
    return [x, y]

#word2vec
def string_to_int(sentence, vocabulary, max_len):
    base = [sentence]
    base = [s.strip() for s in base]
    x_text = base
    x_text = [clean_str(sent) for sent in x_text]
    x_text = [s.split(" ") for s in x_text]
    padded_x_text = pad_sentences_to(x_text, max_len)
    try:
        x = np.array([[vocabulary[word] for word in sentence]
                      for sentence in padded_x_text])
        return x
    except KeyError, e:
        print "La siguiente palabra no esta en la dataset de entrenamiento: %s" % str(e)
        quit()


def load_data(dataset_fraction):
    # Carga y preprocesa
    sentences, labels = load_data_and_labels(dataset_fraction)
    sentences_padded = pad_sentences(sentences)
    print "\tconstruyendo el vocabulario..."
    vocabulary, vocabulary_inv = build_vocab()
    print "\t[OK]"
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]


def batch_iter(data, batch_size, num_epochs):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_data = data[shuffle_indices]
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
