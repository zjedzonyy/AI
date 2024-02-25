import os
import random
import re
import sys
from pagerank import crawl, transition_model

DAMPING = 0.85
SAMPLES = 10000

if len(sys.argv) != 2:
    sys.exit("Usage: python pagerank.py corpus")
corpus = crawl(sys.argv[1])
print(corpus)

    # corpus = {'1.html': {'2.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}, '2.html': {'3.html', '1.html'}}
    # return = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

# print(corpus)
# if corpus:
#     for key, values in corpus.items():
#         key_p = round((1-0.85)/(1 + len(values)), 4)
#         dic = {key: key_p}
        
#         for value in values:
#             value_p = round(0.85/len(values) + key_p, 4)
#             dic[value] = value_p

#         print(dic)
# else:
#     # The probability is the same for going to any page in corpus.keys().
#     p = round(1/len(key), 4)
#     # Return a dictionairy (key = corpus.key, value = p)
#     for key in corpus.keys():
#         dic = {key: p}
#     print(p)




# i = 0
# samples = {}
# sample = random.choice(list(corpus.keys()))
# samples[sample] = 1
# #dobrze dotad
# while i < 9999:
#     i += 1
#     pages = list(transition_model(corpus, sample, 0.85).keys())
#     weights = list(transition_model(corpus, sample, 0.85).values())

#     sample = random.choices(pages, weights=weights, k=1)[0]

#     if sample in samples.keys():
#         samples[sample] += 1
#     else:
#         samples[sample] = 1

# for key in samples.keys():
#     samples[key] /= 10000

# print(samples)