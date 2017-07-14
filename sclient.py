#thi is a simple demo of use socket moudle to connect SMTP server and print banner info
#recv(1024) function is to read next 1024 bytes on the socket
#Notice:
#   1.don't name this script to socket.py(it will crash with socket moudle)
#   2.pay attention to connect() 
import socket
socket.setdefaulttimeout(2)
s = socket.socket()
s.connect(("10.204.148.47",25))
ans = s.recv(1024)
print ans

