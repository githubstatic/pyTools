#this is a simple py task script  

import socket
import time
import base64
import md5
import random

PATH = "log/sendmail.log"


def getTime():
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime(ISOTIMEFORMAT, time.localtime());

def printErr(msg):
    print "[-]Error "+ getTime() + ' ' + msg +'\n'

def saveLog(msg, flag):
    if flag == 1:
        log = '[-]Error '+ getTime() + ' ' + msg +'\n'
    elif flag == 2:
        log = '[-]Warning '+ getTime() + ' ' + msg + '\n'
    elif flag == 3:
        log = '[*]Debug '+ getTime() + ' '+ msg + '\n'
    else:
        log = '[+]Normal '+ getTime() + ' '+ msg + '\n'
    
    try:
        f = open(PATH, 'a')
        f.write(log)
        f.close()
    except Exception, e:
        printErr(str(e))
    
#sendmail is the main funciton in this script
#fr mail form
#to mail to
#data mail content
def sendmail(fr, to, data):
    s = socket.socket()
    #make sure to connect server
    try:
        while True:
            s.connect(("10.204.148.47", 25))
            banner = s.recv(1024)
            if banner[:3] == '220':
                break
            else:
                saveLog("Line 43 Error", 3)
        while True:
            s.send("EHLO kali.mei.com\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
        while True:
            s.send("MAIL FROM:<"+ fr +">\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
        while True:
            s.send("RCPT TO:<"+ to +">\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
        while True:
            s.send("DATA\r\n")
            ret = s.recv(1024)
            if ret[:3] == '354':
                break
            else:
                saveLog("Line 63 Error", 3)
        while True:
            s.send(data.encode('utf-8'))
            s.send("\r\n.\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
            else:
                saveLog("Line 71 Error", 3)
        while True:
            s.send("QUIT\r\n")
            ret = s.recv(1024)
            if ret[:3] == '221':
                break
            else:
                saveLog("Line 79 Error", 3)
        
        s.close()
        return True
    except Exception, e:
        saveLog(str(e), 1)
    
def makeContent(fr, to, subject, data, isHtml=False, Path=None):
    mail_template = '''
    Date: {date}\n
    From: {from}\n
    To: {to}\n
    Subject: {subject}\n
    X-priority: {priority}\n
    X-Mailer: Charmail 1.0.0[cn]\n
    Content-Type: multipart/alternative;\n
        boundary="-------=_Part_{random}_=-------"\n
    This is a multi-part message in MIME format.\n\n
    {content}
    -------=_Part_{random}_=-------\n
    '''

    text_content_template = '''
    -------=_Part_{random}_=-------
    Content-Type: text/plain; charset=UTF-8\n
    Content-Transfer-Encoding:base64\n
    {content}
    '''

    html_content_template = '''
    -------=_Part_{random}_=-------
    Content-Type: text/html; charset=UTF-8\n
    Content-Transfer-Encoding: quoted-printable\n
    {content}
    '''

    attachment_content_template='''
    -------=_Part_{random}_=-------
    Content-Type: {type}; name={name}\n
    Content-Transfer-Encoding: base6\n
    Content-Disposition: attachment; filename={name}\n
    {content}
    '''

    attachment_type = ['text/plain', 'application/zip', 'image/jpeg']

    #make random string
    fr_len = len(fr)
    fr_len_2 = int(fr_len/2)
    to_len = len(to)
    to_len_2 = int(to_len/2)
    sub_len = len(subject)
    sub_len_2 = len(sub_len_2/2)
    rand = fr[random.randint(0,fr_len_2) : random.randint(fr_len_2,fr_len)] + to[ random.randint(0,to_len_2) : random.randint(to_len_2, to_len)] + subject[ random.randint(0,sub_len_2) : random.randint(sub_len_2, sub_len)]
    md = md5.new()
    md.update(rand)
    rand = md.hexdigest()

    if isHtml == True:
        content = html_content_template
        content.replace('{content}', data)
    else:
        content = text_content_template
        content.replace('{content}', base64.b64encode(data))
    #make attachment content later

    #make the total mail content
    mail_template.replace('{date}', getTime())
    mail_template.replace('{from}', fr)
    mail_template.replace('{to}', to)
    mail_template.replace('{subject}', subject)
    mail_template.replace('{priority}', 3)
    mail_template.replace('{random}', rand)
    mail_template.replace('{content}', content)



def main():
   result =  sendmail('mei@trendmei.com', 'myl@trendmei.com', "this is a test mail access IMSS by SMTP cammond code .")
   if result == True:
       saveLog("Mail Send Success", 5)

if __name__ == '__main__':
    main()
    
    
