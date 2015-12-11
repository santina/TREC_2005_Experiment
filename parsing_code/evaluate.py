# To evaluate SVD on TREC2005 
from os import listdir
from os.path import isfile, isdir, join
import re 

def buildAbstractExistDict(metadata):
	''' Make and return a hash that records whether a paper has an abstract
	using the line number of the abstracts in the metadata as the key 
	'''
	hasAbstract = {}
	index = 0
	with open(metadata) as f:
		for line in f:
			line = line.strip().split('\t')
			if line[3] != 'NA':
				hasAbstract[index] = True
			else: 
				hasAbstract[index] = False
			index += 1
	return hasAbstract

def buildRelevanceDict(metadata):
	''' Make and return a hash that records the relevance score {'DR', 'PR', 'NR'}
	(definitely relevance, probably relevance, not relevance) and the category 
	for each paper, using the line number of the abstract in the metadata as the key 
	'''
	relevance = {}
	index = 0
	with open(metadata) as f:
		for line in f:
			line = line.split('\t')
			relevance[index] = (line[0], line[1]) # (category, relevance)
			index += 1
	return relevance

def getPrecision(papers, hasAbstract, relevanceDict, category):
	''' Get the precision of the predictions by checking whether 
	the papers in the prediction are of the same category of the 
	target paper and are also relevant 
	'''
	npapers = len(papers)
	numCorrects = 0
	for paperID in papers:
		
		info = relevanceDict[paperID]
		if info[0] == category and info[1] == ('PR' or 'DR'): 
			numCorrects += 1
			
	return float(numCorrects)/npapers

# TODO: implement different metrics of measuring a score (eg recall, MAP)
def getScore(result, hasAbstractDict, relevanceDict, npapers):
	''' Get a score for the prediction by calling getPrecision() 
	return None if the target paper has no abstract
	'''
	
	IDs = [int(i) for i in result.split()]
	paper = IDs[0]
	if relevanceDict[paper][1] == 'NR' or not hasAbstractDict[paper]:
		return None # if the paper has no abstract 
	else: 
		category = relevanceDict[paper][0] 
		return getPrecision(IDs[1:npapers+1], hasAbstractDict, relevanceDict, category)

def recordScore(out, npapers, totalScore, matrixFolder, distanceFolder, closestPapersFile):
	''' Write the average score for a particular combination of a type matrix, a distance function, 
	and number of singular values used to an outfile file `out` 
	'''
	avgScore = str(float(totalScore)/npapers)
	nsv = re.findall(r'\d+', closestPapersFile)[0]

	out.write('\t'.join([matrixFolder, distanceFolder, closestPapersFile, nsv, avgScore]) + '\n')

def main():
	# TODO : use argparse to read in input files and other parameters 

	metadata_wAbstracts = "../info_data/abstracts.txt"
	resultFolder = "/projects/slin_prj/slin_prj_results/closest_papers/TREC2005_train/abstract_only"
	# file organization: 
	# resultFolder 
	#	> (type of matrix) {term_freq, term_freq_binary, tfidf} 
	#		> (type of distance measurement) {euclidean, cosine}
	evalResultOutFile = resultFolder + "/evaluation_relevance.result"
	out = open(evalResultOutFile, 'w')

	hasAbstractDict = buildAbstractExistDict(metadata_wAbstracts)
	relevanceDict = buildRelevanceDict(metadata_wAbstracts)
	nPapers = 20

	# TODO : wrap this chunk in a separate function 

	# traversing the file 
	for matrixFolder in [f for f in listdir(resultFolder) if isdir(join(resultFolder, f))]:
		curDir = join(resultFolder, matrixFolder)
		
		for distanceFolder in [f for f in listdir(curDir) if isdir(join(curDir, f))]:
			curFolder = join(curDir, distanceFolder)

			for closestPapersFile in [f for f in listdir(curFolder) if isfile(join(curFolder, f))]:
				totalScore = 0
				npapers = 0

				with open(join(curFolder, closestPapersFile)) as f:
					for line in f:
						score = getScore(line, hasAbstractDict, relevanceDict, nPapers)
						if score: # skip the papers with no abstract 
							totalScore += score
							npapers += 1 
					recordScore(out, npapers, totalScore, matrixFolder, distanceFolder, closestPapersFile)



if __name__ == '__main__':
	main()
