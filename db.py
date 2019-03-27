
import math 
from time import gmtime, strftime
import time



#lst = array
def stdDev(lst):
    #Calculates the standard deviation for a list of numbers.
    try:
        num_items = len(lst)
        print num_items
#        print sum(lst)
        mean = (sum(lst) / num_items)
        differences = [x - mean for x in lst]
        sq_differences = [d ** 2 for d in differences]
        ssd = sum(sq_differences)
        
        variance = ssd / num_items
        sd = math.sqrt(variance)
    except:
        sd=0
        if num_items == 0:
            print 'Standard deviation exception - Empty array'
    
    #sd = 0
    return round(sd,2)
 
def mean(lst):
    try:
        num_items = len(lst)
        mean = (sum(lst) / num_items)   
        return round(mean,2)
    except:
        mean=0
        return round(mean,2)
        
def avg(lst):
    try:
        num_items = len(lst)
        mean = (sum(lst) / num_items)   
        return mean
    except:
        mean=0
        return mean
     
# tu tension and pf tension sampling data 
#INCLUDED DANCER POS SAMPLING PPC 7/19/18
def pf_sample():#PF sample samples all data from the start 
    system.tag.write('Path/sum', 0)
    pf_ten_array=[]
    tu_ten_array=[]
    spedge_array = []
    dancerPos_array = [] #dancer Pos TU
    speed_array = []
    
    #added 12/4/18 PPC 
    #mach_start signal isn't sent to PTS until the taping is done. OR if its pressed manually. 
    #manual presssing of start is differentiated by the length of the fiber. if the length is NOT 0 or at least greater than one and then the system receieves a start signal, only then send it to PTS. 
    #this is temp fix until we can differentiate auto start from manual HMI start. 
    #
    #
    
    if (system.tag.read('Path/TU/tapingDone').value == True and system.tag.read('Path/mach_running').value ==True) or ((system.tag.read('Path/mach_start').value ==True) and (system.tag.read('Path/mach_running').value==True)):
        shared.mach_start_stop.mach_start() #send to PTS the start string
        tapingDone = 'True'
        system.tag.write('Path/mach_start_after_taping',1) #this value is set to 0 at CompleteTU event.
        
    
    #test_mach_running
    #while (system.tag.read('Path/test_mach_running').value == 1) and not (system.tag.read('Path/test_mach_stopped').value==1):
    
    #if shared.pf_sample.tapingDone == True: #to eliminate pf_Tension outliers before taping. added 2.5.19 PPC
    time.sleep(2)
            #added a delay to avoid pf_Tension outliers 
    while  (system.tag.read('Path/mach_running').value == 1) and not (system.tag.read('Path/mach_stopped').value==1):
        if system.tag.read('Path/manual_mode').value == 1:
            tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID_manual', 'Path/TU/tu_fiberID']
        else:
            tagPaths = ['Path/po_fiberID','Path/po_serID', 'Path/TU/tu_serID', 'Path/TU/tu_fiberID']
            
        list = system.tag.readAll(tagPaths)
        pf_ten = ((system.tag.read('Path/pf_ten_meas').value))
        tu_ten = ((system.tag.read('Path/TU/tu_ten_meas').value))
        speed = ((system.tag.read('Path/mach_speed').value))
        
        timestamp = (strftime("%Y-%m-%d %H:%M:%S"))
        pf_ten_array.append(pf_ten)
        tu_ten_array.append(tu_ten)
        speed_array.append(speed)
        print speed
        
        #insert into the database = ten_log ---> changed table name to tension_log 12/3/18 PPC
        system.db.runPrepUpdate("INSERT INTO tension_log (po_serialID, po_fiberID, tu_serialID, tu_rwrID, PF_TEN,TU_TEN, mach_speeds, timestamp ) VALUES (?,?,?,?,?,?,?,?)",[list[0].value,list[1].value,list[2].value,list[3].value, pf_ten, tu_ten, speed, timestamp],'mysql') 
        
        time.sleep(3)
        
        #next_value = system.tag.read('fDancerPosMe').value
        
#        if current_value == next_value:
#            count = count+1
#        else:    print 'no count'
#        print count
#        
        #next_value = system.tag.read('fDancerPosMe').value
        
#        if current_value == next_value:
#            count = count+1
#        else:    print 'no count'
#        print count
#        
#    
    s = shared.db
        
    pf_stdDev = s.stdDev(pf_ten_array)
    pf_avg = s.mean(pf_ten_array)
    
    tu_stdDev =s.stdDev(tu_ten_array)
    tu_avg = s.mean(tu_ten_array)
    speed_avg = s.avg(speed_array)

    
    try:
        x=round((min(pf_ten_array)),1)
        y=round((min(tu_ten_array)),1)
        
        a= round((max(pf_ten_array)),1)
        b=round((max(tu_ten_array)),1)
    except:
        x=0
        y=0
        a=0
        b=0
    pf_info_temp = str(x) + ':'+ str(a)+ ':' + str(pf_stdDev) + ':' + str(pf_avg )
    tu_info_temp = str(y) + ':'+ str(b) + ':' + str(tu_stdDev) +':' + str(tu_avg ) 
    system.tag.write('Path/pf_ten_info', str(pf_info_temp))
    system.tag.write('Path/TU/tu_ten_info', str(tu_info_temp))
    system.tag.write('Path/speed_info', speed_avg )
    print pf_info_temp

#4.11455059052:23.8034981092:4.77952943925:25.2021751404