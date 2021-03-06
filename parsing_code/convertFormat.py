

def convert(termFreqFile, outfile):
	''' convert term frequency file, generated by countFreq.py, to matrix file for GraphLab 
	'''
	with open(termFreqFile) as f, open(outfile, 'w') as out:
		for lineNum, line in enumerate(f):  # 0-base for lineNum
			if l != '\n': # skip the lines with no term freq (paper with no abstract or full text)
				pairs = l.strip().split('\t')
				for p in pairs:
					[termId, freq] = p.split(' ')
					out.write('{0}\t{1}\t{2}\n'.format(lineNum, termId, freq))

def binarize(matrixFile, binaryOut):
	''' Take input of a matrix file (format for GraphLab) and binarize all number 
		# i.e. turn every occurence to 1 and write to `binaryout` 
	'''

	with open(matrixFile) as f, open(binaryOut, 'w') as out:
		for _, line in enumerate(f): 
			
			line = line.split()
			line[2] = '1'
			line = '\t'.join(line)
			out.write(line + '\n')


if __name__ == '__main__':
	# TODO: command line arguments 

	termFreqFile = "../info_data/abstracts_term_freq.txt"
	outfile = "../info_data/matrix/abstracts_term_freq.matrix"
	convert(termFreqFile, outfile)
	
	matrixbinary = "../info_data/matrix/abstracts_term_freq_binary.matrix"
	binarize(outfile, matrixbinary)