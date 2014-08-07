oauth_token="38ee6a10e3491b86a73c0ecec647fdc22eb41ac0"
username='imported-from-roundup'
repo='test'

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
		for i in reversed(bug["history"]):
			body+="<b>Comment by "+i["author"]+":</b><dl><dd>"
			body+=i["message"]
			body+="</dl></dd><hr/>\n\n"
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
	if bug["superceder"]:
		body+="Superceder : <b>#"+bug["superceder"]+"</b>\n"
	body+="Priority: <b>"+bug["priority"]+"</b>\n"
	if bug["waitingon"]:
		body+="Waiting On: <b>#"+bug["waitingon"]+"</b>\n"
	body+="Roundup ID: <b>"+bug["id"]+"</b>\n"
	body+="Last modified: <b>"+bug["lastmodified"]+"</b>\n"

	req = urllib2.Request('https://api.github.com/repos/' + username + '/' + repo + '/issues?access_token='+oauth_token,
			json.dumps({
				'title':bug["title"],
				'body':body,
				'asignee':bug["assigned"],
				'labels':labels
			})
		)
	resp = json.load(urllib2.urlopen(req))
	req = urllib2.Request('https://api.github.com/repos/' + username + '/' + repo + '/issues/'+str(resp["number"])+'?access_token='+oauth_token,
			json.dumps({
				'state':openClosed
			})
		)
	resp = urllib2.urlopen(req)
	#print str(json.load(resp))
	c+=1
