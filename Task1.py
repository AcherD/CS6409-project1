# 118100173 Anchen Dai
import os
import re

# set path
path = "Dataset-P1"
files = os.listdir(path)


# get the words dictionary
def dict_get():
    full_data = ""  # string for full data
    # read the data form the database
    for file in files:
        open_file = open(path + "/" + file)  # open the file
        reader = iter(open_file)  # set read to read file
        for line in reader:
            full_data += line  # add data in to full data
    # delete the punctuation
    full_data = re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', '', full_data)
    words_full = full_data.split()  # split the words
    dictionary = {}  # dictionary for words
    for word in range(len(words_full)):
        dictionary.setdefault(words_full[word].lower(), 0)  # set default value 0 and ignore the uppercase
        dictionary[words_full[word].lower()] += 1
    return dictionary


# dictionary filter
def dict_filter(dictionary, min_len, max_len):
    words = list(dictionary.keys())  # get the words
    for num in range(len(dictionary)):
        if len(words[num]) < min_len or len(words[num]) > max_len:
            del dictionary[words[num]]  # delete the words does not match condition
    return dictionary


# sort the dictionary
def dict_sort(dictionary):
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return dictionary[0:200]  # return the top 200 results


words_dir = dict_get()
print(words_dir)
dict_filter(words_dir, 4, 20)  # set the min_size = 4 and max_size = 20
words_dir = dict_sort(words_dir)
print(words_dir)
print(len(words_dir))

# end
