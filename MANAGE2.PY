import os
i=476
while i!=949:
	print "Scraping bug "+str(i)+" of 949"
	os.system("python run.py "+str(i))
	i+=1