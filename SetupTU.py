#change log 


#1.22.18 error handling for cannot use regular id, enter rwrscrap

####################################################################################################
#Setup TU 
#this is followed after oper_logon, state
import system
import traceback
import time 
import math 
from time import strftime
import threading 

#example:
#[2018.05.16 20:31:50] ! VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/setupTU/setupTU.svc/process?inString=mach_no=770:oper_id=328:rwr_id=GET_SPOOL_ID:rwr_serial_id=5220070639:sfo_final_color=NONE:;spoolRun=Single
#[2018.05.16 20:31:51] ! VBC INET got: 770:328:SETUP:TU:RWR865623657:0:PAYSPL:38:TAkSPL:52:TAKLEN:0:CUTLEN:50800:PAYLEN:306902:PROOFTEST:100:CLMODE:NONE:COLOR:OR:TAKTEN:45:TAKPIT:0.5:PAYTEN:70:DIETEN:70:ISELEN:10:MAXSPEED:1500:PLANSEND:SALE:NO:INKTYPE:NONE:TWIST_V:0:TWIST:N:AIRLNTH:0:AIRDNSE:0:SEDGBGN:30.54:SEDGEND:175.56:no:BTLIMIT:15::
#
def timerDone():
	#system.tag.write('Path/timerDone',1)
	system.tag.write('Path/TEST/bool_test',True)
	print 'timer done'
	
	


system.tag.write("Path/TU/tu_danc_bar", 0.22)
Setupsvc = 'setupTU/setupTU.svc/process?inString='#SETUP Svc 

#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/TU/tu_setup 
def SetupTU():
	#CHECK TO SEE IF THE PREVIOUS TU SPOOL IS COMPLETED 
 	previous_complete = system.tag.read('Path/TU/previous_completed').value
 	if previous_complete == 1:
 		system.tag.write('Path/instruction','Ready for a new TU spool')
 		system.tag.write('Path/TU/previous_completed',0)
	
 #reset ALL at new spool 
		shared.TUpkg.Reset()

		
	
	###ASSEMBLE AND SEND
		system.tag.write('Path/CladdingDiameter',0.125)
		mach_no = system.tag.read("Path/mach_no")
		oper_id = system.tag.read("Path/oper_id")
		manual_mode = system.tag.read('Path/manual_mode')
		
		if manual_mode.value == 1:
			tu_serID = system.tag.read('Path/TU/tu_serID_manual').value
			system.tag.write('Path/bTrue5', 0)
		else:
			tu_serID = system.tag.read('Path/TU/tu_serID').value	
			
		system.tag.write('Path/TU/tu_serID',tu_serID) 
		
		
		
		postdata = 'mach_no=' + str(mach_no.value)
		postdata += ':oper_id=' + str(oper_id.value).upper() 
		if system.tag.read('Path/TU/tu_plan_area').value=='SCRP':#or system.tag.read('Path/TU/tu_send_area').value == 'SCRP':
			rwr_id = 'RWRSCRAP'
			system.tag.write('Path/TU/tu_fiberID','RWRSCRAP')
			#system.tag.write('Path/TU/nextID','')#reset next TU ID
			
		#elif system.tag.read('Path/nextDrawID').value == 'SCRP':
			#rwr_id='RWRSCRAP' 
			#system.tag.write('Path/nextDrawID',"")
		else:
			rwr_id = 'GET_SPOOL_ID'
			
		postdata+= ':rwr_id='+ str(rwr_id)
		postdata+= ':rwr_serial_id=' + str(tu_serID)
		postdata+= ':sfo_final_color=' + 'NONE'
		postdata+= ':;spoolRun=' + 'Single'
		###############################################################
		#SEND TO PTS
		try:
			sendstring1= shared._1_Oper_Logon.SendURL(shared.main.PTS_URL, Setupsvc, postdata)
			print sendstring1
			shared.main.log(sendstring1)
			#RESET TU_PLAN_AREA from previous completeTU instruction. Example: if instruction from previous completeTU is "RWRSCRP", reset it as soon as takeup
						
		except:
			shared.main.log(traceback.print_exc('sendstring1'))
			
			shared.main.log ('SETUP TU Error'+traceback.format_exc())
	
		
		### PARSE RESPONSE
		#######################################################################
		#RESPONSE FROM PTS
		try:
			time.sleep(1)
			response1 = system.net.httpGet(sendstring1)
			print response1
			shared.main.log(response1)
			response1sp = response1.split(':')
		
			#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
			
			if response1sp[5]=='0': #response is GOOD 	
				
	#		for i in range(0,response1.count(':')+1):
	#			print ('%d = ')%i + response1sp[i]
				system.tag.write('Path/instruction',response1sp[6])
				#system.tag.write("Path/oper_id", response1sp[1])          #
				phase = response1sp[2] + response1sp[3]
				system.tag.write('Path/TU/tu_fiberID',response1sp[4])
				system.tag.write("Path/setupValid", response1sp[5])      
				system.tag.write("Path/po_type", response1sp[7])          #
				system.tag.write("Path/TU/tu_type", response1sp[9])          #
				system.tag.write('Path/TU/tuLenSet_pts', float(response1sp[11]))
				system.tag.write('Path/TU/CutLenSet_pts', float(response1sp[13]))
				system.tag.write("Path/po_len_set", float(response1sp[15]))
				
				#MADE THE PT POINT TO 105 TO ENSURE IT STAYS ABOVE 100. PPC 8/1/18, set to 30 for scrap
						
				if response1sp[17] =='0':
					pfsetpoint = 30 		
				else:
					pfsetpoint = float(response1sp[17])+5
					
			
				system.tag.write('Path/Pfsetpoint_pts',pfsetpoint)         #
				   
				system.tag.write("Path/fiber_color", response1sp[21])         #
				system.tag.write("Path/TU/tu_ten_pts", response1sp[23])          #takeup tension set point
				system.tag.write("Path/TU/tu_pit_pts", 0.55)#response1sp[25])          #takeup pit set point
				system.tag.write("Path/TU/tu_danc_bar", 0.22)
				system.tag.write("Path/payTen_pts", response1sp[27])          #Pay tension setpoint
				system.tag.write("Path/preDie_pts", response1sp[29])          #Pre die set point pts
				system.tag.write("Path/inEdge", response1sp[31])          #in length set
				system.tag.write("Path/maxLineSpeed", response1sp[33])  #mach line speed
				#system.tag.write("Path/maxLineSpeed", 2000)  #mach line speed
				system.tag.write('Path/plan_send', response1sp[35]) #plan send or type use
				system.tag.write('Path/circle', response1sp[36])  #added new tag  
				#system.tag.write("Path/inkType", response1sp[38]) #N/A         #gInkType
#				system.tag.write("Path/twistVal", response1sp[40])          #twist value #KEY=TWIST_V
#				system.tag.write("Path/setTwist", response1sp[42])   #TWIST #gSetTwist
	#			system.tag.write("Path/airLen", response1sp[44])#N/A          #gAirLength KEY =  AIRLNTH
	#			system.tag.write("Path/airDense", response1sp[46]) #N/A         #gAirDense #  KEY =  AIRDNSE
				system.tag.write("Path/edgeBegin", response1sp[48])          #
				system.tag.write("Path/edgeEnd", response1sp[50])         #gEndEdge
				system.tag.write("Path/meGranted", response1sp[51])
				          #MUTLIPLE end granted?
				system.tag.write("Path/instruction", 'TAKEUP SPOOL VALID')  
				shared.main.log('TAKEUP SPOOL VALID')   

				system.tag.write('Path/inEdge',10.0)
				system.tag.write('Path/TU/tu_spool_accept','true')
				time.sleep(1)
				system.tag.write('Path/TU/tu_spool_accept','false')
				system.tag.write('Path/TU/nextID','')#reset next TU ID, moved to after spool accepted 20180813
				system.tag.write('Path/nextDrawID',"")
				system.tag.write('Path/TU/tu_serID_PTS',tu_serID)
				system.tag.write('Path/TU/prevent_newtu','true')


				#RESET  tu spool_send area-only clear if the response back is 0
				#system.tag.write('Path/TU/tu_send_area',"")
				#system.tag.write('Path/TU/tu_plan_area',"")
				#RESET PREVIOUS SPOOL data
				tags= ["Path/TU/tu_ten_info","Path/pf_ten_info",'Path/stop_code','Path/spedge/spedge_val','Path/TU/tupkg_data','Path/Spedge/spedge_val']
				values=['0','0','none','0','0',0]
				system.tag.writeAll(tags,values)
				
								     #task assigned
				#start timer here, if tu spool is valid and doesn't run after a set amount of time, notify the operator/coach/engrs
#				timeinSec = 400
#				timer = threading.Timer(timeinSec, shared.main.Send_Email('mach_stalled'))
#				timer.start()
#				for i in range(1,timeinSec):
#					i=i+1
#					time.sleep(1)
#					system.tag.write('Path/TEST/test_int',i)#to chck if timer is working
#					
#				
				
				#check to see if dancer is open and then complete the spool
	
			
			else:
			#if plan_send instruction from PO setup gets cleared out, and rwrscrap instruction is to be made, 
			#set the next spool for rwrscrap
				if response1sp[6] == 'Cannot use regular RWR id. Enter RWRSCRAP. ':
					system.tag.write('Path/TU/tu_plan_area','SCRP')
					#system.tag.write('Path/TU/tu_fiberID','RWRSCRAP')
				
				elif (response1sp[6] == 'Cannot use RWRSCRAP. Enter a regular RWR id.'):
					system.tag.write('Path/TU/tu_plan_area','')
				 
				
				system.tag.write('Path/instruction', 'Takeup Spool Rejected. '  + response1sp[6]) 
				shared.main.log('Takeup Spool is Rejected. ' + response1sp[6])

				#error handling for cannot use regular id, enter rwrscrap #ppc 1.22.19



				system.tag.write('Path/TU/tu_spool_reject','true')
				system.tag.write('Path/TU/previous_completed','true')#READY TO ACCEPT A NEW SPOOL SIGNAL 
				time.sleep(1)
				system.tag.write('Path/TU/tu_spool_reject','false')
				shared.main.log(response1sp[6])

				
				
		except:
			shared.main.log(traceback.format_exc())
			
			#"601:JAM:COMP:TU:JRFSF6614A1CLJ:0:RACK:PAYOUT:10:SCRP:0:::NONE:"
		
	
	else:
		system.tag.write('Path/instruction','Previous spool has to be completed to continue')
		shared.main.log('Previous spool has to be completed to continue')	



#Case "TSendTUPackageData"
#		            OutBuff$ = GetTUPackageData$()
#		            ServerProgram$ = "pd_rema"
#		            SendString$ = gMachineNumber$ + ":" + gOperatorID$ + ":RE:MA:TUPKG:" + gTakeupID$ + ":" + gTakeupSerID$ + ":" + gMachStop$ + ":" + gLengthRun$ + ":" + OutBuff$ + ":"
#		            sendstring2$ = "directive=tupkg"
#		            sendstring2$ = sendstring2$ + ";mach_no=" + gMachineNumber$
#		            sendstring2$ = sendstring2$ + ";oper_id=" + gOperatorID$
#		            sendstring2$ = sendstring2$ + ";rwr_id=" + gTakeupID$
#		            sendstring2$ = sendstring2$ + ";rwr_serial_id=" + gTakeupSerID$
#		            sendstring2$ = sendstring2$ + ";mach_stop=" + gMachStop$
#		            sendstring2$ = sendstring2$ + ";length_run=" + gLengthRun$
#		            sendstring2$ = sendstring2$ + ";tupkg_data=" + OutBuff$

#	       '''gPoSol$ = TokenArray(TOKENSTART% + 1)             'Payout spool type
#            gTuSpool$ = TokenArray(TOKENSTART% + 3)             'Takeup spool type
#            gTuLenSet$ = TokenArray(TOKENSTART% + 5)            'Length on takeup spool
#            If Val(gTuLenSet$) > 0 Then
#                gWindMode$ = "SPLICE"
#            End If
#            gCutLenSet$ = TokenArray(TOKENSTART% + 7)           'Cut length
#            gPayLenSet$ = TokenArray(TOKENSTART% + 9)           'Payout spool length
#            gPayLen& = Val(gPayLenSet$)
#            gPrfTenSetpoint$ = TokenArray(TOKENSTART% + 11)     'Prooftest setpoint
#'            If Val(gPrfTenSetpoint$) > 35 And gTakeupID$ <> "RWRSCRAP" Then
#            If Val(gPrfTenSetpoint$) > 35 Then
#                gWindMode$ = "PROOFTEST"
#            Else
#                gWindMode$ = "REWIND"
#                gPrfTenSetpoint$ = "25"     'Set minimum to 25 kpsi per Trey Ryan 03/17/2005
#            End If
#            gColorMode$ = TokenArray(TOKENSTART% + 13)      'Color mode
#            If gColorMode = "RECU" Then
#                gColorMode = "RECURE"
#            End If
#            gFiberColor$ = TokenArray(TOKENSTART% + 15)     'Color of fiber after rewind/coloring
#            If gTakeupID = "RWRSCRAP" Then
#                gColorMode = "NONE"
#            End If
#            gTakeTenSetpoint$ = TokenArray(TOKENSTART% + 17)    'Takeup tension setpoint
#            gTakePitSetpoint$ = TokenArray(TOKENSTART% + 19)    'Takeup pitch
#            gPayTenSetpoint$ = TokenArray(TOKENSTART% + 21)     'Payout tension
#            gPreDieSetpoint$ = TokenArray(TOKENSTART% + 23)     'Pre-die tension
#            gInLenSet$ = TokenArray(TOKENSTART% + 25)           'Inside end length
#            gMaxLineSpeed$ = TokenArray(TOKENSTART% + 27)       'Fast line speed
#            gTypeUse$ = TokenArray(TOKENSTART% + 29)            'Plan Send or current takeup spool
#            gCircle$ = TokenArray(TOKENSTART% + 30)
#            gInkType$ = TokenArray(TOKENSTART% + 32)            'Ink type for DSM or Hexion
#            gTwistValue$ = TokenArray(TOKENSTART% + 34)         'Twist value
#            gSetTwist$ = TokenArray(TOKENSTART% + 36)           'Flag for setting twist value
#            gAirLength$ = TokenArray(TOKENSTART% + 38)
#            gAirDense$ = TokenArray(TOKENSTART% + 40)
#            gBeginEdge = TokenArray(TOKENSTART% + 42)
#            gEndEdge = TokenArray(TOKENSTART% + 44)
#            gMEGranted$ = TokenArray(TOKENSTART% + 45)
#            gInstruction$ = ""
#            gInstruction$ = TokenArray(TOKENSTART% + 48)
#            '''	
#	
def x():
	timer = threading.Timer(5,shared.SetupTU.timerDone)
	timer.start()
#	
#	
	

	
		
