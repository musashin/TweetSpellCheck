TweetSpellCheck
===============

A simple script to analyse a tweeter feed for spelling mistakes, grade the tweet as a function of their quality and mail a report

Sample Call
===============
Below are the argument for a 'sample' call.
The idea is that:
 * The dictionnary (it is enchant speel check dictionnary), user name of the user followed on twitter and the
   mail address to which the report is to be mailed are specified as command arguments.
 * The credentials to twitter and the SMTP server used to mail the report are specified in a config file

The goal is to make it easy to schedule different 'cron' job to differnt users.

	-configFile /home/nicolas/Documents/TweeConfig.ini -followedUser DenisCoderre -language fr_FR -destination toto@gmail.com


sample config file
===============
[TweeterAPI]
consumer_key=toto
consumer_secret=tata
access_token_key=foosdsds
access_token_secret=cxcxcx

[SMTPServer]
server = smtp.gmail.com:587
login  = toto@xmail.com
pwd    = xsxxc


