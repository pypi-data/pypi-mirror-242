def stemming():
    s="""from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

sentence = "running runner runs quickly"
words = word_tokenize(sentence)

for word in words:
    print(ps.stem(word))
"""
    return s
def lemmatization():
    s="""from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()

sentence = "running runner runs quickly"
words = word_tokenize(sentence)

for word in words:
    print(lemmatizer.lemmatize(word))
"""
    return s
def backpropogation():
    s="""import numpy as np
def sigmoid(x, deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))
X = np.array([  [0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1] ])
y = np.array([[0,0,1,1]]).T
np.random.seed(1)
ini_weight = 2*np.random.random((3,1)) - 1
for iter in range(10000):
    # forward propagation
    l0 = X
    l1 = sigmoid(np.dot(l0,ini_weight))
    l1_error = y - l1
    l1_delta = l1_error * sigmoid(l1,True)
    ini_weight += np.dot(l0.T,l1_delta)
print("Output After Training:")
print(l1)"""
    return s
def pos_tagging():
    s="""import nltk
from nltk.tokenize import word_tokenize

# Sentence
sentence = "The quick brown fox jumps over the lazy dog"

# Tokenize the sentence
words = word_tokenize(sentence)

# Perform POS tagging
tagged_words = nltk.pos_tag(words)

# Print the tagged words
for word in tagged_words:
    print(word)
"""
    return s
def neural_engineering_framework():
    s="""pip install nengo
import numpy as np
import nengo
with nengo.Network() as model:
    neurons = 100
    ensemble = nengo.Ensemble(n_neurons=neurons, dimensions=1)
    input_node = nengo.Node(output=np.sin)
    nengo.Connection(input_node, ensemble)
    probe = nengo.Probe(ensemble)

with nengo.Simulator(model) as sim:
    sim.run(1)

import matplotlib.pyplot as plt

plt.plot(sim.trange(), sim.data[probe])
plt.xlabel("Time (s)")
plt.ylabel("Ensemble Output")
plt.show()"""
    return s