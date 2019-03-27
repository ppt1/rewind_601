def Calibrate(): #check calibration

	svc= 'rewind_aux/rewind_aux.svc/process?inString='
	tu_ten = round(system.tag.read('Path/fWindingTensionMe').value,2)
	pf_ten = round(system.tag.read('Path/Calib/fProofTensionCalibCheckMe').value,2)
	
	#pf_tension and tu_tension  nominal setpoint values 
	pf_ns = system.tag.read('Path/Calib/fProofTensionCalibMaxNs').value
	tu_ns = system.tag.read('Path/Calib/fTensionCalibMaxNs').value
	
	#call of inTolerance function
	if shared.main.inTolerance(pf_ns,5.0, pf_ten):
		pf_st = "YES:" #tu status
	else:
		pf_st = "NO:"
	print pf_ten
		
	if shared.main.inTolerance(tu_ns,5.0,tu_ten):
		tu_st = "YES:" #tu status
	else:
		tu_st = "NO:"
	print tu_ten

	mach_no = system.tag.read('Path/mach_no.value')
	oper_id = system.tag.read('Path/oper_id').value.upper()
	data= 'directive=calibrate_mach'	
	data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value) 
	data+= ';oper_id=' + str(system.tag.read('Path/current_oper_id').value) 
	data += ';calibrate_data=POLC:YES:0' + ':' #N/A for nextrom new mach
	data+= ':TULC:' + str(tu_st) + str(tu_ten)  #eg: YES:-55.952:
	data += ':PTLC:'+ str(pf_st) + str(pf_ten)
	
	try:
		sendstring1 = shared.main.PTS_URL + svc + data #UNCOMMENT AFTER TESTING 
		#sendstring1 = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467:'
		shared.main.log(sendstring1)
		print sendstring1
		response = system.net.httpGet(sendstring1)
		shared.main.log(response)
		print response
		
		responsesp = response.split(':')
		
		system.tag.write('Path/instruction', responsesp[6])
		
	except:
		
		shared.main.log('Calibrate send error has occured')
		print 'error'
		
	



def testCalibrate():
	import system

	sendstring1 = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467:'
	
	print sendstring1
	response = system.net.httpGet(sendstring1)
	
	print response
	
	responsesp = response.split(':')
	shared.main.log(response)
	system.tag.write('Path/instruction', responsesp[6])#+responsesp[6])

	#http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=calibrate_mach;mach_no=601;oper_id=277;calibrate_data=POLC:YES:-57.95:TULC:YES:-55.952:PTLC:YES:-63.467: