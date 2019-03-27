#initialize and reset
import time
import traceback
tu_serID = str(system.tag.read('Path/TU/tu_serID').value)
def init_reset():
	system.tag.write('Path/instruction',"")
	system.tag.write('Path/spoolRun',"Single")
	
	
	
#same function for abort and run out. 
#6.22.18 PPC
#only the directive is different between these two. abort vs. run_out

def func(select):
	#response = system.net.httpGet('http://nordevapp01.corp.int/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=abort;mach_no=601;oper_id=ITS;layout_id=JHE;layout_passwd=JHE123;reason=MT;')
	#system.net.httpGet('http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/rewind_aux/rewind_aux.svc/process?inString=directive=abort;mach_no=601;oper_id=167;layout_id=JIH;reason=MT;layout_passwd=JIHAB3')
	import time
	reason = ''
	

	try:
		svc='rewind_aux/rewind_aux.svc/process?inString='
	
		if select == 'abort':
			directive = 'abort'
		else:
			directive = 'run_out'
		print directive
		
		data = 'directive=' + directive
		data+= ';mach_no=' + str(system.tag.read('Path/mach_no').value)
		data+= ';oper_id='+ str(system.tag.read('Path/layout_id').value).upper()
		#JIH I need to preserve the oper id with a new tag
		#data+= ';oper_id='+ 'JIH'
		data+= ';layout_id='+ str(system.tag.read('Path/layout_id').value).upper()
		data+=';layout_passwd=' + str(system.tag.read('Path/layout_pw').value).upper()
		#data+= ';layout_id='+ 'JIH'
		#data+=';layout_passwd=' + 'TASHA7'
		#abort reason parse
		abort_reason = (str(system.tag.read('Path/abort_reason').value))
		

		if abort_reason == '0': 
			reason = 'MT'
		elif abort_reason == '1':
			reason = 'ME'
		elif abort_reason == '2':
			reason = 'BQ'
		elif abort_reason == '3':
			reason = 'BR'
		elif abort_reason == '4':
			reason = 'BS'
		elif abort_reason == '5':
			reason = 'CC'
		elif abort_reason == '6':
			reason = 'LE'
		elif abort_reason == '7':
			reason = 'WP'
		print reason + 'reason'		

		data+=';reason='+ reason
	#	
		
		
		sendstring = (shared.main.PTS_URL+svc+data)
		print sendstring
		shared.main.log('SEND: ' + sendstring)
		response = system.net.httpGet(sendstring)
		print response
		shared.main.log('GOT: ' + response)
		
		
		responsesp = response.split(':')
		response_size = response.count(':')
		print response_size
		
		system.tag.write('Path/bTrue',0) #BOOLS ASSOCIATED WITH THE VISIBILITY OF EACH OF THE ABORT DIALOG BOX. 
		system.tag.write('Path/bTrue2',0)
#		system.tag.write('Path/po_removeID',1)
		#system.tag.write('Path/po_fiberID', '')
		#system.tag.write('Path/po_serID', '')
#		system.tag.write('Path/TU/nextID', '')
#		system.tag.write('Path/TU/CutLenSet_pts', '')
#		system.tag.write('Path/TU/tu_plan_area', '')
#		system.tag.write('Path/po_len_set', '')
#		system.tag.write('Path/po_serID_hidden', '')
#		time.sleep(1)
#		system.tag.write('Path/po_removeID',0)
		
		#if there is not a 0 code. 0 = good, 4 = error
		if responsesp[5] != '0' and response_size > 5:
			
			if responsesp[6] == 'Invalid password or layout id. ' or 'Failed to get layout id.': #'Invalid password or layout id. ':
				system.gui.messageBox(responsesp[6])
				system.tag.write('Path/instruction',responsesp[6])
				system.tag.write('Path/layout_reject', 0)
				
			system.tag.write('Path/instruction',responsesp[6] + responsesp[7])
	
		
		else:
				
				system.tag.write('Path/po_removeID',1)
				system.tag.write('Path/TU/nextID', '')
				system.tag.write('Path/TU/CutLenSet_pts', '')
				system.tag.write('Path/TU/tu_plan_area', '')
				system.tag.write('Path/po_len_set', '')
				system.tag.write('Path/po_serID_hidden', '')
				system.tag.write('Path/TU/tu_plan_area','')
				time.sleep(1)
				system.tag.write('Path/po_removeID',0)
				system.gui.messageBox(responsesp[6])

	except:
		shared.main.log(traceback.format_exc())
		
#SCRIPT IS RAN WHEN THE OK BUTTON IS PRESSED AFTER LOGGING IN THE ABORT TU SPOOL

		
def tu_abort():

	layout_id = str(system.tag.read('Path/layout_id').value).upper()
	layout_passwd = str(system.tag.read('Path/layout_pw').value).upper()
	
	if layout_id == 'ADMIN' and layout_passwd == 'OFS12345':
		system.tag.write('Path/TU/previous_completed',1)
		system.tag.write('Path/instruction','TU spool aborted')
		shared.main.log('TU spool is aborted or scrapped')
		
	else:
		system.gui.messageBox('invalid username or password')
	system.tag.write('Path/bTrue3',0)
	
	