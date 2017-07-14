#this is a simple demo of python functions and execption handling
#
import socket

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024) 
        return banner
    except Exception, e:
        return "[-ERROR-] "+ str(e)

def main():
    ip = "10.204.148.47"
    port = 25
    banner = retBanner(ip, port)
    if banner:
        print banner
    else:
        print "connect server failed"

if __name__ == '__main__':
    main()

