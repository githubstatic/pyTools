#this is simple demo of read, write file 
#Notice
#   1.open(path, 'r') this function use read-only mode to read file
#   2.readlines() to read a line(include \r)
#   3.strip('\r') to strip out \r
def readFile(path):
    try:
        f = open(path, 'r')
        for line in f.readlines():
            print line.strip('\r')
            print '\t'
    except Exception, e:
        print "[-ERROR-] Read File Failed!"+ str(e)


def writeFile(path):
    try:
        f = open(path, 'w')
        print "wirtting file ..\n"
        for x in range(1,255):
            f.write("10.204.148."+str(x)+'\n')
        print "wirted done! \n"
    except Exception, e:
        print "[-ERROR-] Write File Failed! "+ str(e)

def main():
    path = "tmp/rw.txt"
    writeFile(path)
    readFile(path)

if __name__ == '__main__':
    main()
