import system 
import java.io as F
from java.util import Calendar
c=Calendar.getInstance()
tMs=c.getTimeInMillis()
adir = "C:\\IgnitionTextFiles\\"
filename = adir+"Test_File_%d_%d.txt"%(c.get(Calendar.YEAR),c.get(Calendar.DAY_OF_YEAR))
print filename

text=log('test') 

def writeToFile(text):

    line ='\n This is %s'%(text)+'\n'
    fstream = F.FileWriter(filename,1)    
    out = F.BufferedWriter(fstream)
    out.newLine()
    out.write(line)    
    out.close()

writeToFile(text)