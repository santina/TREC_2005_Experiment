# For indexing trec data 
import re 

def getRelevance(info):
	match = re.search(r'\w\w\d+:', info[0])
	if match:
		return match.group()[:2] # get the first two chars 
	else:
		return 'NA'

def getTitle(info):
	if len(info[1]) < 0:
		return 'NA'
	return info[1].replace('\n', ' ')

def getPMID(info):
	for line in info: 
		match = re.search('(?<=PMID: )\d+', line)
		if match:
			return match.group() # get the first two chars 
		
	return str(-1)

def getJournal(info):
	information = info[0].split('.')
	information = information[0].split(':')
	title = information[1].strip()
	if title: 
		return title 
	else:
		return 'NA'

def getYear(info):
	date = info[0].split('.')[1].strip()
	if date:
		date = date.split(' ')[0]
		return date.split(';')[0]
	else:
		return str(-1)

def getAbstractText(info):

	# If there's no abstract for that paper (less than 20 words)
	if not info[4] or len(info[4].split()) < 20:
		return 'NA'

	abstract = info[4].replace('\n', ' ')
	return abstract 





