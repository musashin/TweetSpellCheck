#!/usr/bin/env python
'''
Created on 2013-11-27

Analyze tweets for spelling mistakes, grade them,
and mail a report

Depends on:
  - pyEnchant for spellchecker (http://pythonhosted.org/pyenchant/)
      - sudo apt-get install python-abiword
      - https://pypi.python.org/pypi/pyenchant/1.6.5
      - see http://pythonhosted.org/pyenchant/tutorial.html for installation details
  - sudo apt-get install myspell-fr for install extra language dictionnaries
  - Using Python twitter as a wrapper for the python API ( installed from https://code.google.com/p/python-twitter/)

@author: mushahi
'''
import argparse
import ConfigParser
import twitter
import sys
import SpellCheck
import ReportMailer
 
#Some basic help 
parser = argparse.ArgumentParser('Analyze tweets for spelling mistakes, grade them, and mail a report')
parser.add_argument('-configFile',   help='full path to the configuration file',type=str)
parser.add_argument('-followedUser', help='username to follow',type=str)
parser.add_argument('-language',     help='language dictionary used',type=str)
parser.add_argument('-destination',  help='Email the report shall be sent ',type=str)


def GenerateReport(tweetReportList):
    '''
    Given a list of tupple under the format (number_of_word,number_of_faults,grade,s.text)
    indentify the best and worse tweet. At equivalent grade, prioryt is given to the
    tweet with the longest text
    '''
    
    #find the tweets with the best score
    maxScore = max(tweet[2] for tweet in tweetReportList)
    bestTweetIndex = [i for i, tweet in enumerate(tweetReportList) if tweet[2] == maxScore]
    bestTweetsTexts = [tweetReportList[i][3] for i in bestTweetIndex]
    bestTweetMaxLength = max(len(s) for s in bestTweetsTexts) 
    bestTweet = [s for s in bestTweetsTexts if len(s) == bestTweetMaxLength][0]

    
    #find the tweets with the lowest score score
    minScore =  min(tweet[2] for tweet in tweetReportList)
    worseTweetIndex = [i for i, tweet in enumerate(tweetReportList) if tweet[2] == minScore]
    worseTweetsTexts = [tweetReportList[i][3] for i in worseTweetIndex]
    worstTweetMaxLength = max(len(s) for s in worseTweetsTexts) 
    worseTweet = [s for s in worseTweetsTexts if len(s) == worstTweetMaxLength][0]
    
    biggestFaultCount = max(tweet[1] for tweet in tweetReportList)
    lowestFaultCount = min(tweet[1] for tweet in tweetReportList)
    
    tweetAverage = sum(tweet[2] for tweet in tweetReportList)/float(len(tweetReportList))
   
    return {'number of tweets':len(tweetReportList),
            'average grade': round(tweetAverage,1),
            'best grade':round(tweetReportList[bestTweetIndex[0]][2],1),
            'worse grade':round(tweetReportList[worseTweetIndex[0]][2],1),
            'biggest number of faults in a tweet':biggestFaultCount,
            'smallest number of faults in a tweet':lowestFaultCount,
            'best tweet':bestTweet,
            'worse tweet':worseTweet}
           
    
def print_report(report):
    '''
    Given a dictionary, return a text with each dictionary key turned in a lie
    with the following format:
    \tab-key : value
    '''
    text = ''
    for keys,values in report.items():
        text = text + '\t-' + str(keys) + ' : '+ str(values) + '\n'
        
    return text

def read_configuration(filePath):
    '''
    Read the configuration file for credential to the twitter API and
    credential to the SMTP server
    '''
    
    expected_api = ('consumer_key','consumer_secret','access_token_key','access_token_secret')
    SMTPServer   = ('server','login','pwd')
    
    config = ConfigParser.ConfigParser()
    config.readfp(open(filePath))
    
    for opt in expected_api:
        if not config.has_option('TweeterAPI', opt):
            sys.exit("TweeterAPI section need {}".format(opt))
        
    for option in SMTPServer:
        if not config.has_option('SMTPServer', option):
            sys.exit("SMTPServer section need {}".format(option))
   
    return (config)

def  read_tweets(TweeterAPI,followedUser):
    '''
    Read tweets for the specified user name
    '''
    statuses = None
    try:
        api = twitter.Api(consumer_key=config.get('TweeterAPI', 'consumer_key', 0),
                          consumer_secret=config.get('TweeterAPI', 'consumer_secret', 0),
                          access_token_key=config.get('TweeterAPI', 'access_token_key', 0),
                          access_token_secret=config.get('TweeterAPI', 'access_token_secret', 0))
        
    except Exception as e:
        print "Could not connect to twitter: ", e.message
    
    try:
        statuses = api.GetUserTimeline(screen_name=followedUser,count=200)

    except Exception as e:
        print "Could not connect to retrieve status for user {} ({}): ".format(followedUser,e.message)
   
    return statuses

if __name__ == '__main__':
    
    args    = parser.parse_args()
    
    config  = read_configuration(args.configFile)
    
    spellCheck = SpellCheck.SpellChecker(args.language)
        
    statuses = read_tweets(config,args.followedUser)
    
    if statuses is not None:  
        tweetReportList = list()
        for s in statuses:
            (number_of_word,number_of_faults,grade) = spellCheck.analyse_tweet(s.text)
            tweetReportList.append((number_of_word,number_of_faults,grade,s.text))
      
        if len(tweetReportList)>10:
            text = 'Latest tweets:\n'
            latestReport = GenerateReport(tweetReportList[:len(tweetReportList)/2])
            text = text+print_report(latestReport)
            previousReport = GenerateReport(tweetReportList[len(tweetReportList)/2+1:])
            text = text+'Previous tweets:\n'
            text = text+print_report(previousReport)
    
        else :
            report = GenerateReport(tweetReportList)
            text = 'Latest tweets:\n'
            text = text+print_report(report)
        
        mail = ReportMailer.ReportMailer()
        
        try: 
            mail.SendReport(config=config, 
                            destinationEmail=args.destination,
                            tweetAuthor=args.followedUser,
                            text=text)
        except Exception as e:
            print "Could not mail report to {} ({}): ".format(args.destination,e.message)
   
    else:
        sys.exit('Could not read tweets')
    
    
