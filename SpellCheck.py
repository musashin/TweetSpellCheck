'''
Created on 2013-11-25

@author: nicolas
'''

import enchant
import re

class SpellChecker(object):
    '''
    Class to check tweet for spelling mistakes
    '''

    def __init__(self,language):
        '''
        Constructor
        '''
        self.dictionnary = enchant.Dict(language)
    
    def is_tweet_keyword(self,word):
    
        return re.search('@[\w]',word)!= None or re.search('#[\w]',word)!= None  

    def is_emoticon(self,word):
    
        return re.search('\s(\w+)\s((?::|;|=)(?:-)?(?:\)|D|P))',word) != None

    def is_URL(self,word):
    
        return re.search('http://(\w)*',word) != None
        
    def is_name(self,word):
        return word[0].isupper()
    
    def analyse_tweet(self,tweetText):
        
        number_of_word = 0
        number_of_faults = 0
        
        for word in [w for w in re.split(' |,|\'|\?',tweetText) if w]:
            number_of_word = number_of_word+1
            if not self.dictionnary.check(unicode(word)) \
            and not self.is_tweet_keyword(word) \
            and not self.is_name(word)           \
            and not self.is_URL(word)           \
            and not self.is_emoticon(word) \
            and len(word)>1:
                number_of_faults = number_of_faults+1
         
        if number_of_word >0 :       
            grade = (number_of_word-number_of_faults)/float(number_of_word) * 100.0
        else :
            grade = 100
        
        return (number_of_word,number_of_faults,grade)     

    
        