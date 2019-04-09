import time
import traceback
begin_array = []
end_array = []
count = 0.0


#THIS FUNCTION CALCULATES STAE COUNT 
#THIS FUNCTION IS CALLED in  shared.TUpkg.Calc_tupkg(parameter)

def stae(param):
		ref = shared.TUpkg
		t = shared.main.inTolerance
		c = shared.main
		#inTolerance parameters
		num = 90 #90 degrees
		toleranceVal = 15 #15 degrees tolerance
		mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
		const = 1.8 #conversion contanst from percentage to degree 
		
	#	convert_val. NEXTROM prooftesters dancer position is in %. percent is converted to degrees to match BAM controllers. 
		converted_val = round(param* const,2)
#		if param == x:
#			param = system.tag.read('Path/test_float').value
#	
	#FOR STAE COUNT  CHECK IF THE DANCER POSITIONS FALL WITHIN THE TOLERANCE VALUE. This is compared against the BAM controllers - changed to degrees
		if not t(num,toleranceVal,converted_val,mode):
			shared.TUpkg.count +=1
		system.tag.write('Path/TU/stae_count' , shared.TUpkg.count)
		return shared.TUpkg.count
		
#CALLED EVERY TIME THERES A TAG CHANGE IN DANCER BEGIN/END MIN/MAX POSITIONS

def Calc_tupkg(param):	

	#short hand INITIALIZE
	ref = shared.TUpkg
	t = shared.main.inTolerance
	c = shared.main
	#inTolerance parameters
	num = 90 #90 degrees
	toleranceVal = 15 #15 degrees tolerance
	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
	const = 1.8 #conversion contanst from percentage to degree 
	
	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
	
	dancerPos = system.tag.readAll(dancerList)
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	d0 = round(dancerPos[0].value * const,2)
	print d0
	d1 = dancerPos[1].value * const
	d2 = dancerPos[2].value * const
	d3 = dancerPos[3].value * const
	
	#PPC 07.24.18
	#SUBTRACT 50 TO SEND TO PTS 

	#ref = what is to be calculated. 
	#this function is called at value change at each of the following paths

#	d0 = ('Path/TU/fDancerBeginMaxPos').value
#	d1 = ('Path/TU/fDancerBeginMinPos').value 
#	d2 = ('Path/TU/fDancerEndMaxPos').value
#	d3 = ('Path/TU/fDancerEndMinPos').value
	
	
#CHECK WHAT PARAMETERS ARE PASSED IN. 
	if param == 'beginMax':
		ref.begin_array.append(d0)
		
	elif param == 'beginMin':
		ref.begin_array.append(d1)
		
	elif param == 'endMax':
		ref.end_array.append(d2)
	
	elif param == 'endMin':
		ref.end_array.append(d3)
	else:
		ref.end_array.append(system.tag.read('Path/test_float').value)
		print ref.end_array
	print 'begin stdDev'
			
#	begin_stdDev = shared.db.stdDev(ref.begin_array)
#		
#	begin_avg = shared.db.mean(ref.begin_array)
#	begin_avg = num - begin_avg #subtract from 90 to send to PTS
#	
#	end_stdDev = shared.db.stdDev(ref.end_array)
#
#	
#	end_avg = shared.db.mean(ref.end_array)
#	end_avg = num - end_avg
	
	#subract everything by 90
	d0 = num - d0
	d1 = num - d1	
	d2 = num - d2	
	d3 = num - d3	


	system.tag.write('Path/TU/begin_array', ref.begin_array)
	system.tag.write('Path/TU/end_array',  ref.end_array)

	
		
	if system.tag.read('Path/manual_mode').value == 1:
		tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID_manual', 'Path/TU/tu_fiberID']
	else:
		tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID', 'Path/TU/tu_fiberID']
	
	lst = system.tag.readAll(tagPaths)
	
	#COMMENTED OUT ON 11/29/18 PPC - INSERT BACK IN. mySQL is offline
	system.db.runPrepUpdate("INSERT INTO dancerPos (beginMax, beginMin, endMax, endMin, po_fiberID, po_serialID, timestamp, tu_serialID)  VALUES (?,?,?,?,?,?,?,?)",[str(d0), str(d1), str(d2),str(d3),lst[0].value,lst[1].value,c.timestamp, lst[2].value],'mysql') 
		
		
	

	 
def Reset():#THIS FUNCTION IS CALLED AT shared.TUpkg.Send_tupkg()
		
		shared.TUpkg.end_array = []
		shared.TUpkg.begin_array = []
		shared.TUpkg.count = 0
		system.tag.write('Path/TU/stae_count',0)
		system.tag.write('Path/TU/tu_ten_info','')
		system.tag.write('Path/TU/take_len',0)
		system.tag.write('Path/TU/tu_length',0)
			

		system.tag.write('Path/TU/begin_array',[])
		system.tag.write('Path/TU/end_array',[])
		
		system.tag.write('Path/PITCH','')
		
		print shared.TUpkg.begin_array
		
		

def Send_tupkg(): #THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/CompleteTU

	t = shared.main.inTolerance
	c = shared.main
	ref = shared.TUpkg
	#inTolerance parameters
	num = 90 #90 degrees
	toleranceVal = 15 #15 degrees tolerance
	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
	const = 1.8 #conversion contanst from percentage to degree 
	
	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
	
	dancerPos = system.tag.readAll(dancerList)
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	d0 = round(dancerPos[0].value * const,2)
	print d0
	d1 = dancerPos[1].value * const
	d2 = dancerPos[2].value * const
	d3 = dancerPos[3].value * const
	
	
	
	begin_stdDev = shared.db.stdDev(system.tag.read('Path/TU/begin_array').value)
	
	begin_avg = shared.db.mean(system.tag.read('Path/TU/begin_array').value)
	begin_avg = num - begin_avg #subtract from 90 to send to PTS
	
	end_stdDev = shared.db.stdDev(system.tag.read('Path/TU/end_array').value)
	
	
	end_avg = shared.db.mean(system.tag.read('Path/TU/end_array').value)
	end_avg = num - end_avg
	
	#subract everything by 90
	#begin_avg= num - begin_avg
	#end_avg= num - end_avg
	d0 = num - d0
	d1 = num - d1	
	d2 = num - d2	
	d3 = num - d3
	d4 = system.tag.read('Path/Spedge/begin_error_outer').value
	d5 = system.tag.read('Path/Spedge/end_error_inner').value

	print ref.begin_array
	print ref.end_array
	
	
	
	#ASSEMBLE TU_PKG AND WRITE TO PATH/TU/TU_DATA
	tu_pkg =  str(round(begin_avg,2))+':' #fDancerBeginMaxPos
	tu_pkg += str(begin_stdDev)+':' #
	tu_pkg += str(round(d0,2))+':'#fDancerBeginMaxPos
	tu_pkg += str(round(d1,2))+':' #fDancerBeginMinPos
	tu_pkg += str(round(end_avg,2))+':'
	tu_pkg += str(round(end_stdDev,2))+':'
	tu_pkg += str(round(d2,2))+':'#fDancerendMaxPos
	tu_pkg += str(round(d3,2))+':'#fDancerendMinPos
	tu_pkg += str(round(d4,2))+':' #begin error outer
	tu_pkg +=str(round(d5,2))+':' #begin error inner
	
	
	if shared.TUpkg.count > 0: #Last attribute of the string 
		tu_pkg += str(shared.TUpkg.count-1)+'0'
	else:
		tu_pkg += '0.00'
		

	system.tag.write('Path/TU/tupkg_data',(tu_pkg))

	
	print tu_pkg
	#ASSEMBLE DATA AND SEND TO PTS
	try:
		svc= "rewind_aux/rewind_aux.svc/process?inString="	 #TU Svc 
		stop_code = system.tag.read('Path/stop_code') 
		manual_mode = system.tag.read('Path/manual_mode')				
		if manual_mode.value == 1:
			tu_serID = system.tag.read('Path/TU/tu_serID_manual').value
			shared.main.log('Machine is in manual mode')
		else:
			tu_serID = system.tag.read('Path/TU/tu_serID_PTS').value	
			
		postdata= "directive=" + 'tupkg' +';' 	
		postdata+= 'mach_no=' + str(system.tag.read('Path/mach_no').value) 
		postdata+= ';oper_id=' + str(system.tag.read('Path/current_operid').value).upper()			
		postdata+= ';rwr_id=' + str(system.tag.read('Path/TU/tu_fiberID').value)#change to  
		postdata+= ';rwr_serial_id=' + str(tu_serID)		
		postdata+= ';mach_stop=' + str(system.tag.read('Path/stop_code').value)
		postdata+= ';length_run='+str(system.tag.read('Path/TU/tu_length').value)
		postdata+= ';tupkg_data='+tu_pkg
		
		
		time.sleep(1) # delay the PTS messange sending for one minute to avoid server hangup
		sendstring = shared.main.PTS_URL + svc + postdata
		shared.main.log(sendstring)
		#RESPONSE GET
		response = system.net.httpGet(sendstring)
		shared.main.log(response)
		responsesp = response.split(":") #example :770:231:COMP:TU:JRFSF3959D2CLJ:0:RACK:PAYOUT:41:SALE:0:::NONE:
		if responsesp[5] == '0':
			ref.Reset()
			#system.tag.write('Path/instruction','TU spool completed, place it on the RACK')
		else:
			system.tag.write('Path/instruction',responsesp[6])
			
		shared.main.log('TUpkg data = ' + tu_pkg)
		ref.tu_pkg = tu_pkg
		
		
	except:
		shared.main.log('Tupkg exception: ' + traceback.format_exc())
		#RECEIVE
	

	
		 
