#This is a simple to test unix password by crypt module
#Excute UnixPwdCracker.py need root role, becase the /etc/shadow file only root user to read
#
#Root user's password after encrypted store in /etc/shadow. And the format such as:
#   user:$id$salt$encrypted::::::
#$id$ mean different encrypt algorithm, relationship as fellow:
#   $1$     =>  MD5
#   $2$     =>  Blowfish
#   $2a$    =>  eksBlowfish
#   $5$     =>  SHA256
#   $6$     =>  SHA512
#Notice:
#   1.You can change default encrypt algorithm in /etc/login.defs
#   2.Most *nix system's default algotithm is SHA512
#   3.More infomation of shadow file refer to http://www.tldp.org/LDP/lame/LAME/linux-admin-made-easy/shadow-file-formats.html Or http://www.yourownlinux.com/2015/08/etc-shadow-file-format-in-linux-explained.html
#In python we use crypt module to calculate encrypted password and compare with /etc/shadow file content: the core step as follow:
#   crypt.crypt('password in dictionary', '$6$salt$')


import crypt

def testPass(cryptPass, salt):
	dictFile = open('dictionary/password.txt', 'r')
	for word in dictFile.readlines():
		word = word.strip("\n")
		cryptWord = crypt.crypt(word, salt)
		if(cryptWord == cryptPass):
			print "[+] Found Password "+ word +"\n"
			return
	print "[-] Password Not Found.\n"
	return

def main(user):
	passFile = open('/etc/shadow', 'r')
	for line in passFile.readlines():
		if user+":" in line:
			passField = line.split(':')[1].strip(' ')
           		cryptPass = passField
           		passField = passField.split('$')
           		salt = '$'+ passField[1] +'$'+ passField[2] +'$'
			print '[*] Cracking Password For: '+user
			testPass(cryptPass, salt)
			break

if __name__=="__main__":
	main("root")
		
