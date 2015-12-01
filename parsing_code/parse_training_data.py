import parse_odd_train as odd
import parse_even_train as even


def getFieldsOfEven(paper):
	info = paper.split('\n\n')
	return {
		'title': even.getTitle(info), 
		'journal': even.getJournal(info),
		'relevance': even.getRelevance(info), 
		'pmid': even.getPMID(info),
		'year': even.getYear(info), 
		'abstract': even.getAbstractText(info)
	}

def readEvenNumFile(raw_file, out, category):

	f = open(raw_file, 'r')
	content = f.read().strip().split('\n\n\n\n')

	for paper in content:
		
		fields = getFieldsOfEven(paper)
		paper_info = '\t'.join([category, fields['relevance'], fields['title'], 
			fields['pmid'], fields['journal'], fields['year']]) + '\n'

		out.write(paper_info)


def getRelevanceOfOdd(paper):
	if 'DR' in paper:
		return 'DR'
	elif 'PR' in paper:
		return 'PR'
	else:
		return 'NR'

def readOddNumFile(raw_file, out, category):

	for paper in odd.parse_odd_file(raw_file):
		paper_info = '\t'.join([category, getRelevanceOfOdd(paper), paper['TI'], 
			paper['PMID'], paper['TA'], paper['DP'].split()[0]]) + '\n'

		out.write(paper_info)



def writeEvenAbstracts(raw_file, out, category):
	f = open(raw_file, 'r')
	content = f.read().strip().split('\n\n\n\n')

	for paper in content: 
		fields = getFieldsOfEven(paper)

		paper_info = '\t'.join([
			category, fields['relevance'], fields['pmid'], fields['abstract']
			]) + '\n'

		out.write(paper_info)
		

def writeOddAbstracts(raw_file, out, category):

	for paper in odd.parse_odd_file(raw_file):

		abstract = 'NA'
		if 'AB' in paper:
			abstract = paper['AB']

		abstract = abstract.replace('\n', ' ')

		paper_info = '\t'.join([
			category, getRelevanceOfOdd(paper), paper['PMID'], abstract
			]) + '\n'

		out.write(paper_info)


# Filter by categories list and write into a new file 
def filterByRelevance(fname, out, relevances):
	with open(fname) as f:
		for line in f:
			l = line.split('\t')
			if l[1] in relevances:
				out.write(line)


def writeMetaData():
	outfile = '../info_data/metaData.txt'
	folder = '../abstracts_files/'
	out = open(outfile, 'a')

	readEvenNumFile(folder+'90.txt', out, '90')
	readOddNumFile(folder+'91.txt', out, '91')
	
	readEvenNumFile(folder+'92.txt', out, '92')
	readOddNumFile(folder+'93.txt', out, '93')
	
	readEvenNumFile(folder+'94.txt', out, '94')
	readOddNumFile(folder+'95.txt', out, '95')
	
	readEvenNumFile(folder+'96.txt', out, '96')
	readOddNumFile(folder+'97.txt', out, '97')
	
	readEvenNumFile(folder+'98.txt', out, '98')
	readOddNumFile(folder+'99.txt', out, '99')


def writeAbstractData():

	outfile = '../info_data/abstracts.txt'
	folder = '../abstracts_files/'
	out = open(outfile, 'a')
	# four fields: category \t relevance \t ID \t AbstractString 

	writeEvenAbstracts(folder+'90.txt', out, '90')
	writeOddAbstracts(folder+'91.txt', out, '91')

	writeEvenAbstracts(folder+'92.txt', out, '92')
	writeOddAbstracts(folder+'93.txt', out, '93')

	writeEvenAbstracts(folder+'94.txt', out, '94')
	writeOddAbstracts(folder+'95.txt', out, '95')

	writeEvenAbstracts(folder+'96.txt', out, '96')
	writeOddAbstracts(folder+'97.txt', out, '97')
	
	writeEvenAbstracts(folder+'98.txt', out, '98')
	writeOddAbstracts(folder+'99.txt', out, '99')


def filterEntries():
	meta = '../info_data/metaData.txt'
	outfile_meta = '../info_data/metaData_filtered.txt'
	out_meta = open(outfile_meta, 'w')

	abstracts = '../info_data/abstracts.txt'
	outfile_abstract = '../info_data/abstracts_filtered.txt'
	out_abstracts = open(outfile_abstract, 'w')

	filterByRelevance(meta, out_meta, ['DR', 'PR'])
	filterByRelevance(abstracts, out_abstracts, ['DR', 'PR'])

if __name__ == '__main__':
	writeMetaData()
	writeAbstractData()
	filterEntries()






