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
import traceback
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU
def CompleteTU():
	tu_length = system.tag.read('Path/TU/take_len').value #move the OPC Path/take_length to a local memory tag. Fix the TUpkg not being sent issue. Reset this later. 
	system.tag.write('Path/TU/tu_length',tu_length)
	
	time.sleep(5)
	
	try:
#http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/completeTU/completeTU.svc/process?inString=mach_no=601;oper_id=200;
#po_id=;po_serial_id=;rwr_id=RWR722616469;rwr_serial_id=5220158737;plan_length=26074;actual_len=1380;accum_len=1380;tu_color=BL;tu_status=OK;stop_code=PFBK;mach_speed=0;I_PO_TEN=0.0:0.0:0.0:0.0;I_TU_TEN=0:0:0.0:0.0;I_PF_TEN=0:0:0.0:0.0;SPEDGE=156.15:156.15:0.0:9.92:9.92:0.0:;MISC=21

		svc= 'completeTU/completeTU.svc/process?inString=' #TU Svc 
	
		#postData2= "directive=" + directive2 +';' 
		postdata= 'mach_no=601' 
		postdata+= ';oper_id=' + str(system.tag.read('Path/current_operid').value).upper()
		postdata+= ';po_id=' + str(system.tag.read('Path/po_fiberID').value)
		postdata+= ';po_serial_id=' + str(system.tag.read('Path/po_serID').value) 
			
		postdata+= ';rwr_id=' + str(system.tag.read('Path/TU/tu_fiberID').value)
		
		manual_mode = system.tag.read('Path/manual_mode')
		
		#SPEDGE PARAMETERS ADDED 7/16/18 -  PPC
		
		spedge_tags = ['Path/Spedge/init_begin_outer','Path/Spedge/actual_begin_outer','Path/Spedge/begin_error_outer','Path/Spedge/init_end_inner','Path/Spedge/actual_end_inner','Path/Spedge/end_error_inner']
		lst = (system.tag.readAll(spedge_tags))
		#inner and outer are what is referreced as end and begin (respectively) on the nextrom plc 
		#outer = begin
		#inner = end 
		#str(round(d0,2))
		spedge = str(round(lst[0].value,2)) + ':' #init_begin_outer
		spedge += str(round(lst[1].value,2))+ ':' #actual_begin_outer
		spedge += str(round(lst[2].value,2))+ ':' #begin_error_outer
		spedge += str(round(lst[3].value,2))+ ':' #init_end_inner
		spedge += str(round(lst[4].value,2))+ ':' # actual_end_inner
		spedge += str(round(lst[5].value,2))+ ':' #end_error_inner
		system.tag.write('Path/spedge/spedge_val', spedge)
	
		tu_serID = system.tag.read('Path/TU/tu_serID').value	 
		postdata+= ';rwr_serial_id=' + str(tu_serID) 
		postdata+= ';plan_length=' +str(system.tag.read('Path/TU/CutLenSet_pts').value) 
		postdata+= ';actual_len=' + str(system.tag.read('Path/TU/take_len').value) #+ ';accum_len=43198'#;tu_color=RD;tu_status=OK;stop_code=STCT;mach_speed=1500;spoolRun=Single;I_PO_TEN=59.5:76.1:2.27:70.17;I_TU_TEN=44.2:55.5:1.92:50.18;I_PF_TEN=106.3:114.5:1.48:110.11;SPEDGE=30.54:29.91:-0.52:175.56:176.03:0.21:;DEFECT=0:0;MISC=21'
		postdata+= ';accum_len=' + str(system.tag.read('Path/TU/take_len').value) 
		postdata+= ';tu_color=' + str(system.tag.read('Path/fiber_color').value)
		postdata+= ';tu_status=OK' #+ str(system.tag.read('Path/tu_status').value) 
		
		stop_code = shared.main.Stop_code() 
		
		
		if system.tag.read('Path/TU/take_len').value <30 and (stop_code == 'PFBK'):
			stop_code = 'TUBK'	
			
		system.tag.write('Path/stop_code', stop_code)
		postdata+= ';stop_code=' + str(stop_code)
	
		postdata+= ';mach_speed=' + str(system.tag.read('Path/speed_info').value)#JIH gather avg speed
		postdata+= ';I_PO_TEN=0.0:0.0:0.0:0.0'
		postdata+= ';I_TU_TEN='+ str(system.tag.read('Path/TU/tu_ten_info').value)
		postdata+=';I_PF_TEN='+ str(system.tag.read('Path/pf_ten_info').value)
		postdata+= ';SPEDGE='+ spedge
		#SEND PITCH CHANGE PARAMETER ONLY WHEN THERE IS A PITCH CHANGE 
		if system.tag.read('Path/pitch_change').value == 1:
			postdata+= ';PITCH=' + str(system.tag.read('Path/PITCH').value) 
			
		postdata+= ';MISC=21'

		sendstring1 = shared.main.PTS_URL + svc + postdata #Sendstring2 = directive=state. get the state of the machine. 
		print sendstring1
		shared.main.log(sendstring1)
		
		
		
		response = system.net.httpGet(sendstring1)
		shared.main.log(response)
		responsesp = response.split(":") #example :770:231:COMP:TU:JRFSF3959D2CLJ:0:RACK:PAYOUT:41:SALE:0:::NONE:
		#:770(0):231(1):COMP(2):TU(3):JRFSF3959D2CLJ(4):0(5):RACK(6):PAYOUT(7):41(8):SALE(9):0(10):(11):(12):NONE(13):
		print response
		#IF PITCH CHANGE, TURN OFF THE FLAG. 
		system.tag.write('Path/pitch_change',0)
		
		#check to see if the spool is already completed. 
		#this is to avoid freeze on the sequence/handshaking when a "complete" button is already pressed on nextrom HMI 
		#error2 checks with the error given from PTS  = give nextrom the NEXT tu signal	
		error2 = str(system.tag.read('Path/TU/tu_fiberID').value) + ' has already been used in rew_fiber. :' #added 12/19/2018

		
		
		if responsesp[5] == '0'or response[6] == error2:
			system.tag.write('Path/TU/NextTU','true')
			system.tag.write('Path/TU/Next_TU_LCU','true')
			system.tag.write('Path/TU/prevent_newtu','false')
			#system.tag.write('Path/TUBK','false')
			time.sleep(2)
			system.tag.write('Path/TU/NextTU','false')
			system.tag.write('Path/TU/Next_TU_LCU','false')
			system.tag.write('Path/instruction','Completed Takeup. ' + responsesp[9])#changed from 12 JIH
			system.tag.write("Path/TU/tu_send_area", responsesp[6]) #changed from 8 JIH
			system.tag.write("Path/po_sendarea", responsesp[7])	
			system.tag.write('Path/TU/nextID', responsesp[8])#changed from 9
			system.tag.write('Path/po_next_id', responsesp[13]) #JIH for GetID
			system.tag.write('Path/TU/tu_plan_area', responsesp[9])
			system.tag.write('Path/TU/actual_len',0)
			system.tag.write('Path/TU/tu_fiberID',' ')
			
			if system.tag.read('Path/po_sendarea').value=='COMP':
				#system.tag.write('Path/po_fiberID', '')
				#system.tag.write('Path/po_serID', '')
				system.tag.write('Path/po_removeID',1)
				system.tag.write('Path/TU/nextID', '')
				system.tag.write('Path/TU/CutLenSet_pts', '')
				system.tag.write('Path/po_len_set', '')
				system.tag.write('Path/TU/tu_plan_area', '')
				system.tag.write('Path/po_serID_hidden', '')
				time.sleep(1)
				system.tag.write('Path/po_removeID',0)
		else:
			system.tag.write('Path/TU/NextTU','false')
			system.tag.write('Path/TU/Next_TU_LCU','false')
			system.tag.write('Path/instruction',responsesp[6])
	
		#system.tag.write('Path/instruction', 'Set Takeup area to %s. Set Payout area to %s',responsesp[6],responsesp[7])
		#PAYOUT
		
		res_size = responsesp.count(':')
		#previous spool HAS TO BE  completed TO ACCEPT NEW SPOOL
		system.tag.write('Path/TU/previous_completed',1)
		
		if  res_size > 7:
		
			system.tag.write("Path/ink_level", responsesp[res_size+1]) #41
			system.tag.write("Path/type_use", responsesp[res_size+2]) #SALE
		
			system.tag.write("Path/instruction", responsesp[res_size+4]+ ' ' +responsesp[res_size+5] ) #0
	
			system.tag.write("Path/nextDrawID",  responsesp[res_size+5]) #	
			
	#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
			
	
			print ("Invalid response. Check the message sent")
	except:	
		shared.main.log("CompleteTU error: "+ traceback.format_exc())
	

#		 Case "TUpdateTakeup"
#            gTuSendArea$ = TokenArray(TOKENSTART%)   'Current spool takeup send area
#            gPoSendArea$ = TokenArray(TOKENSTART% + 1)
#            gTuSpool$ = TokenArray(TOKENSTART% + 2)
#            gTypeUse$ = TokenArray(TOKENSTART% + 3)
#            gInkLevel$ = TokenArray(TOKENSTART% + 4)   'Current ink level
#            If (gfViewTrace) Then
#                objUserControl.TXT_debug_SelText = Chr$(CR) + Chr$(LF) + "UP:TU set takeup spool type to" & gTuSpool$
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 4) Then
#                gInstruction$ = TokenArray(TOKENSTART% + 5)
#                If (gInstruction$ <> "") Then Logger LOG_CLIENT, LOG_TRACE, "UP:TU set instruction to " & gInstruction$
#            Else
#                gInstruction$ = ""
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 5) Then
#                gInstruction2$ = TokenArray(TOKENSTART% + 6)
#                If (gInstruction2$ <> "") Then Logger LOG_CLIENT, LOG_TRACE, "UP:TU set instruction2 to " & gInstruction2$
#            Else
#                gInstruction2$ = ""
#            End If
#            If UBound(TokenArray) > (TOKENSTART% + 6) Then
#                gNextDrawID$ = TokenArray(TOKENSTART% + 7)
#            End If
#	PITCH CALCULATIONS 

#WHILE pitch detection is on, calculate the traverse position. 

	
	#TU DANCER TU_PKG vals 
	#TU-PKG PARAMETERS ADDED 7/18/18 PCCCC
	
	
	#while (system.tag.read('Path/test_mach_running').value == 1) and not (system.tag.read('Path/test_mach_stopped').value==1):
#	count = 0
#	#inTolerance parameters 
#	t = shared.main.inTolerance
#	num = 90 #90 degrees
#	toleranceVal = 15 #15 degrees tolerance
#	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
#	const = 1.8 #conversion contanst from percentage to degree 
#	
#	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
#	dancerPos = system.tag.readAll(dancerList)
#	
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	
	
	
	#TU-PKG PARAMETERS ADDED 7/18/18 PPC
