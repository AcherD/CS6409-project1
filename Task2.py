# 118100173 Anchen Dai
import os
import re
import math
import numpy

# set path
path = "Dataset-P1"
files = os.listdir(path)


# get the words form file
def get_words(file):
    sentences = ""
    open_file = open(path + "/" + file)  # open the file
    reader = iter(open_file)  # set read to read file
    for line in reader:
        sentences += line  # add data in to full data
    sentences = re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', '', sentences)
    words = sentences.lower().split()  # spilt sentences to words
    return words


# sort the dictionary
def dict_sort(dictionary, n):
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return dict(dictionary[1:n+1])  # return the top n results


# sort the dictionary
def dict_sort_reverse(dictionary, n):
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=False)
    return dict(dictionary[1:n+1])  # return the top n results


# get tf list of file
def get_tf(file):
    words = get_words(file)
    tf_dictionary = {}  # dictionary for words
    for word in range(len(words)):
        tf_dictionary.setdefault(words[word].lower(), 0)  # set default value 0 and ignore the uppercase
        tf_dictionary[words[word].lower()] += 1
    return tf_dictionary


# get idf list
def get_idf(file):
    words = list(set(get_words(file)))
    idf_dictionary = {}
    for word in range(len(words)):
        file_include = 0
        for document in files:
            document_words = get_words(document)
            if words[word] in document_words or words[word].lower() in document_words:
                file_include += 1
        #  file_include = file_include + 1
        idf_dictionary[words[word].lower()] = math.log(len(files) / file_include,2)+1
    return idf_dictionary


# get tf-idf value return tf-idf dict
def get_tfidf(file):
    tf_value = get_tf(file)
    idf_value = get_idf(file)
    tfidf_value = {}
    for word in tf_value:
        tfidf_value[word] = tf_value[word] * idf_value[word]  # calculate the tf- idf value
    return tfidf_value


# get top ten using tf-idf
def top_ten_retrieve(file_name):
    file_words = get_words(file_name)
    file_tfidf = get_tfidf(file_name)
    distance_result = {}
    complete = 0
    # calculate the distance between all files
    for data in files:  # read the data form the database
        distance = 0
        data_words = get_words(data)
        keywords = list(set(file_words + data_words))
        data_tfidf = get_tfidf(data)
        for key in keywords:
            if key not in file_tfidf.keys():
                file_tfidf[key.lower()] = 0
            if key not in data_tfidf.keys():
                data_tfidf[key.lower()] = 0
            distance += math.pow(file_tfidf[key.lower()] - data_tfidf[key.lower()], 2)
        distance_result[data] = math.sqrt(distance)
        print("calculating {:.2%} completed".format(complete / len(files)))
        complete += 1
    distance_result = dict_sort_reverse(distance_result, 10)
    print("The top 10 files compare with " + file_name + " :")
    for result in distance_result.keys():
        print(result + "    value = " + str(distance_result[result]))
    print("===================End===================")
    #  return distance_result  # return the top 10 results


# calculate cos similarity of two files, using top n key words of two file
def get_cos(file):
    file1_words = get_words(file)
    cos_simi = {}
    for data in files:
        file2_words = get_words(data)
        keywords = list(set(file1_words + file2_words))
        # set vector
        vector1 = numpy.zeros(len(keywords))
        vector2 = numpy.zeros(len(keywords))
        # make the vector
        for index in range(len(keywords)):
            for word_1 in range(len(file1_words)):
                if keywords[index] == file1_words[word_1]:
                    vector1[index] += 1
            for word_2 in range(len(file2_words)):
                if keywords[index] == file2_words[word_2]:
                    vector2[index] += 1
        # calculate the cos similarity
        cos_simi[data] = float(numpy.dot(vector1, vector2) / (numpy.linalg.norm(vector1) * numpy.linalg.norm(vector2)))
    cos_simi = dict_sort(cos_simi, 10)
    print("The top 10 files using cosine similarity compare with " + file + " :")
    for result in cos_simi.keys():
        print(result + "    value = " + str(cos_simi[result]))
    print("===================End===================")
    return cos_simi


top_ten_retrieve("6.txt")
cos = get_cos("6.txt")
# end
