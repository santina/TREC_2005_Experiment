# To evaluate SVD on TREC2005 
from os import listdir
from os.path import isfile, isdir, join
import re 

def buildAbstractExistDict(metadata):
	hasAbstract = {}
	index = 0
	with open(metadata) as f:
		for line in f:
			line = line.split('\t')
			if line[3] != 'NA':
				hasAbstract[index] = True
			else: 
				hasAbstract[index] = False
			index += 1
	return hasAbstract

def buildRelevanceDict(metadata):
	relevance = {}
	index = 0
	with open(metadata) as f:
		for line in f:
			line = line.split('\t')
			relevance[index] = (line[0], line[1]) # (category, relevance)
			index += 1
	return relevance

def getPrecision(papers, hasAbstract, relevanceDict, category):
	npapers = len(papers)
	numCorrects = 0
	for paperID in papers:
		if hasAbstract[paperID]:
			info = relevanceDict[paperID]
			if info[0] == category and info[1] == ('PR' or 'DR'): 
				numCorrects += 1
			
		else: 
			npapers -= 1
	return float(numCorrects)/npapers

def getScore(result, hasAbstractDict, relevanceDict, npapers):
	
	IDs = [int(i) for i in result.split()]
	paper = IDs[0]
	if relevanceDict[paper][1] == 'NR':
		return None # if the paper has no abstract 
	else: 
		category = relevanceDict[paper][0] 
		return getPrecision(IDs[1:npapers+1], hasAbstractDict, relevanceDict, category)

def recordScore(out, npapers, totalScore, matrixFolder, distanceFolder, closestPapersFile):
	avgScore = str(float(totalScore)/npapers)
	nsv = re.findall(r'\d+', closestPapersFile)[0]

	out.write('\t'.join([matrixFolder, distanceFolder, closestPapersFile, nsv, avgScore]) + '\n')

def main():

	metadata_wAbstracts = "../info_data/abstracts.txt"
	resultFolder = "/projects/slin_prj/slin_prj_results/closest_papers/TREC2005_train"
	# file organization: 
	# resultFolder 
	#	> (type of matrix) {term_freq, term_freq_binary, tfidf} 
	#		> (type of distance measurement) {euclidean, cosine}
	evalResultOutFile = "/projects/slin_prj/slin_prj_results/closest_papers/TREC2005_train/evaluation_relevance.result"
	out = open(evalResultOutFile, 'w')

	hasAbstractDict = buildAbstractExistDict(metadata_wAbstracts)
	relevanceDict = buildRelevanceDict(metadata_wAbstracts)
	nPapers = 20

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
