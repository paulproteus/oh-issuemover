oauth_token="74aba8524476083e805734e59784693fffdc960a"

import urllib2, json
import glob

bug_files = glob.glob('bugs/*')
without_dir_name = [x.replace('bugs/', '') for x in bug_files]
as_int = sorted([int(x) for x in without_dir_name])

for c in as_int:
	print "Adding bug "+str(c)+"/" + str(len(as_int))
	bug=json.load(open("bugs/"+str(c)))
	openClosed='open'
	body=""
	if bug["status"]=='resolved':
		openClosed='closed'
	
	if bug["history"]!=[]:
		for i in bug["history"]:
			body+="<b>Comment by "+i["author"]+":</b><i>\n"
			body+=i["message"]
			body+="</i><hr/>\n\n"
	else:
		body+="No Messages!"
	if bug["files"]!=[]:
		for i in bug["files"]:
			body+="<b>File at "+i["url"]+" by "+i["author"]+"</b>\n"
	body+="\n"
	body+="Status : <b>"+bug["status"]+"</b>\n"
	body+="Nosy List : <b>"
	for i in bug["nosylist"]:
		body += "  "+i+" "
	body+="</b>\n"
	labels=bug["keywords"]
	labels.append("imported")
	labels.append(bug["priority"])
	labels.append(bug["status"])
	if bug["milestone"]!="":
		labels.append("milestone:"+bug["milestone"])
	body+="Superceder : <b>"+bug["superceder"]+"</b>\n"
	body+="Priority : <b>"+bug["priority"]+"</b>\n"
	body+="Waiting On : <b>"+bug["waitingon"]+"</b>\n"
	body+="Roundup ID : <b>"+bug["id"]+"</b>\n"

	req = urllib2.Request('https://api.github.com/repos/paulproteus/test-bug-import/issues?access_token='+oauth_token,
			json.dumps({
				'title':bug["title"],
				'body':body,
				'asignee':bug["assigned"],
				'labels':labels
			})
		)
	resp = json.load(urllib2.urlopen(req))
	req = urllib2.Request('https://api.github.com/repos/paulproteus/test-bug-import/issues/'+str(resp["number"])+'?access_token='+oauth_token,
			json.dumps({
				'state':openClosed
			})
		)
	resp = urllib2.urlopen(req)
	#print str(json.load(resp))
	c+=1
