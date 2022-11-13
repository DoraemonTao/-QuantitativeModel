#main_classify.py
import codecs
import math
import random
import string
import time
import numpy as np
import torch
from sklearn.metrics import accuracy_score

'''
Don't change these constants for the classification task.
You may use different copies for the sentence generation model.
'''
train_category_lines = {}
val_catgory_lines = {}
languages = ["af", "cn", "de", "fi", "fr", "in", "ir", "pk", "za"]
n_languages = len(languages)
all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)



def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )


'''
Returns the words of the language specified by reading it from the data folder
Returns the validation data if train is false and the train data otherwise.
Return: A nx1 array containing the words of the specified language
'''
def getWords(baseDir, lang, train = True):
    pass

'''
Returns a label corresponding to the language
For example it returns an array of 0s for af
Return: A nx1 array as integers containing index of the specified language in the "languages" array
'''
def getLabels(lang, length):
    tensor = torch.zeros(n_letters,1)
    tensor[0][languages.find(lang)] = 1
    return tensor

# Read a file and split into lines
def readLines(filename):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [unicodeToAscii(line) for line in lines]
'''
Returns all the laguages and labels after reading it from the file
Returns the validation data if train is false and the train data otherwise.
You may assume that the files exist in baseDir and have the same names.
Return: X, y where X is nx1 and y is nx1
'''
def readData(baseDir, train=True):
  category_lines = {}
  if train:
    for filename in findFiles('train/*.txt'):
      lang = os.path.splitext(os.path.basename(filename))[0]
      y = getLabels(lang,n_languages)
      lines = readLines(filename)
      category_lines[category] = lines
  else:
    for filename in findFiles('val/*.txt'):
      lang = os.path.splitext(os.path.basename(filename))[0]
      y = getLabels(lang,n_languages)
      lines = readLines(filename)
      category_lines[category] = lines



def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor
'''
Convert a line/word to a pytorch tensor of numbers
Refer the tutorial in the spec
Return: A tensor corresponding to the given line
'''
def line_to_tensor(line):
  tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor

'''
Returns the category/class of the output from the neural network
Input: Output of the neural networks (class probabilities)
Return: A tuple with (language, language_index)
        language: "af", "cn", etc.
        language_index: 0, 1, etc.
'''
def category_from_output(output):
  top_n, top_i = output.topk(1)
  category_i = top_i[0].item()
  return all_categories[category_i], category_i

def randomChoice(l):
    return l[random.randint(0, len(l) - 1)]
'''
Get a random input output pair to be used for training 
Refer the tutorial in the spec
'''
def random_training_pair(X, y):
  category = randomChoice(y)
  line = randomChoice(X[category])
  category_tensor = torch.tensor([languages.index(category)], dtype=torch.long)
  line_tensor = line_to_tensor(line)
  return line_tensor , category_tensor

'''
Input: trained model, a list of words, a list of class labels as integers
Output: a list of class labels as integers
'''
def predict(model, X, y):
    random_training_pair(X,y)

'''
Input: trained model, a list of words, a list of class labels as integers
Output: The accuracy of the given model on the given input X and target y
'''
def calculateAccuracy(model, X, y):
    pass
def categoryFromOutput(output):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return all_categories[category_i], category_i
'''
Train the model for one epoch/one training word.
Ensure that it runs within 3 seconds.
Input: X and y are lists of words as strings and classes as integers respectively
Returns: You may return anything
'''
def trainOneEpoch(model, criterion, optimizer, X, y):
    hidden = model.initHidden()

    model.zero_grad()

    for i in range(X.size()[0]):
        output, hidden = model(X[i], hidden)

    loss = criterion(output, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Add parameters' gradients to their values, multiplied by learning rate
    for p in model.parameters():
        p.data.add_(p.grad.data, alpha=-learning_rate)

    return output, loss.item()



'''
Use this to train and save your classification model. 
Save your model with the filename "model_classify"
'''
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def run(lr=0.01):
  n_iters = 100000
  print_every = 5000
  plot_every = 1000
  current_loss = 0
  all_losses = []
  optimizer = optim.SGD(model_2.parameters(),lr = lr, momentum = 0.9)
  for iter in range(1, n_iters + 1):
    line_tensor,category_tensor = random_training_pair(train_category_lines,)
    output, loss = trainOneEpoch(model,criterion,category_tensor, line_tensor)
    current_loss += loss

    # Print iter number, loss, name and guess
    if iter % print_every == 0:
        guess, guess_i = categoryFromOutput(output)
        correct = '✓' if guess == category else '✗ (%s)' % category
        print('%d %d%% (%s) %.4f %s / %s %s' % (iter, iter / n_iters * 100, timeSince(start), loss, line, guess, correct))

    # Add current loss avg to list of losses
    if iter % plot_every == 0:
        all_losses.append(current_loss / plot_every)
        current_loss = 0
  return all_losses

def val()

def evaluate(line_tensor):
    hidden = rnn.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    return output