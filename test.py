begin_array = []
end_array = []
ref = ""
	
def Calc_tupkg(ref):	

	count = 0
	#inTolerance parameters 
	t = shared.main.inTolerance
	num = 90 #90 degrees
	toleranceVal = 15 #15 degrees tolerance
	mode = 0 #mode = 0 if the tolerance Value is NOT  a percentage
	const = 1.8 #conversion contanst from percentage to degree 
	
	dancerList = ['Path/TU/fDancerBeginMaxPos','Path/TU/fDancerBeginMinPos', 'Path/TU/fDancerEndMaxPos','Path/TU/fDancerEndMinPos']
	
	dancerPos = system.tag.readAll(dancerList)
	#convert the percentage to degrees to match BAM tolerance level for the TU dancer position 
	#BAM range goes from 0 to 180 degrees with 90 being the middle. 15% tolerance 
	
	
	
	
		
#FOR STAE COUNT  CHECK IF THE DANCER POSITIONS FALL WITHIN THE TOLERANCE VALUE. This is ocmpared against the BAM controllers - changed to degrees
	if not t(num,toleranceVal,(dancerPos[0].value * const),mode): # Path/TU/fDancerBeginMaxPos
		count = count +1
	if not t(num,toleranceVal,(dancerPos[1].value * const),mode): #Path/TU/fDancerBeginMinPos
		count = count +1
	if not t(num,toleranceVal,(dancerPos[2].value * const),mode): #Path/TU/fDancerEndMaxPos
		count = count +1
	if not t(num,toleranceVal,(dancerPos[3].value * const),mode):#Path/TU/fDancerEndMinPos
		count = count +1
		
	if count > 0 : #two intolerances count as 1 
		count = count-1 
	print count
	
	#PPC 07.24.18
	#SUBTRACT 90  degrees TO SEND TO PTS 
	d0 = dancerPos[0].value * const
	d1= dancerPos[1].value * const
	d2 = dancerPos[2].value * const
	d3= dancerPos[3].value * const
	
	


	#REF = what is to be calculated. 
	#this function is called at value change at each of the following paths

#	path1 = system.tag.read('Path/TU/fDancerBeginMaxPos').value
#	path2 = system.tag.read('Path/TU/fDancerBeginMinPos').value 
#	path3 = system.tag.read('Path/TU/fDancerEndMaxPos').value
#	path4 = system.tag.read('Path/TU/fDancerEndMinPos').value
	
	
#CHECK WHAT PARAMETERS ARE PASSED IN. 
	if ref == 'beginMax':
		begin_array.append(d0)
		#INSERT DB INSERT LOGIC HERE*********
			
	elif ref == 'beginMin':
		begin_array.append(d1)
		
	elif ref == 'endMax':
		end_array.append(d2)
	
	elif ref == 'endMin':
		end_array.append(d3)
	print 'begin stdDev'		
	begin_stdDev = shared.db.stdDev(begin_array)
	print begin_stdDev
	print 'begin avg'
	begin_avg = shared.db.mean(begin_array)
	end_stdDev = shared.db.stdDev(end_array)
	end_avg = shared.db.mean(end_array)
		

	
	print begin_array
	print end_array
	print begin_avg
	#ASSEMBLE TU_PKG AND WRITE TO PATH/TU/TU_DATA
	tu_pkg =  str(90-abs(begin_avg))+':'
	tu_pkg += str(90-abs(begin_stdDev))+':'
	tu_pkg += str(90-d0)+':'
	tu_pkg += str(90-d1)+':'
	tu_pkg += str(90-end_avg)+':'
	tu_pkg += str(90-end_stdDev)+':'
	tu_pkg += str(90-d2)+':'
	tu_pkg += str(90-d3)+':'
	tu_pkg += str(system.tag.read('Path/Spedge/begin_error_outer').value)+':'
	tu_pkg +=str(system.tag.read('Path/Spedge/end_error_inner').value)+':'
	tu_pkg += str(count)
	
	
	 
	system.tag.write('Path/test_string',(tu_pkg))
	system.tag.write('Path/TU/tupkg_data',(tu_pkg))
	
	return tu_pkg
