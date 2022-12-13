import os
import re
from collections import Counter
import numpy as np
import torch
from gensim.models import Word2Vec


def make_embedding(sentences, model,tokenizer):
    vecs = []
    with torch.no_grad():

        for sentence in sentences:
            inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True,  max_length=64)

            hidden_states = model(**inputs, return_dict=True, output_hidden_states=True).hidden_states

            #Averaging the first & last hidden states
            output_hidden_state = (hidden_states[-1] + hidden_states[1]).mean(dim=1)

            vec = output_hidden_state.cpu().numpy()[0]

            vecs.append(vec)
    return vecs

def scenesentence_to_embedding(scene_dict):
    scene_embedding = {}
    for i, char_dict in scene_dict.items():
        scene = {}
        for char, sent in char_dict.items():
            emb = make_embedding(sent)
            scene[char] = emb        
        scene_embedding[i] = scen
    return scene_embedding
    
def read_graph(edgeList):
    G = nx.read_edgelist(edgeList, nodetype=str, delimiter='  ', data=(('type',int),('id',int)), create_using=nx.DiGraph())
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] = 1.0
    return G
    
def make_graph(scene_embedding):
    g_list = []
    id_num = 1
    node_embedding = {}
    total_act = []
    for i, (scene, contents) in enumerate(scene_embedding.items()):
        sent_num = 1
        for char, embs in contents.items():        
            for emb in embs:
                line = 'scene_' + str(scene) + '  ' + str(scene) + '_act_' + str(sent_num) + '  ' + '2' + '  ' + str(id_num)
                total_act.append(str(scene) + '_act_' + str(sent_num))
                node_embedding[str(scene) + '_act_' + str(sent_num)] = emb
                id_num += 1
                g_list.append([line])
                line = str(scene) + '_act_' + str(sent_num) + '  ' + char + '  ' + '3' + '  ' + str(id_num)
                id_num += 1
                sent_num += 1
                g_list.append([line])
        if sent_num!=1:     
            for j in range(sent_num):
                for k in range(j+1,sent_num):
                    line = str(scene) + '_act_' + str(j) + '  ' + str(scene) + '_act_' + str(k) + '  ' + '4' + '  ' + str(id_num)
                    id_num += 1
                    g_list.append([line])
    with open('test.csv', 'w',newline='') as f: 
        write = csv.writer(f) 
        write.writerows(g_list)
    g = read_graph('test.csv')
    return g
    
def set_node(g):
    attr = {}
    for node in g.nodes():
        if 'scene' in node:
            attr[node]='scene'
        elif 'act' in node:
            attr[node]='act'
        elif 'char' in node:
            attr[node]='char'
    nx.set_node_attributes(g, attr,"label")
    return g
    
def word2vec_train(g, filename, path, vector_size=384, window=5, min_count=0, sg=1, workers=4, epochs=60):
    word2vec = Word2Vec(vector_size=384, window=5, min_count=0, sg=1, workers=4, epochs=60)
    word2vec.build_vocab(corpus_iterable=[list(g.nodes())])
    for key in word2vec.wv.index_to_key:
        if key in node_embedding.keys():
            word2vec.wv[key] = node_embedding[key]
    word2vec.train(walks, total_examples=word2vec.corpus_count, epochs=30)        
    word2vec.save('word2vec_model_dim=384/'+ filename + 'word2vec.model')

