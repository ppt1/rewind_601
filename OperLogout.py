def OperLogout():
	system.tag.write('Path/test','true')
	time.sleep(4)
	system.tag.write('Path/test','false')