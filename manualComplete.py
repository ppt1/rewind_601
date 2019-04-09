#Complete TU 
#triggered by "Complete" button by the PLC 
#Corresponds to TVerifyTakeup Function on NETUTIL.bas 

#COMPLETE TU		
#Example:  http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/completeTU/completeTU.svc/process?inString=mach_no=770;oper_id=117;
#po_id=JRFVY3889A1RVJ;po_serial_id=3800125904;rwr_id=RWR551295121;rwr_serial_id=5206475492;
#plan_length=50550;actual_len=50551;accum_len=50555;tu_color=GR;tu_status=OK;stop_code=STCT;
#mach_speed=1500;spoolRun=Single;I_PO_TEN=66.5:72.7:1.45:69.48;I_TU_TEN=45.4:55.3:1.83:49.78;
#I_PF_TEN=106.1:114.7:1.82:109.75;SPEDGE=30.54:29.77:-0.49:175.56:176.35:0.39:;DEFECT=0:0;MISC=21
import system 
import time
import threading
def manualComplete(temp):
	if temp == 'opln':
		t = threading.Timer(600,shared.main.Send_Email('tapingFail'))
		t.start()
	elif temp == 'tubk' or 'pfbk' or 'pobk':
		t = threading.Timer(600,shared.main.Send_Email('fiberBreak'))
		t.start()
		print 'send email'
	shared.CompleteTU.CompleteTU()
	shared.TUpkg.Send_tupkg()
	system.tag.write('Path/TU/previous_completed',1)
	if temp == 'auto':
		shared.main.log('Spool auto completed')
	else:
		shared.main.log('Spool manually completed')
	
#	system.tag.write('Path/TU/Next_TU_LCU',1) #added this to complete no matter what
#	system.tag.write('Path/TU/NextTU',1)
#	time.sleep(1.5)
#	system.tag.write('Path/TU/Next_TU_LCU',0) #added this to complete no matter what
#	system.tag.write('Path/TU/NextTU',0)
	

