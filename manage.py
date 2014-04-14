import os
i=41
while i!=476:
	print "Scraping bug "+str(i)+" of 476"
	os.system("python run.py "+str(i))
	i+=1