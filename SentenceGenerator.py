'''
    SentenceGenerator.py generates a random sentence using
    the words and probabilities from earlier parts of this project.
    
    This generator is going to use probabilities in two ways. The first is going to be
    to take complete sentences (from Stephen) and weight each sentence structure based on how often it appears.
    In this way, not only are the words weighted, but the different sentence structures will appear
    with varying probabilities.
    
    The second use of the probabilities will come from Matt. He is sending me a dictionary of (word, value) pairs
    which I will use in a similar way to grab sentences with some of the most liked words.
    
    Written by: MitchVz
    Date: 5/7/2013
    '''

import nltk
import random
import FacebookScraper
import classify

'''
    chooseStructure will take a list of strings and choose a grammatical structure to use based on the most common grammatical structure
    found in those sentences. The parsing of the sentences is going to be similar to what Matt did with classify words
    '''
def chooseStructure(allStatuses):
    
    # taggedStatuses will be a list of the statuses with only the parts of speech
    taggedStatuses = []
    
    for status in allStatuses:
        taggedWords = nltk.pos_tag(nltk.word_tokenize(status))
        
        justTags = []
        # Now take those tags and put them in a dictionary
        for aTuple in taggedWords:
            justTags.append(aTuple[1])
    
        taggedStatuses.append(justTags)

    # At this point, taggedStatuses contains a bunch of structures and we will simply choose a structure
    randomIndex = random.randrange(0, len(taggedStatuses))
    theRandomStructure = taggedStatuses[randomIndex]
    
    return theRandomStructure

'''
    createSentence will receive a grammarStructure chosen by chooseStructure and a list of words keyed to likes
    and will fill the grammar structure with words based on the number of likes each word received
    '''
def createSentence(grammarStructure, posWordDict, likesWordDict):
    newStatus = ""
    
    keyedWords = []
    # First we loop through the list of PoS in the grammarStructure and grab a word for each part of speech
    for posKey in grammarStructure:
        keyedWords = (posWordDict[posKey])
        
        myListOfWords = []
        # Now for each word in that part of speech, we take the number of likes it has been given, and write it
        # that many times to a list of words. Later, we will choose a word from that list of words
        for aWord in keyedWords:
            numLikes = likesWordDict[aWord]
            for i in range(numLikes):
                myListOfWords.append(aWord) # append a word numLikes times
    
        # now we choose a random word from myListOfWords
        randomIndex = random.randrange(0, len(myListOfWords))
        chosenWord = myListOfWords[randomIndex]
    
        # and finally, add the word to the new status
        newStatus += chosenWord + " "

    newStatus += "."
    return newStatus

#--------------------------------------------------------------


#This is the main method for our program (it runs Matt's code as well)
stephenDict = FacebookScraper.getPostDict()


# theStatuses will be a list of statuses that stephen gives me
theStatuses = []
# This will go through every sentence and add it to theStatuses
for key, value in stephenDict.iteritems():
    theStatuses.append(value[0])
print theStatuses

print "The chosen structure is:"
theStructure = chooseStructure(theStatuses)
print theStructure
print "The classified words are:"
classyWords = classify.classify_words(stephenDict)
print classyWords
print "The dictionary of likes is:"
likesDictionary = classify.assign_likes_to_words(stephenDict)
print likesDictionary


randomlyGeneratedStatus = createSentence(theStructure, classyWords, likesDictionary)
print randomlyGeneratedStatus

print "done"