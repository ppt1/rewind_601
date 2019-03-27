import system
import traceback
import time 
import math 
from time import strftime
#THIS FUNCTION IS CALLED When Get_ID button is pressed

#send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=state;mach_no=750;oper_id=JAM
#got: 750:JAM:RWD:AUX:state:0:MUNZ JOHN A:???:???:???:???:0:???:MainRoom:CALIBRATE:ONLINE:ON:250000:250000:PAYOUT:UNCL:FIBCOLOR:??:JAM:PAYSPL:??:TAKSPL:??:TAKLEN:0:CUTLEN:0:PAYLEN:0:PROOFTEST:0:CLMODE:??:TAKTEN:???:TAKPIT:???:PAYTEN:???:DIETEN:???:ISELEN:0:MAXSPEED:0:ORDER:NO:DSM751:AIRLNTH:0:AIRDNSE:0:TWIST_V:0:TWIST:N:SEDGBGN:0:SEDGEND:0:no:TASKASGN:NO:NONE:

def GetSpool():

	try:
		PTS_URL = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
		svc = 'rewind_aux/rewind_aux.svc/process?inString=directive=state;'
		x= system.tag.read('Path/mach_no').value
		y= system.tag.read('Path/current_operid').value
		
		data = 'mach_no=' + str(x) + ';'
		data += 'oper_id=' +str(y)
	
		getSpoolSend = shared.main.PTS_URL + svc + data
		shared.main.log(getSpoolSend)
		print  shared.main.PTS_URL + svc + data
		response1 = system.net.httpGet( shared.main.PTS_URL + svc + data)
		print response1
		time.sleep(1)
		shared.main.log(response1)
		response1sp = response1.split(':')
		if response1sp[5]=='0': #response is GOOD 
			system.tag.write('Path/instruction','Machine on task assignment? ' + response1sp[67] + ', Next Draw Spool=' + response1sp[68])
			system.tag.write('Path/nextDrawID',response1sp[68])			
		else:
			system.tag.write('Path/instruction','Cannot GetID. Verify you are logged in and machine on assignment')								
	except:
		shared.main.log ('Get_ID Error: '+traceback.format_exc())	
		
	
	