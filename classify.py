'''
vals_and_probs is a library providing two primary functions:

1) assign_likes_to_words takes in a dictionary of status IDs keyed to 
a tuple of (status, likes) and separates those sentences into a dictionary keying each 
individual word to its total number of "likes."

2) classify_words takes in a dictionary of statuses 

Created on May 3, 2013

@author: mjk42
'''

import nltk
import string
import re

#----------------------------------------------------------------------------------------------

def assign_likes_to_words(status_dict):
    '''
    Parses facebook statuses into individual words and adds each word to a new dictionary. 
    In the new dictionary, each word is keyed to the total of "likes" from the status of which 
    it was originally a part.
    
    For example, the status:
        { 1234 : ("Hello, Mitch", 5) }
    Would be parsed into:
        { "Hello": 5, "Mitch": 5 }
    
    @param status_dict: A dictionary of facebook statuses keyed to their number of "likes."
    @return: A dictionary of all {word in status: # of likes}
    '''
    words_dict = {}
    
    for statusID in status_dict:
        # Split each status into its words
        status = status_dict[statusID][0]
        words = status.split(' ')
        for word in words:
            word = remove_punctuation(remove_emoticons(word))
            
            # Add the words to the dictionary, so long as they are not just punctuation
            if word == "":
                continue
            elif words_dict.has_key(word):
                words_dict[word] += 1
            else:
                words_dict[word] = 1
    
    return words_dict

def remove_punctuation(status):
    ''' 
    Removes the punctuation from a string, converting all newlines into spaces 
    
    @param status: The word from which to remove punctuation
    @return: The status with no punctuation, relegated to one line ('\n' --> ' ')  
    '''
    fixed_status = status.translate(string.maketrans('\n\r', '  '))
    return fixed_status.translate(None, string.punctuation)

def remove_emoticons(status):
    '''
    Removes emoticons from a string
    
    @param status: The word from which to remove punctuation
    @return: The status with common emoticons parsed out.
    '''
    # Remove these objects from the string
    remove_dict = {
                   ':\)':'', ':-\)':'', ':D':'', ':-D':'', ';D':'',
                   ':\/': '', ':\(':'', ':-\(':'', '>:\(':'', '<3':'',
                   ':O': '', ':\'\(':'', ':P':'', ':-P':'', ':\|':'',
                   ':\\':'', ':$':'', '<\/3':''
                   }
    remove_object = re.compile('|'.join(remove_dict.keys()))
    fixed_status = remove_object.sub(lambda m: remove_dict[m.group(0)], status)
    
    return fixed_status

#----------------------------------------------------------------------------------------------

def classify_words(status_dict):
    '''
    Takes a dictionary of statuses and classifies what part of speech each word is.
    
    @param status_dict: A dictionary of statuses keyed to lists of [status_text, likes]
    @return: Dictionary of { speech part : [ list of words in that speech part ] }
    '''
    tag_dict = {}
    for statusID in status_dict:
        # Tag the words in a status and place them in a list of ("word", "tag") tuples
        status = status_dict[statusID][0]
        word_tags = classify_sentence(status)
        
        # Build the dictionary as { speech part : list of words which are that speech part }
        for tag in word_tags:
            if tag_dict.has_key(tag[1]):
                tag_dict[tag[1]].append(tag[0])
            else:
                tag_dict[tag[1]] = [tag[0]]
    
    return tag_dict

def classify_sentence(status):
    '''
    Classifies the words in a sentence using NLTK's default tagger
    
    @param status: A sentence in the form of a string.
    @return: A list of tuples in ("Word", "Speech Part Tag") form
    '''
    word_tags = nltk.pos_tag(nltk.word_tokenize(status))
    return word_tags

#----------------------------------------------------------------------------------------------

test = {'100001066420386_541929349185941': ['Happiness is...\n20. Running through sprinklers.', 1], 
        '1334531204_10200604077258466': ["you're going to have a lot of notifications... sorry. but not really. I'm prepping for our story time. ", 1], 
        '1096793804_10200805407872979': ['Live in Love: Is it really that simple?', 1], 
        '512318607_10151575131243608': ['\\uc790\\uac81\\ud0c0\\uc784\r\n\r\n+ \r\n\r\n\\ubed0\\ub09c\\uba5c\\ub85c\\ub514_\r\nhttp:\\/\\/www.youtube.com\\/watch?v=Jkozsve2oKU', 1], 
        '512318607_10151575137338608': ['\\uc544 \\uc774\\ub7f0\\uac70\\uc2dc \\uc870\\uc73c\\ub2e4 . ', 1], 
        '545130542_10152785859675543': ['Late nights and earlier mornings while paper writing has imparted me the appreciation of bitter and dark coffee, peaceful and silent mornings save the clacking of my keyboard, and the quiet, gradual brilliance of a sunrise.', 5], 
        '662326254_10201103188124553': ['Happy birthday, NJB!!!', 1], 
        '548501150_10201103191364634': ['Happy Birthday!:D', 1]}

print "Dictionary of Words and Likes:"
print assign_likes_to_words(test)
print "\nClassified Words: "
print classify_words(test)