from lxml import html, etree
import urllib2, json, time
basePath="http://openhatch.org/bugs/"

import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
  
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication([__file__])  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit() 
bugs=[] 
issueNumber=int(sys.argv[1])
def xp(xpath, t=1):
	#try:
	x=root.xpath(xpath)
	if x!=None and x!=[]:
		x=x[0]
		if t:
			x=x.text
			if x==None: return ''
		return x
	else: return None
	#except BaseException as e:
	#	print "ERROR"
	#	print e
	#	return "ERROR"
url = basePath+"issue"+str(issueNumber)
r = Render(url)  
result = ""
for i in r.frame.toHtml():
	try:
		x=str(i)
		result += x
	except:
		result += "(UNKNOWN CHARACTER)"
root = html.fromstring(
		result
	)
time.sleep(0.5)

issue={"id":str(issueNumber)}
issue["title"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[1]/td")
issue["assigned"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[5]/td[1]").strip()
issue["milestone"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[2]/td[1]").strip()
issue["waitingon"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[3]/td[1]").strip()
issue["priority"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[2]/td[2]").strip()
issue["status"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[3]/td[2]").strip()
keywords=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[5]/td[2]").split("\n")
issue["superceder"]=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[4]/td[1]").strip()
nosylist=xp("/html/body/table/tbody/tr[3]/td/div/form/table/tbody/tr[4]/td[2]").split("\n")
files=root.find_class("files")
messages=root.find_class("messages")
issue["files"]=[]
issue["history"]=[]
issue["lastmodified"] = root.xpath('/html/body/table/tbody/tr[3]/td/div/p/b[3]')[0].text.strip()
if messages !=None and messages!=[]:
	messages=messages[0][0]
	messages=messages[1:]
	i=0
	author=""
	while i!=len(messages):
		if i%2==0: #even
			author=messages[i][1].text.replace("Author: ","")
		else:
			v=etree.tostring(messages[i]
						[0]
						[0]
						, pretty_print=True)
			v=v.replace("<pre>","").replace("</pre>","")
			issue["history"].append({
					"author":author,
					"message":v
				})
		i+=1
if files !=None and files!=[]:
	files=files[0][0]
	for i in files[2:]:
		issue["files"].append({
				'url':basePath+i[0][0].attrib["href"],
				'author':i[1][0].text
			})

issue["keywords"]=[]
issue["nosylist"]=[]
for i in keywords:
	x=i.strip()
	if x!='':
		issue["keywords"].append(x)
for i in nosylist:
	x=i.strip()
	if x!='':
		issue["nosylist"].append(x)
bugs.append(issue)
open("bugs/"+str(issueNumber), 'w').write(json.dumps(issue))
issueNumber+=1
del r
del root
del result
open("allbugs", 'w').write(json.dumps({'bugs':bugs}))
