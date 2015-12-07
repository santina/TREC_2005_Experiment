

import argparse
import numpy as np
import timeit
import resource 
import gc



def countEntries(string):
	s = string.split('\t')
	return len(s)

def countOccurrence(string):
	count = 0
	pairs = string.split('\t')
	for p in pairs:
		p = p.split(' ')
		try:
			count += int(p[1])
		except IndexError:
			count += 0
	return count 
			
'''
	Given the filename of all termID - frequency pairs for each paper (whose ID is the line number)
	and the line numbers to start and end the reading of the file, fill the matrix
'''
def countTotalEntries(filename):
	nEntries = 0 
	nTerms = 0 
	with open(filename, 'rb') as f:
		for _ , line in enumerate(f):
			nEntries += countEntries(line)
			#nTerms += countOccurrence(line)
	return nEntries

def buildTermFreqHash(filename):
	h = {}
	with open(filename, 'rb') as f:
		content = f.readlines()
		for line in content: 
			for pair in line.split('\t'):
				p = pair.split(' ')
				if len(p) == 2:
					try: 
						h[int(p[0])] = h.get(int(p[0]), 0) + int(p[1])
					except IndexError or ValueError: 
						continue
	return h

''''
	find number of unused words 
'''
def countUnused(globalHash, ntotalWords):
	count = 0 
	for i in range(0, ntotalWords-1):
		if i not in globalHash:
			count += 1
	return count 

def countUsed(globalHash, ntotalWords):
	count = 0 
	for i in range(0, ntotalWords-1):
		if i in globalHash:
			count += 1
	return count 

def getMostOccurred(globalHash, ntotalWords):
	maxNum = 0 
	maxID = 0
	for i in range(0, ntotalWords-1):
		if i in globalHash:
			if globalHash[i] > maxNum: 
				maxNum = globalHash[i] 
				maxID = i
	return maxNum, maxID



if __name__ == "__main__":
	# The length of all the words in the wordlist for term extraction
	totalWords = 1062805  
	
	filename = "../info_data/abstracts_term_freq.txt"
	h = buildTermFreqHash(filename)
	print countTotalEntries(filename)
	print
	print countUnused(h, totalWords)
	print
	print countUsed(h, totalWords)
	print
	print getMostOccurred(h, totalWords)
