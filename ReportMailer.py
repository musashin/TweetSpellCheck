'''
Created on 2013-11-25

@author: nicolas
'''

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

class ReportMailer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def SendReport(self,config,destinationEmail,tweetAuthor,text):
        
        msg = MIMEText(text)
    
        msg['Subject']  = 'Tweet Spell Check for ' + tweetAuthor
        msg['From']     = config.get('SMTPServer', 'login', 0)
        msg['To']       = destinationEmail
       
        server = smtplib.SMTP(host=config.get('SMTPServer', 'server', 0),timeout=30)
        
        server.starttls()
        server.login(config.get('SMTPServer', 'login', 0),config.get('SMTPServer', 'pwd', 0))
        server.sendmail(config.get('SMTPServer', 'login', 0), [destinationEmail], msg.as_string())
        server.quit()
        
        
   