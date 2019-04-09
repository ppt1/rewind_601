#[2018.05.11 00:24:40] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=mach_start;start_length=23;line_speed=746;mach_no=770;oper_id=251
#[2018.05.11 00:24:40] ! VBC INET got: 770:251:RWD:AUX:mach_start:0:
import system
import traceback
import time
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/mach_running


def mach_start(): #machine start
	svc = 'rewind_aux/rewind_aux.svc/process?inString='

	
	data = 'directive=mach_start'
	data+= ';start_length=' + str(system.tag.read('Path/take_len').value)
	data+= ';line_speed=' + str(system.tag.read('Path/maxLineSpeed').value)
	data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value) #JIH read tag since sometime main value was none
	data+= ';oper_id=' + str(system.tag.read('Path/current_operid').value)

	
	try:
		sendstring1 = shared.main.PTS_URL + svc + data
		
		
		response1 = system.net.httpGet(sendstring1)
		print response1	
		shared.main.log(response1)
		
		response1sp = response1.split(':')
		
		if response1sp[5] == '0':
			system.tag.write('Path/instruction',"Machine started with no errors")
		else:
			x = "Error in starting"
			shared.main.log(x)
		

	except:
		shared.main.log('Machine Start:' + traceback.format_exc())
		
	shared.main.log(sendstring1)
		
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU	
def mach_stop():
	
#[2018.05.24 13:11:08] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=mach_stop;stop_reason=STCT;stop_length=50723;mach_no=770;oper_id=334
#[2018.05.24 13:11:08] ! VBC INET got: 770:334:RWD:AUX:mach_stop:0:
	time.sleep(0.5)
	svc = 'rewind_aux/rewind_aux.svc/process?inString='
	data = 'directive=mach_stop'
	stop_length =  str(system.tag.read('Path/TU/take_len').value)
	stop_code = shared.main.Stop_code() 
	shared.main.log(stop_code)
	system.tag.write('Path/stop_code',stop_code)	
	
	data+= ';stop_reason=' + stop_code#stop_reason
	data+= ';stop_length=' + stop_length
	data+= ';mach_no=' + '601'
	data+= ';oper_id=' + str(system.tag.read('Path/current_operid').value)
	
	#if tapingDone == True:
	sendstring1 = shared.main.PTS_URL + svc + data
	print sendstring1 
	shared.main.log(sendstring1)
	
	response1 = system.net.httpGet(sendstring1)
	print response1	
	shared.main.log(response1)
	
	response1sp = response1.split(':')
	
	#if response1sp[5] == '0': #JIH removed if statement so complete works when PTS communication did not
	system.tag.write('Path/NextTU','true')
	system.tag.write('Path/instruction', 'Machine Stopped')
	time.sleep(1)
	system.tag.write('Path/NextTU','false')
	tapingDone = False
	#else:
	#	system.tag.write('Path/NextTU','false')

	
