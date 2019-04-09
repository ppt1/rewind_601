#######################################################
#GENERAL MACH VALUES 
#######################################################
import time 



mach_no = system.tag.read('Path/mach_no')

target = 'pts'

if target == 'dev':
	PTS_URL='http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
else:
	PTS_URL='http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'

from time import gmtime, strftime

timestamp = (strftime("%Y-%m-%d %H:%M:%S"))
#######################################################

from time import gmtime, strftime
import system 
import java.io as F
from java.util import Calendar

c=Calendar.getInstance()
tMs=c.getTimeInMillis()
adir = "C:\\postdraw\\"
print c.get(Calendar.DAY_OF_MONTH)
day = (c.get(Calendar.DAY_OF_MONTH)) # days 0 thru 9 have a leading 0. 
month = c.get(Calendar.MONTH)+1
if day < 10 :
	print day
	day = '0'+ str(day)
if  month < 10: 
	month = '0'+str(month)
	
filename = adir+"zlog-%d.%s.%s.txt"%(c.get(Calendar.YEAR),month,(day))
print filename

#######################################################
#SEND EMAIL
##################################################
#ileName = filePath.split("\\")[-1]

def Send_Email(temp):

	#fileData = fpmi.file.readFileAsBytes(filePath)
	if temp == 'TU_Rejects':
		subject = 'Multiple Takeup Spool Rejects' #reason code for the issue and send email for the take up spools rejected
		body = system.tag.read('Path/instruction').value
	elif (temp == 'fiberBreak') and (system.tag.read('Path/mach_running').value==0):
		subject = 'Fiber Break. Attention Required.'
		body =   'Fiber break occured on '+ str(system.tag.read('Path/mach_no').value)+'.'#str(system.tag.read('Path/stop_code').value)
	elif temp == 'tapingFail':
		subject = '601 Attention Required'
		body = 'Auto-taping Failed, Operator attention required.'
	elif temp == 'mach_idle':
		subject = '601 Machine idle'
		body = 'Machine has been idle for over 25 minutes, Operator attention required. Active PO ' + str(system.tag.read('Path/po_fiberID').value)

	smtp = "mail.ofsoptics.com"
	sender = "REW601@OFS"
	#recipients = ["pcharles@ofsoptics.com"]
	recipients = ["jheim@ofsoptics.com","pcharles@ofsoptics.com",'jmunz@ofsoptics.com','dbalfour@ofsoptics.com','twilliamson@ofsoptics.com','rflores@ofsoptics.com']
	system.net.sendEmail(smtp, sender, subject, body, 0, recipients)#, [fileName], [fileData])	
#Function to display log on the root container 

	#Function to log files on 
	########################################################
	
def writeToFile(text):
	
	line = (strftime("[%Y.%m.%d  %H:%M:%S] "))+ (text)+'\n'
	fstream = F.FileWriter(filename,1)    
	out = F.BufferedWriter(fstream)
	out.newLine()
	out.write(line)    
	out.close()
	  
y=""

def log(x):
			
	shared.main.y = shared.main.y + (strftime("[%Y.%m.%d   %H:%M:%S]")) + " " +x +"\n"    
	system.tag.write('displayMsg',shared.main.y)
	writeToFile(x)
	return x


###################################################################################
#custom tolerance function. Parameter description
#returns bool. isRange = 1, not in range = 0
#test = the value you want to test. variable value. type = float
#toleranceVal = % value! the +- value, written in percentage. 
#num = constant, float, constant value 
#mode = PERCENTAGE or actual value. mode = 1 for PERCENTAGE and 0 for float tolerance value
#therefore: 10+-5% will be written as: isRange = inTolerance(10,5,testVariable)
########################################################
def inTolerance(num, toleranceVal,test,mode):

	toleranceVal = toleranceVal * 1.0 #convert to float
	if mode == 1: #if tolerance value is in percentage, convert to a float 
		x =  num * (toleranceVal/100)*1.0 #converted to float
	else:
		x=toleranceVal
	
	
	#print x
	maxVal = num + abs(x)
	minVal = num - abs(x)
	#return float(minVal), float(maxVal)
	#print minVal, maxVal
	
	if test <= maxVal and test>=minVal:
		isRange = 1
	else: 
		isRange = 0
	return isRange
#######################################################
#LOG LENGTH EVERY 5 SECONDS	
#######################################################
def logLength():
	data = 'TU SERIAL = '+ str(system.tag.read('Path/TU/tu_serialID').value)
	data+= str(system.tag.read('Path/TU/take_len').value)
	shared.main.log(data)
	time.sleep(5)


#######################################################
	
def toggle(tagPath): #toggle values. make flags momentary
	
	temp = system.tag.read(tagPath)
	
	if temp == '1':
		system.tag.write(temp,'false')
	else:
		system.tag.write(temp,'false')


########################################################
#STOP CODE 
########################################################
def Stop_code():

				
			if (system.tag.read('Path/TUBK').value)==1:# and system.tag.read('Path/PFBK').value ==1) or (system.tag.read('Path/TUBK').value == 1):
				code = 'TUBK'
				print 'TUBK'
			elif system.tag.read('Path/PFBK').value == 1:
				code = 'PFBK'
				print 'pfbk'
				shared.main.log('PFBK occured')
				system.tag.write('Path/instruction', 'PFBK')
			elif system.tag.read('Path/STCT').value == 1:
				code= 'STCT'
				print 'stct'
			elif system.tag.read('Path/bPOBK').value == 1:
				code = 'POBK'
				print 'pobk'
				
			else:
				code = 'PFBK'
				
			if system.tag.read('Path/TU/take_len').value < 5: #added on 2/25/19 PPC ; OPLN = auto tapingFailure
				code = 'OPLN'
				shared.main.log('Auto taping Failure occured')
			
			
			return code
			
########################################################
#LOGOUT LOGIC 			
#######################################################

def Logout():
		   	system.tag.write('Path/operValid',0)
		   	system.tag.write('Path/oper_name',"")
		   	system.tag.write('Path/oper_id',"")
		   	system.tag.write('Path/oper_password',"")
		   	system.tag.write('Path/operValid',"false")
		   	
		   	
		   	
########################################################
#COLLECT DATA		
#######################################################
def collect_data():
	while (system.tag.read('Path/mach_running').value == 1) and not (system.tag.read('Path/mach_stopped').value==1):
		length_run = system.tag.read('Path/TU/take_len').value
		shared.main.log('RUN LENGTH - ' + str(length_run))	
		time.sleep(7)


def ackDancer():
		system.tag.write('Path/TU/NextTU',1)
		system.tag.write('Path/TU/Next_TU_LCU',1)
		time.sleep(1)
		system.tag.write('Path/TU/NextTU',0)
		system.tag.write('Path/TU/Next_TU_LCU',0)
		system.tag.write('Path/instruction', 'Dancer Fault acknowledged, ready for the Next TU spool')
		shared.main.log('Dancer Fault acknowledged. Ready for the Next TU spool') 
		
def Fiber_Break():
		
	shared.main.Stop_code()
	shared.CompleteTU.CompleteTU()
	
	shared.TUpkg.Send_tupkg()
	system.tag.write('Path/mach_start_after_taping',0)

import threading 
def SetupTU_timer():
	print 'timer Done!'

#arg1= time in ms
#arg2 = function to execute when timer is done

def startTimer(temp):
	if temp == 'TU':
		
		threading.Timer(250, SetupTU_timer).start() #hello function will be executed after 4seconds
