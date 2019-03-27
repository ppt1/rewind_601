import system 
import time
import math
#operator login function, that passes the PTS Url and service. Maybe change later 
import traceback

#def a function at each state. directive or state of the machine 
#directive=Logon 
#for sale spools, not Tspool, you logon at every instance. 
#PTS_URL = "http://devpts.ganor.ofsoptics.com/norcross/pts/rewind/svc/"


# (Path/OperLogonReady) = Ready to run the _1_Oper_Logon script
def SendURL(URL,svc,data):
	send_data = URL + svc + data
	
	return send_data



#Oper Logon send event 
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/OperLogonReady
def Logon():
#dev PTS_URL. change for prod
	
	svc = "rewind_aux/rewind_aux.svc/process?inString="	
	directive1 = "oper_logon"
	mach_no = system.tag.read("Path/mach_no")
	if system.tag.read("Path/bTrue4").value == True: #JIH option to login through Ignition
		oper_id = system.tag.read("Path/layout_id")
		if len(system.tag.read("Path/layout_id").value) == 5:
			oper_pw = "BadgeNb"
		else:
			oper_pw = system.tag.read("Path/layout_pw") #'BadgeNb'
	else:
		oper_id = system.tag.read("Path/oper_id")
		if len(system.tag.read("Path/oper_id").value) == 5:
			oper_pw = "BadgeNb"
		else:
			oper_pw = system.tag.read("Path/oper_password").value #'BadgeNb'
	#layout_id = "XXX"
	#layout_passwd = "XXXXXX"
	
	postData = "directive=" + directive1 +';' 
	postData += 'mach_no=' + str(mach_no.value) + ';'
	postData += 'oper_id=' + str(oper_id.value.upper()) + ';'
	if system.tag.read("Path/bTrue4").value == True:
		if len(system.tag.read("Path/layout_id").value) == 3:
			postData += 'oper_passwd=' + str(oper_pw.value.upper())
		else:
			postData += 'oper_passwd=' + oper_pw	
	else:
		if len(system.tag.read("Path/oper_id").value) == 3:
			postData += 'oper_passwd=' + str(oper_pw.value.upper())
		else:
			postData += 'oper_passwd=' + oper_pw
	sendstring1 = SendURL(shared.main.PTS_URL,svc,postData)#PTS_URL + svc + postData #sendstring1 is directive=oper_logon
	print sendstring1
	shared.main.log(sendstring1)
	
	try:#send string to get a response
		
		response1 = system.net.httpGet(sendstring1)
		print response1
		shared.main.log(response1)
	
		
		loginResponseSp = response1.split(":") #response split to get members of the array
	
			
		if loginResponseSp[5] == "0":
			operlogonValid = 1 #binary
			 #valid =0 invalid <>0
			system.tag.write("Path/operValid",operlogonValid) #binary logon valid
			system.tag.write('Path/instruction', 'Operator Logged in: ' + str(system.tag.read('Path/oper_name').value))
			
	
			#########################################################################################int
			
		#quantify inital login. Logout itself after a while 
		#machine stop code = 05 Check the code
		#check for state at every login
			directive2 = "state"
			postData2= "directive=" + directive2 +';' 
			postData2+= 'mach_no=' + str(mach_no.value) + ';'
			postData2+= 'oper_id=' + str(oper_id.value)
			
			sendstring2 = shared.main.PTS_URL + svc + postData2 #Sendstring2 = directive=state. get the state of the machine. 
			shared.main.log(sendstring2)
			stateRes= system.net.httpGet(sendstring2)
			shared.main.log(stateRes)
			 
			
			stateRessp = stateRes.split(':') #StateRes Split - State Response Split 
			#print stateRes
			
	
			if stateRessp[5] == '0': #check for validity 
				system.tag.write('Path/stateResValid',1)
				system.tag.write('Path/instruction', stateRessp[6])
				system.tag.write('Path/po_type',stateRessp[7])
				print stateRes
				
			
			else: 
				system.tag.write('Path/stateResValid',0)
				system.tag.write('Path/instruction',stateRessp[6]+'. '+stateRessp[7])	
				shared.main.log(stateRessp[6]+'. '+stateRessp[7])
				#TEST print 
				
			
			#770:231:RWD:AUX:state:0:HORN JOHN:???:???:???:???:-2:???:MainRoom:CALIBRATE:ONLINE:ON:0:250000:PAYOUT:UNCL:FIBCOLOR:??:231:PAYSPL:??:TAKSPL:??:TAKLEN:0:CUTLEN:0:PAYLEN:0:PROOFTEST:0:CLMODE:??:TAKTEN:???:TAKPIT:???:PAYTEN:???:DIETEN:???:ISELEN:0:MAXSPEED:0:ORDER:NO:DSM751:AIRLNTH:0:AIRDNSE:0:TWIST_V:0:TWIST:N:SEDGBGN:0:SEDGEND:0:no:TASKASGN:NO:NONE:
				
					
			size_stateRes = stateRes.count(':')
					
			
		#SEE LINE 154 FOR DETAILS.	
		#INTERMEDIATE VALUE TAGS FROM EXCEL SHEET
			system.tag.write("Path/mach_no", stateRessp[0])          #
			system.tag.write("Path/oper_id", stateRessp[1])          #
			#system.tag.write("Path/valid", stateRessp[5])          #
			system.tag.write("Path/oper_name", stateRessp[6])          #
			system.tag.write("Path/po_fiberID", stateRessp[7])          #
			system.tag.write("Path/po_serID", stateRessp[8])          #
			system.tag.write("Path/TU/tu_fiberID", stateRessp[9])          #
			system.tag.write("Path/TU/tu_serID", stateRessp[10])          #
			system.tag.write("Path/PayoutLenSofar", stateRessp[11])          #
			#system.tag.write("Path/DieID", stateRessp[12]) 
			if stateRessp[14] == 'CALIBRATE':
				system.tag.write('Path/instruction','Check Calibration of the machine')         #
			system.tag.write("Path/maxInkLevel", stateRessp[18])          #
			system.tag.write("Path/po_sendarea", stateRessp[19])          #
			#system.tag.write("Path/Current_color", stateRessp[20])          #
			#system.tag.write("Path/fiber_color", stateRessp[22])          #
			system.tag.write("Path/current_operid", stateRessp[23])          #
			system.tag.write("Path/po_type", stateRessp[25])          #
			system.tag.write("Path/TU/tu_type", stateRessp[27])          #
			system.tag.write("Path/po_len_set", stateRessp[33])          #
			#system.tag.write("Path/colormode_pts", stateRessp[37])          #
			#system.tag.write("Path/TU/tu_ten_pts", stateRessp[39])          #takeup tension set point
			#system.tag.write("Path/TU/tu_pit_pts", stateRessp[41])          #takeup pit set point
			system.tag.write("Path/payTen_pts", stateRessp[43])          #Pay tension setpoint
			#system.tag.write("Path/preDie_pts", stateRessp[45])          #Pre die set point pts
			system.tag.write("Path/inEdge", stateRessp[47])          #in length set
			system.tag.write("Path/maxLineSpeed", stateRessp[49])          #max line speed
			system.tag.write("Path/ordermode", stateRessp[51])          #
			#system.tag.write("Path/inkType", stateRessp[52]) #NA for 601          #gInkType
			#system.tag.write("Path/airLen", stateRessp[54])  #NA for 601         #gAirLength
			#system.tag.write("Path/airDense", stateRessp[56])  #NA for 601         #gAirDense
			#system.tag.write("Path/twistVal", stateRessp[58])          #twist value
			#system.tag.write("Path/setTwist", stateRessp[60])          #gSetTwist
			system.tag.write("Path/edgeBegin", stateRessp[62])          #
			system.tag.write("Path/edgeEnd", stateRessp[64])          #gEndEdge
			system.tag.write("Path/meGranted", stateRessp[65])          #MUTLIPLE end granted?
			system.tag.write("Path/task_asgn", stateRessp[67])          #task assigned
			system.tag.write("Path/nextDrawID", stateRessp[68])          #
			#system.tag.write("Path/dualspool", stateRessp[70])          #
			system.tag.write('Path/bTrue4',0)
			
		else:
			system.tag.write('Path/instruction',loginResponseSp[5])
			
			if loginResponseSp.count(':') > 5:
			
				shared.main.log(loginResponseSp[loginResponseSp.count(':')+1])
			
	except: 
		shared.main.log ('Operator Login Error'+traceback.format_exc())

	
	    #
#	mach_no = stateRessp[0]        # 
#	oper_id = stateRessp[1]        # 
#	RWD = stateRessp[2]        # 
#	AUX = stateRessp[3]        # 
#	state = stateRessp[4]        # 
#	valid  = stateRessp[5]        # 
#	oper_name = stateRessp[6]        # 
#	po_fiberID = stateRessp[7]        # 
#	po_serID = stateRessp[8]        # 
#	tu_fiberID = stateRessp[9]        # 
#	tu_serID = stateRessp[10]        # 
#	PayoutLenSofar = stateRessp[11]        # 
#	DieID = stateRessp[12]        # 
#	RefStatus = stateRessp[13]        #Reference Status  
#	CalStatus = stateRessp[14]        #Calibration Status 
#	OpMode = stateRessp[15]        #ONLINE or OFFLINE 
#	DataCollection = stateRessp[16]        #ON or OFF 
#	inkLevel = stateRessp[17]        #meters of fiber that can be colored 
#	maxInkLevel = stateRessp[18]        # 
#	po_sendarea = stateRessp[19]        # 
#	Current_color = stateRessp[20]        # 
#	FIBCOLOR = stateRessp[21]        #key 
#	fiber_color = stateRessp[22]        #value 
#	current_operid = stateRessp[23]        #value  
#	PAYSPL = stateRessp[24]        #key 
#	po_type = stateRessp[25]        #value 
#	TAKSP = stateRessp[26]        #key 
#	tu_type = stateRessp[27]        #value 
#	TAKLEN = stateRessp[28]        #key 
#	tuLenSet_pts = stateRessp[29]        #Takeup Length set by pts 
#	CUTLEN = stateRessp[30]        #key 
#	CutLenSet_pts = stateRessp[31]        #Cut Length set pts 
#	PAYLEN = stateRessp[32]        #key 
#	payLenSet = stateRessp[33]        #value 
#	PROOFTEST = stateRessp[34]        #pROOFtESTsET POINT_PTS KEY …. > 35 "PROOFTEST" ELSE "REWIND" 
#	Pfsetpoint_pts = stateRessp[35]        # 
#	CLMODE  = stateRessp[36]        #key color mode
#	colormode_pts = stateRessp[37]        #value 
#	TAKTEN = stateRessp[38]        #key 
#	tu_ten_pts = stateRessp[39]        #value takeup tension set point
#	TAKEPIT = stateRessp[40]        #KEY 
#	tu_pit_pts = stateRessp[41]        #VALUE takeup pit set point
#	PAYTEN = stateRessp[42]        #KEY 
#	payTen_pts = stateRessp[43]        #VALUE Pay tension setpoint
#	DIETEN = stateRessp[44]        #KEY 
#	preDie_pts = stateRessp[45]        #VALUE Pre die set point pts
#	ISELEN = stateRessp[46]        #KEY 
#	inLenSet = stateRessp[47]        #value in length set
#	MAXSPEED = stateRessp[48]        #KEY 
#	maxLineSpeed = stateRessp[49]        #value max line speed
#	ORDER = stateRessp[50]        #KEY order mode
#	ordermode = stateRessp[51]        #value 
#	inkType = stateRessp[52]        #value gInkType
#	AIRLNTH = stateRessp[53]        #KEY 
#	airLen = stateRessp[54]        #value gAirLength
#	AIRDNSE = stateRessp[55]        #key 
#	airDense = stateRessp[56]        #value gAirDense
#	TWIST_V = stateRessp[57]        #key 
#	twistVal = stateRessp[58]        #value twist value
#	TWIST = stateRessp[59]        #key 
#	setTwist = stateRessp[60]        #value gSetTwist
#	SEDGBGN = stateRessp[61]        #KEY gBeginEdge
#	edgeBegin = stateRessp[62]        #VALUE 
#	SEDGEND = stateRessp[63]        #KEY 
#	edgeEnd = stateRessp[64]        #VALUE gEndEdge
#	meGranted = stateRessp[65]        #VALUE MUTLIPLE end granted?
#	TASKASGN = stateRessp[66]        #KEY 
#	task_asgn = stateRessp[67]        #value task assigned
#	nextDrawID = stateRessp[68]        #vlaue 
#	null = stateRessp[69]        # 
#	#dualspool = stateRessp[70]#VALUE
#

	
		
	

	
	
	
	
	
		
	
	