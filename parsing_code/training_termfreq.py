import sys
sys.path.append('/home/slin/Thesis/Jake')
import textExtractionUtils as utils
import timeit
import pickle



def getIDs(text, idList):
	termID = {}
	for sentence in utils.sentenceSplit(text):
		# Tokenize each sentence
		tokens = utils.tokenize(sentence)

		# Get the IDs of terms found in the sentence
		ids = utils.getID_FromLongestTerm(tokens, idList)  # use a dictionary instead
		for i in ids:
			termID[i] = termID.get(i, 0) + 1

	return termID

def getTermFreq(abstracts_file, idList):
	with open(abstracts_file) as f: 
		for line in f:
			l = line.split('\t')
			abstract = l[3]
			yield getIDs(abstract, idList)


def hashAsString(dictionary):
	""" Convert a dictionary to a string
	@input: 	
		a dicitonary of termID : frequencies
	@output:
		a string representing the dictionary, each key-value pair is separated 
		by a tab deliminator, and key and value
		themselves are separated by a space 
	"""

	string = ""

	for key, val in dictionary.iteritems():
		string += ' '.join([str(key), str(val)]) + "\t"

	return string.strip() # strip out the last tab 


def recordTermFreq(abstracts_file, idList, out_file):
	""" Write the term frequencies info to `out_file` for each 
	abstract in `abstracts_file` 
	"""
	out = open(out_file, 'w')

	for IDs in getTermFreq(abstracts_file, idList):
		out.write(hashAsString(IDs) + '\n')


def main():
	t = timeit.default_timer()
	utils.loadParsingTools()
	print "\nTo load parsing tools: ", timeit.default_timer() - t

	t = timeit.default_timer()
	binaryTermsFile =  "/home/slin/Thesis/Jake/umlsWordlist.pickle"
	wordlist = pickle.load(open(binaryTermsFile, "rb"))
	print "\nTo load term file: ", timeit.default_timer() - t

	abstracts_file = "/home/slin/Thesis/data/testData/trec2005_train/abstracts.txt"
	term_freq_file = "/home/slin/Thesis/data/testData/trec2005_train/abstracts_term_freq.txt"

	t = timeit.default_timer()
	recordTermFreq(abstracts_file, wordlist, term_freq_file)
	print "\nTo find terms in all abstracts: ", timeit.default_timer() - t

if __name__ == '__main__':
	main()



