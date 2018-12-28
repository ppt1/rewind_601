import system
import time
import traceback
#THIS FUNCTION IS CALLED AT THE TAG CHANGE EVENT OF Path/po_setup
def SetupPO():

	system.tag.write('Path/po_removeID',0)
#VBC INET send: http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/setupPO/setupPO.svc/process?inString=701:128:JRFVY1714A1RVH:3800117787:DEF_DET:NO:DEF_LVL:0::
#VBC INET got: 701:128:SETUP:PO:JRFVY1714A1RVH:0:TAKEUP:41:SALE:200M:PLN:4741::
#VBC INET got: 701_0:128_1:SETUP_2:PO_3:JRFVY1714A1RVH_4:0_5:TAKEUP_6:41_7:SALE_8:200M_9:PLN_10:4741_11::
	try:
		PTS_URL = 'http://pts.ganor.ofsoptics.com/norcross/pts/rewind/svc/'
		svc = "setupPO/setupPO.svc/process?inString="
		
		manual_mode = system.tag.read('Path/manual_mode')	
		if manual_mode.value == 1:
			shared.main.log('Machine is in manual mode')
			
		x= system.tag.read('Path/mach_no').value
		y= system.tag.read('Path/oper_id').value
		z= system.tag.read('Path/po_fiberID').value
		a= system.tag.read('Path/po_serID').value
		#hide po serial ID from operators on the HMI
		hiddenFigures = a[0] + a[1]+a[2]+a[3]+'xxxx'+a[8]+a[9]
		system.tag.write('Path/po_serID_hidden',hiddenFigures)
		
		
		data = str(x) + ':'
		data += str(y)+':'
		data += str(z)+':'
		data += str(a)+':'
		data += 'DEF_DET:NO:DEF_LVL:0:'+':' #N/A for nextrom machines
		setupPOsend = shared.main.PTS_URL + svc + data
		shared.main.log(setupPOsend)
		print  shared.main.PTS_URL + svc + data
		response1 = system.net.httpGet( shared.main.PTS_URL + svc + data)
		print response1
		time.sleep(1)
		shared.main.log(response1)
		response1sp = response1.split(':')
		
#VBC INET got: 701_0:128_1:SETUP_2:PO_3:JRFVY1714A1RVH_4:0_5:TAKEUP_6:41_7:SALE_8:200M_9:PLN_10:4741_11::	
		if response1sp[5]=='0': #response is GOOD 
			system.tag.write('Path/instruction','Payout Spool accepted . ' + response1sp[12])
			
			system.tag.write('Path/po_type',response1sp[6])
			system.tag.write('Path/po_sendarea',response1sp[7])
			system.tag.write('Path/tu_plan_area',response1sp[8])
			#system.tag.write('Path/get_setup_direction',response1sp[8])
			system.tag.write('Path/PayoutLenSofar',response1sp[11])
			shared.main.log('PO Response valid')
			
			system.tag.write('Path/po_spool_accept','true')
			time.sleep(1)	
			system.tag.write('Path/po_spool_accept','false')
			
		else:
			system.tag.write('Path/instruction','Payout Spool REJECTED. '+response1sp[6]+response1sp[7])
			system.tag.write('Path/po_spool_reject','true')
			time.sleep(1)
			system.tag.write('Path/po_spool_reject','false')
	except:
		shared.main.log ('PO Setup Error: '+traceback.format_exc())
			
