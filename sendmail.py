#this is a simple py task script  

import socket
import time
import base64
import md5
import random

PATH = "log/sendmail.log"

#getTime according specify format
def getTime(format):
    #return the time format like 2017-07-17 15:34:23
    if(format == 1):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        return time.strftime(ISOTIMEFORMAT, time.localtime());
    #return the time format like Sun Jun 15:34:23 2017
    elif(format == 2):
        return time.asctime( time.localtime(time.time()) )

def printErr(msg):
    print "[-]Error "+ getTime(1) + ' ' + msg +'\n'

def saveLog(msg, flag):
    if flag == 1:
        log = '[-]Error '+ getTime(1) + ' ' + msg +'\n'
    elif flag == 2:
        log = '[-]Warning '+ getTime(1) + ' ' + msg + '\n'
    elif flag == 3:
        log = '[*]Debug '+ getTime(1) + ' '+ msg + '\n'
    else:
        log = '[+]Normal '+ getTime(1) + ' '+ msg + '\n'
    
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
def sendMailCore(fr, to, data):
    s = socket.socket()
    #make sure to connect server
    try:
        while True:
            s.connect(("10.204.148.47", 25))
            banner = s.recv(1024)
            if banner[:3] == '220':
                break
            else:
                saveLog("Connect return: "+ banner, 3)
        while True:
            s.send("EHLO kali.mei.com\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
            else:
                saveLog("EHLO return: "+ banner, 3 )
        while True:
            s.send("MAIL FROM:<"+ fr +">\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
            else:
                saveLog("FROM return: "+ banner, 3)
        while True:
            s.send("RCPT TO:<"+ to +">\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
            else:
                saveLog("RCPT return: "+ banner, 3)
        while True:
            s.send("DATA\r\n")
            ret = s.recv(1024)
            if ret[:3] == '354':
                break
            else:
                saveLog("DATA return:"+ banner, 3)
        while True:
            s.send(data.encode('utf-8'))
            s.send("\r\n.\r\n")
            ret = s.recv(1024)
            if ret[:3] == '250':
                break
            else:
                saveLog("DATA OVER return: "+ banner, 3)
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
        return False
    
def makeContent(fr, to, subject, data, isHtml=False, Path=None):
    mail_template = '''Date: {date}\r\nFrom: <{from}>\r\nTo: <{to}>\r\nSubject: {subject}\r\nX-priority: {priority}\r\nX-Mailer: Charmail 1.0.0[cn]\r\nMIME-Version: 1.0\r\nContent-Type: multipart/alternative;\r\n\tboundary="-----=_Part_{random}_=-----"\r\n{content}\r\n-------=_Part_{random}_=-------'''

    text_content_template = '''-------=_Part_{random}_=-----\r\nContent-Type: text/plain;\n\tcharset="UTF-8"\r\nContent-Transfer-Encoding: base64\r\n\r\n{content}\r\n'''

    html_content_template = '''-------=_Part_{random}_=-----\r\nContent-Type: text/html;\r\n\tcharset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n{content}\r\n'''

    attachment_content_template='''-------=_Part_{random}_=-----\r\nContent-Type: {type};\r\n\tname={name}\r\nContent-Transfer-Encoding: base6\r\nContent-Disposition: attachment;\r\n\tfilename={name}\r\n{content}\r\n'''

    attachment_type = ['text/plain', 'application/zip', 'image/jpeg']

    #make random string
    fr_len = len(fr)
    fr_len_2 = int(fr_len/2)
    to_len = len(to)
    to_len_2 = int(to_len/2)
    sub_len = len(subject)
    sub_len_2 = int(sub_len/2)
    rand = fr[random.randint(0,fr_len_2) : random.randint(fr_len_2,fr_len)] + to[ random.randint(0,to_len_2) : random.randint(to_len_2, to_len)] + subject[ random.randint(0,sub_len_2) : random.randint(sub_len_2, sub_len)]
    md = md5.new()
    md.update(rand)
    rand = md.hexdigest()

    if isHtml == True:
        content = html_content_template
        content = content.replace('{content}', data)
        content = content.replace('{random}', rand)
    else:
        content = text_content_template
        content = content.replace('{content}', base64.b64encode(data))
        content = content.replace('{random}', rand)
    #make attachment content later

    #make the total mail content
    mail_template =  mail_template.replace('{date}', getTime(2))
    mail_template =  mail_template.replace('{from}', fr)
    mail_template =  mail_template.replace('{to}', to)
    mail_template =  mail_template.replace('{subject}', subject)
    mail_template =  mail_template.replace('{priority}', '3')
    mail_template =  mail_template.replace('{random}', rand, 5)
    mail_template =  mail_template.replace('{content}', content)
    
    return mail_template
    
def sendMail(fr, to, subject, data, isHtml=False, Path=None ):
    return sendMailCore(fr, to, makeContent(fr, to, subject, data, isHtml, Path) )

def main():
    #makeContent('from@abc.com', 'to@abc.com', 'make content test', 'this is mail content data')
    result =  sendMail('mei@trendmei.com', 'myl@trendmei.com', 'Charmail test' ,'''
            <!DOCTYPE html>
            <html><head></head><body>hello html</body></html>
            ''')
    #result = sendMailCore('mei@trendmei.com', 'myl@trendmei.com', 'Charmail test')
    if result == True:
        print "Successed"
        saveLog("Mail Send Success", 5)
    else:
        print "Failed"
        saveLog("Send Mail Failed", 3)

if __name__ == '__main__':
    main()
    
    
